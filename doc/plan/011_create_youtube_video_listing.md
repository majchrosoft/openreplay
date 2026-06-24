# 011 - Create YouTube Video List Fetcher

## Objective
Implement functionality to list YouTube videos accessible to the authenticated user.

## Input
- YouTube API credentials
- None (fetches user's videos)

## Output
- List of YouTube videos with metadata

## Deliverables

### Files to Create
1. Extend `providers/youtube.py` - Add video listing

### Features
- Fetch user's video list
- Display video metadata (title, ID, published date)
- Handle pagination
- Error handling

### Video Metadata
```python
class Video:
    id: str
    title: str
    published_at: datetime
    comment_count: int
```

## Testing
- Test with valid authentication
- Verify video metadata extraction
- Test error handling (no videos, API errors)

## Time Estimate
1 hour
