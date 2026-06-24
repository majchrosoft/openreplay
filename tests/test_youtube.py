"""YouTube provider tests."""

import json
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

from providers.youtube import YouTubeProvider, Comment, Video
from providers.base import Provider


class TestYouTubeProvider(unittest.TestCase):
    """Test YouTube provider."""

    def test_provider_interface(self):
        """Test YouTubeProvider implements Provider interface."""
        self.assertTrue(isinstance(YouTubeProvider(), Provider))

    @patch("providers.youtube.webbrowser.open")
    def test_authenticate_new_tokens(self, mock_webbrowser):
        """Test authentication with new tokens."""
        with patch("providers.youtube.requests.post") as mock_post:
            mock_response = Mock()
            mock_response.json.return_value = {
                "access_token": "test_token",
                "expires_in": 3600,
                "refresh_token": "refresh_token",
            }
            mock_response.raise_for_status = Mock()
            mock_post.return_value = mock_response

            with patch("builtins.input", return_value="auth_code_123"):
                provider = YouTubeProvider("client_id", "client_secret")
                tokens = provider.authenticate()

            self.assertEqual(tokens["access_token"], "test_token")
            self.assertIn("expires_at", tokens)

    def test_authenticate_missing_credentials(self):
        """Test authentication raises error without credentials."""
        provider = YouTubeProvider()
        with self.assertRaises(ValueError):
            provider.authenticate()

    @patch("providers.youtube.requests.post")
    def test_refresh_tokens(self, mock_post):
        """Test token refresh."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "new_token",
            "expires_in": 3600,
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        provider = YouTubeProvider("client_id", "client_secret")
        tokens = provider._refresh_tokens("refresh_token")

        self.assertEqual(tokens["access_token"], "new_token")

    def test_list_resources_not_authenticated(self):
        """Test list_resources raises error when not authenticated."""
        provider = YouTubeProvider("client_id", "client_secret")
        with self.assertRaises(ValueError):
            provider.list_resources()

    @patch("providers.youtube.requests.get")
    def test_list_resources(self, mock_get):
        """Test listing YouTube videos."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [
                {
                    "id": "video1",
                    "snippet": {
                        "title": "Test Video",
                        "publishedAt": "2024-01-01T00:00:00Z",
                    },
                    "statistics": {"commentCount": "10"},
                }
            ],
            "nextPageToken": None,
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        provider = YouTubeProvider("client_id", "client_secret")
        provider.credentials = {"access_token": "test_token"}

        videos = provider.list_resources()

        self.assertEqual(len(videos), 1)
        self.assertIsInstance(videos[0], Video)
        self.assertEqual(videos[0].id, "video1")
        self.assertEqual(videos[0].title, "Test Video")

    def test_list_comments_not_authenticated(self):
        """Test list_comments raises error when not authenticated."""
        provider = YouTubeProvider("client_id", "client_secret")
        with self.assertRaises(ValueError):
            provider.list_comments("video_id")

    @patch("providers.youtube.requests.get")
    def test_list_comments(self, mock_get):
        """Test fetching YouTube comments."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [
                {
                    "id": "comment1",
                    "snippet": {
                        "topLevelComment": {
                            "snippet": {
                                "authorDisplayName": "User1",
                                "textDisplay": "Great video!",
                                "publishedAt": "2024-01-01T00:00:00Z",
                                "likeCount": 5,
                            }
                        },
                        "totalReplyCount": 2,
                    },
                }
            ],
            "nextPageToken": None,
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        provider = YouTubeProvider("client_id", "client_secret")
        provider.credentials = {"access_token": "test_token"}

        comments = provider.list_comments("video_id", max_results=10)

        self.assertEqual(len(comments), 1)
        self.assertIsInstance(comments[0], Comment)
        self.assertEqual(comments[0].id, "comment1")
        self.assertEqual(comments[0].text, "Great video!")

    def test_publish_reply_not_authenticated(self):
        """Test publish_reply raises error when not authenticated."""
        provider = YouTubeProvider("client_id", "client_secret")
        with self.assertRaises(ValueError):
            provider.publish_reply("comment_id", "Reply content")

    @patch("providers.youtube.requests.post")
    def test_publish_reply(self, mock_post):
        """Test publishing YouTube reply."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "reply123"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        provider = YouTubeProvider("client_id", "client_secret")
        provider.credentials = {"access_token": "test_token"}

        result = provider.publish_reply("comment_id", "Reply content")

        self.assertEqual(result["id"], "reply123")
        mock_post.assert_called_once()

    def test_get_user_info_not_authenticated(self):
        """Test get_user_info raises error when not authenticated."""
        provider = YouTubeProvider("client_id", "client_secret")
        with self.assertRaises(ValueError):
            provider.get_user_info()

    @patch("providers.youtube.requests.get")
    def test_get_user_info(self, mock_get):
        """Test getting user information."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [
                {
                    "id": "channel1",
                    "snippet": {
                        "title": "My Channel",
                    },
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        provider = YouTubeProvider("client_id", "client_secret")
        provider.credentials = {"access_token": "test_token"}

        user_info = provider.get_user_info()

        self.assertEqual(user_info["id"], "channel1")
        self.assertEqual(user_info["snippet"]["title"], "My Channel")


class TestDataClasses(unittest.TestCase):
    """Test data classes."""

    def test_video_dataclass(self):
        """Test Video dataclass."""
        video = Video(
            id="video123",
            title="Test Video",
            published_at=datetime.fromisoformat("2024-01-01T00:00:00+00:00"),
            comment_count=10,
        )
        
        self.assertEqual(video.id, "video123")
        self.assertEqual(video.title, "Test Video")
        self.assertEqual(video.comment_count, 10)

    def test_comment_dataclass(self):
        """Test Comment dataclass."""
        comment = Comment(
            id="comment123",
            author="User1",
            text="Great video!",
            published_at=datetime.fromisoformat("2024-01-01T00:00:00+00:00"),
            like_count=5,
            reply_count=2,
        )
        
        self.assertEqual(comment.id, "comment123")
        self.assertEqual(comment.author, "User1")
        self.assertEqual(comment.text, "Great video!")


if __name__ == "__main__":
    unittest.main()
