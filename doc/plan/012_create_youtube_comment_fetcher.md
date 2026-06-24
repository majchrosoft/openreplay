# 012 - Create YouTube Comment Fetcher

## Objective
Implement functionality to fetch comments for a specific YouTube video.

## Input
- YouTube API credentials
- Video ID

## Output
- List of comments for the specified video

## Deliverables

### Files to Create
1. Extend `providers/youtube.py` - Add comment fetching

### Features
- Fetch comments for video ID from config
- Handle YouTube API pagination
- Extract comment metadata
- Store in workspace/comments.json

### Comment Data Structure
```python
class Comment:
    id: str
    author: str
    text: str
    published_at: datetime
    like_count: int
    reply_count: int
```

### Storage
```
workspace/
├── comments.json
    [
        {
            "id": "...",
            "author": "...",
            "text": "...",
            "published_at": "...",
            "like_count": ...,
            "reply_count": ...
        }
    ]
```

## Testing
- Test with valid video ID
- Verify comment count matches
- Test pagination handling
- Test API errors

## Time Estimate
1.5 hours
