# 017 - Create Fetch Command

## Objective
Create the fetch comments CLI command.

## Input
- Command: `openreplay fetch`
- Configuration from config.yaml
- Authentication from tokens/youtube.json

## Output
- Comments saved to workspace/comments.json

## Deliverables

### Files to Create
1. `commands/fetch.py` - Fetch command

### Features
- Load configuration for video_id
- Authenticate with YouTube
- Fetch comments for video
- Save to workspace/comments.json
- Show comment count

### Command Implementation
```python
def main():
    config = load_config()
    auth = load_auth()
    comments = youtube.fetch_comments(config.youtube.video_id, auth)
    save_comments(comments)
    print(f"Fetched {len(comments)} comments")
```

## Testing
- Test with valid authentication
- Test with missing authentication
- Test with invalid video ID
- Verify JSON storage

## Time Estimate
1 hour
