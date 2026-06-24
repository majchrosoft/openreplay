"""Fetch command."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

import argparse
import json
from datetime import datetime
from pathlib import Path

from openreplay.config import config
from providers.youtube import YouTubeProvider


def save_comments(comments: list, filepath: str = "workspace/comments.json") -> None:
    """Save comments to JSON file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "comments": comments,
        "loaded_at": datetime.now().isoformat(),
    }
    
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def run(args: argparse.Namespace):
    """Execute fetch command."""
    video_id = config.video_id
    
    if not video_id:
        print("Error: No video_id configured in config.yaml")
        print("Please set youtube.video_id in your config file.")
        return
    
    output_file = getattr(args, "output", "workspace/comments.json")
    
    provider = YouTubeProvider()
    
    try:
        tokens = provider.authenticate()
    except ValueError as e:
        print(f"Authentication error: {e}")
        return
    except Exception as e:
        print(f"Authentication error: {e}")
        return
    
    try:
        comments = provider.list_comments(video_id)
    except Exception as e:
        print(f"Failed to fetch comments: {e}")
        return
    
    comments_data = []
    for comment in comments:
        comments_data.append({
            "id": comment.id,
            "content": comment.text,
            "author": comment.author,
            "published_at": comment.published_at.isoformat(),
        })
    
    save_comments(comments_data, output_file)
    
    print(f"Fetched {len(comments)} comments from video {video_id}")
    print(f"Saved to {output_file}")
