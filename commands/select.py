"""Select command - fetch and choose YouTube videos."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

import argparse
import json
from pathlib import Path

import yaml

from openreplay.config import config
from providers.youtube import YouTubeProvider


def save_videos(videos: list, filepath: str = "workspace/videos.json") -> None:
    """Save videos to JSON file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "videos": [video.__dict__ for video in videos],
        "loaded_at": __import__('datetime').datetime.now().isoformat(),
    }
    
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def update_config(video_id: str) -> None:
    """Update config.yaml with video ID."""
    config_path = Path("config.yaml")
    
    # Load existing config or create empty
    if config_path.exists():
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f) or {}
    else:
        config_data = {}
    
    # Update youtube.video_id
    if "youtube" not in config_data:
        config_data["youtube"] = {}
    config_data["youtube"]["video_id"] = video_id
    
    # Write back
    with open(config_path, "w") as f:
        yaml.dump(config_data, f, default_flow_style=False)


def display_videos(videos: list) -> None:
    """Display video list with index numbers."""
    if not videos:
        print("No videos found.")
        return
    
    print("\nAvailable videos:")
    for i, video in enumerate(videos, 1):
        comments = f"({video.comment_count:,} comments)" if video.comment_count > 0 else "(0 comments)"
        print(f"  [{i}] {video.id} - {video.title} {comments}")
    print("  [0] Enter video ID manually")


def run(args: argparse.Namespace):
    """Execute select command."""
    provider = YouTubeProvider()
    
    # Check authentication
    try:
        tokens = provider.authenticate()
    except ValueError as e:
        print(f"Authentication error: {e}")
        return
    except Exception as e:
        print(f"Authentication error: {e}")
        return
    
    # Fetch videos
    try:
        videos = provider.list_resources()
    except Exception as e:
        print(f"Failed to fetch videos: {e}")
        return
    
    # Save videos to file if requested
    output_file = getattr(args, "output", None)
    if output_file:
        save_videos(videos, output_file)
        print(f"Saved video list to {output_file}")
    
    # Display videos
    display_videos(videos)
    
    if not videos:
        print("\nNo videos found. Please upload videos to your YouTube channel first.")
        return
    
    # Get user selection
    while True:
        try:
            choice = input("\nEnter video number to select (or 'q' to quit): ").strip()
            
            if choice.lower() == 'q':
                print("Cancelled.")
                return
            
            choice_num = int(choice)
            
            if choice_num == 0:
                # Manual ID entry
                custom_id = input("Enter YouTube video ID: ").strip()
                if custom_id:
                    # Verify video exists
                    try:
                        # Test by trying to fetch comments (will fail if video doesn't exist)
                        provider.list_comments(custom_id, max_results=1)
                        update_config(custom_id)
                        print(f"Selected video ID: {custom_id}")
                        print("Config updated successfully!")
                        return
                    except Exception as e:
                        print(f"Invalid video ID: {e}")
                        print("Please try again.")
                        continue
                else:
                    print("ID cannot be empty. Please try again.")
                    continue
            
            if 1 <= choice_num <= len(videos):
                selected_video = videos[choice_num - 1]
                update_config(selected_video.id)
                print(f"Selected: {selected_video.title}")
                print(f"Video ID: {selected_video.id}")
                print("Config updated successfully!")
                return
            else:
                print("Invalid selection. Please try again.")
                
        except ValueError:
            print("Please enter a valid number or 'q' to quit.")
        except KeyboardInterrupt:
            print("\nCancelled.")
            return


def main():
    """Main entry point for select command."""
    parser = argparse.ArgumentParser(
        description="Fetch and select YouTube videos",
        prog="openreplay select",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file to save video list",
    )
    
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
