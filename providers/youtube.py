"""YouTube OAuth2 authentication provider."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

import json
import os
import time
import webbrowser
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import requests

from providers.base import Provider


@dataclass
class Video:
    """YouTube video metadata."""
    id: str
    title: str
    published_at: datetime
    comment_count: int


@dataclass
class Comment:
    """YouTube comment metadata."""
    id: str
    author: str
    text: str
    published_at: datetime
    like_count: int
    reply_count: int


class YouTubeProvider(Provider):
    """YouTube provider with OAuth2 authentication."""

    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
    REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"

    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        """Initialize YouTube provider.
        
        Args:
            client_id: OAuth2 client ID from Google Cloud Console
            client_secret: OAuth2 client secret from Google Cloud Console
        """
        self.client_id = client_id or os.environ.get("YOUTUBE_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("YOUTUBE_CLIENT_SECRET")
        self.tokens_file = Path("tokens/youtube.json")
        self.credentials = None

    def _load_tokens(self) -> Optional[dict]:
        """Load stored tokens from file."""
        if not self.tokens_file.exists():
            return None
        try:
            with open(self.tokens_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def _save_tokens(self, tokens: dict) -> None:
        """Save tokens to file."""
        self.tokens_file.parent.mkdir(exist_ok=True)
        with open(self.tokens_file, "w") as f:
            json.dump(tokens, f, indent=2)

    def _refresh_tokens(self, refresh_token: str) -> dict:
        """Refresh access token using refresh token."""
        response = requests.post(
            self.TOKEN_URL,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
        )
        response.raise_for_status()
        return response.json()

    def authenticate(self) -> dict:
        """Execute OAuth2 flow and return credentials.
        
        Returns:
            dict: Authentication credentials with access token
            
        Raises:
            ValueError: If client ID or secret not provided
        """
        if not self.client_id or not self.client_secret:
            raise ValueError("Client ID and client secret must be provided")

        tokens = self._load_tokens()

        if tokens:
            if tokens.get("expires_at", 0) > time.time():
                self.credentials = tokens
                return tokens
            
            if tokens.get("refresh_token"):
                try:
                    tokens = self._refresh_tokens(tokens["refresh_token"])
                    tokens["expires_at"] = time.time() + tokens.get("expires_in", 3600)
                    self._save_tokens(tokens)
                    self.credentials = tokens
                    return tokens
                except requests.exceptions.RequestException:
                    pass

        auth_url = (
            f"{self.AUTH_URL}"
            f"?client_id={self.client_id}"
            f"&redirect_uri={self.REDIRECT_URI}"
            f"&scope={self.SCOPE}"
            f"&response_type=code"
        )

        print(f"Open this URL in your browser:\n{auth_url}")
        webbrowser.open(auth_url)

        auth_code = input("Enter the authorization code: ").strip()

        response = requests.post(
            self.TOKEN_URL,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": auth_code,
                "redirect_uri": self.REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        response.raise_for_status()

        tokens = response.json()
        tokens["expires_at"] = time.time() + tokens.get("expires_in", 3600)
        self._save_tokens(tokens)
        self.credentials = tokens

        return tokens

    def _make_request(self, endpoint: str, params: Optional[dict] = None, method: str = "GET", data: Optional[dict] = None) -> dict:
        """Make authenticated YouTube API request.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            method: HTTP method (GET, POST)
            data: Request body for POST requests
            
        Returns:
            dict: JSON response from API
        """
        if not self.credentials:
            raise ValueError("Not authenticated. Call authenticate() first.")
        
        headers = {
            "Authorization": f"Bearer {self.credentials['access_token']}",
            "Content-Type": "application/json",
        }
        
        if method == "GET":
            url = f"https://www.googleapis.com/youtube/v3/{endpoint}"
            response = requests.get(url, headers=headers, params=params or {})
        else:
            url = f"https://www.googleapis.com/youtube/v3/{endpoint}"
            response = requests.post(url, headers=headers, params=params or {}, json=data or {})
        
        response.raise_for_status()
        return response.json()

    def list_resources(self) -> List[Video]:
        """List available resources (videos).
        
        Returns:
            List[Video]: List of videos with metadata
            
        Raises:
            ValueError: If not authenticated
            requests.exceptions.RequestException: API request failed
        """
        if not self.credentials:
            raise ValueError("Not authenticated. Call authenticate() first.")

        videos = []
        page_token = None

        while True:
            params = {
                "part": "snippet,statistics",
                "mine": "true",
                "maxResults": 50,
            }
            if page_token:
                params["pageToken"] = page_token

            response = self._make_request("videos", params)
            
            for item in response.get("items", []):
                snippet = item.get("snippet", {})
                statistics = item.get("statistics", {})
                
                video = Video(
                    id=item["id"],
                    title=snippet.get("title", "Unknown"),
                    published_at=datetime.fromisoformat(snippet["publishedAt"].replace("Z", "+00:00")),
                    comment_count=int(statistics.get("commentCount", 0)),
                )
                videos.append(video)

            page_token = response.get("nextPageToken")
            if not page_token:
                break

        return videos

    def list_comments(self, video_id: str, max_results: int = 100) -> List[Comment]:
        """Fetch comments for a specific video.
        
        Args:
            video_id: YouTube video ID
            max_results: Maximum number of comments to fetch
            
        Returns:
            List[Comment]: List of comments with metadata
            
        Raises:
            ValueError: If not authenticated
            requests.exceptions.RequestException: API request failed
        """
        if not self.credentials:
            raise ValueError("Not authenticated. Call authenticate() first.")

        comments = []
        page_token = None
        results_per_page = min(max_results, 100)

        while len(comments) < max_results:
            params = {
                "part": "snippet,replies",
                "videoId": video_id,
                "textFormat": "plainText",
                "maxResults": results_per_page,
            }
            if page_token:
                params["pageToken"] = page_token

            response = self._make_request("commentThreads", params)
            
            for item in response.get("items", []):
                snippet = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
                
                comment = Comment(
                    id=item["id"],
                    author=snippet.get("authorDisplayName", "Unknown"),
                    text=snippet.get("textDisplay", ""),
                    published_at=datetime.fromisoformat(snippet["publishedAt"].replace("Z", "+00:00")),
                    like_count=int(snippet.get("likeCount", 0)),
                    reply_count=int(item.get("snippet", {}).get("totalReplyCount", 0)),
                )
                comments.append(comment)

            page_token = response.get("nextPageToken")
            if not page_token:
                break

        return comments[:max_results]

    def publish_reply(self, comment_id: str, reply_content: str) -> dict:
        """Publish a reply to a specific comment.
        
        Args:
            comment_id: YouTube comment ID to reply to
            reply_content: Text content of the reply
            
        Returns:
            dict: API response with reply details
            
        Raises:
            ValueError: If not authenticated
            requests.exceptions.RequestException: API request failed
        """
        if not self.credentials:
            raise ValueError("Not authenticated. Call authenticate() first.")

        data = {
            "snippet": {
                "parentId": comment_id,
                "textOriginal": reply_content,
            }
        }

        response = self._make_request(
            "comments",
            method="POST",
            data=data,
        )

        return response

    def get_user_info(self) -> dict:
        """Get authenticated user information.
        
        Returns:
            dict: User profile information
            
        Raises:
            ValueError: If not authenticated
            requests.exceptions.RequestException: API request failed
        """
        if not self.credentials:
            raise ValueError("Not authenticated. Call authenticate() first.")

        response = self._make_request(
            "channels",
            params={"part": "snippet,contentDetails,statistics", "mine": "true"},
        )

        if items := response.get("items"):
            return items[0]

        return {}
