"""Publish command."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

import argparse
import json
from datetime import datetime
from pathlib import Path

from openreplay.config import config
from providers.youtube import YouTubeProvider


def load_replies(filepath: str = "workspace/replies.json") -> list:
    """Load replies from JSON file."""
    path = Path(filepath)
    if not path.exists():
        return []
    
    with open(path, "r") as f:
        data = json.load(f)
        return data.get("replies", [])


def save_published(published: list, filepath: str = "workspace/published.json") -> None:
    """Save published replies to JSON file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "published": published,
        "published_at": datetime.now().isoformat(),
    }
    
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def run(args: argparse.Namespace):
    """Execute publish command."""
    replies_file = getattr(args, "replies_file", "workspace/replies.json")
    dry_run = getattr(args, "dry_run", False)
    
    replies = load_replies(replies_file)
    
    if not replies:
        print("No replies to publish.")
        return
    
    # Load previously published replies to avoid duplicates
    published_replies_file = Path("workspace/published.json")
    already_published = set()
    if published_replies_file.exists():
        with open(published_replies_file, "r") as f:
            data = json.load(f)
            already_published = {r.get("comment_id") for r in data.get("published", [])}
    
    provider = YouTubeProvider()
    
    try:
        tokens = provider.authenticate()
    except ValueError as e:
        print(f"Authentication error: {e}")
        return
    except Exception as e:
        print(f"Authentication error: {e}")
        return
    
    published = []
    video_id = config.video_id
    
    if not video_id:
        print("Error: No video_id configured in config.yaml")
        return
    
    for reply in replies:
        if reply.get("status") != "generated":
            print(f"Skipping {reply['comment_id']}: status={reply['status']}")
            continue
        
        comment_id = reply["comment_id"]
        
        # Skip if already published
        if comment_id in already_published:
            print(f"Skipping {comment_id}: already published")
            continue
        
        reply_content = reply["final_reply"]
        
        if dry_run:
            print(f"[DRY RUN] Would publish to comment {comment_id}: {reply_content[:50]}...")
            published.append({
                "comment_id": comment_id,
                "reply_id": "dry_run",
                "timestamp": datetime.now().isoformat(),
                "status": "skipped (dry run)",
            })
            continue
        
        try:
            result = provider.publish_reply(comment_id, reply_content)
            reply_id = result.get("id", "unknown")
            
            published.append({
                "comment_id": comment_id,
                "reply_id": reply_id,
                "timestamp": datetime.now().isoformat(),
                "status": "success",
            })
            
            print(f"Published to comment {comment_id}: {reply_content[:50]}...")
        except Exception as e:
            published.append({
                "comment_id": comment_id,
                "reply_id": None,
                "timestamp": datetime.now().isoformat(),
                "status": "failed",
                "error": str(e),
            })
            
            print(f"Failed to publish to comment {comment_id}: {e}")
    
    save_published(published)
    
    success_count = sum(1 for p in published if p["status"] == "success")
    failed_count = sum(1 for p in published if p["status"] == "failed")
    
    print(f"\nPublished {success_count} replies")
    if failed_count > 0:
        print(f"Failed: {failed_count}")
