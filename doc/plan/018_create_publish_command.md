# 018 - Create Publish Command

## Objective
Create the publish replies CLI command.

## Input
- Command: `openreplay publish`
- Generated replies from workspace/replies.json
- YouTube authentication

## Output
- Replies published to YouTube comments

## Deliverables

### Files to Create
1. `commands/publish.py` - Publish command

### Features
- Load generated replies
- Load YouTube authentication
- Publish each reply
- Track published replies
- Save to workspace/published.json
- Show summary

### Command Implementation
```python
def main():
    replies = load_replies()
    auth = load_auth()
    published = []
    
    for reply in replies:
        if reply.status == "generated":
            result = youtube.publish_reply(
                config.youtube.video_id,
                reply.comment_id,
                reply.final_reply,
                auth
            )
            published.append({
                "comment_id": reply.comment_id,
                "reply_id": result.id,
                "timestamp": datetime.now(),
                "status": "success"
            })
    
    save_published(published)
```

## Testing
- Test with valid replies
- Test with missing authentication
- Test partial failures
- Verify publishing works

## Time Estimate
1 hour
