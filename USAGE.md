# Usage Guide

This guide covers using OpenReplay CLI commands.

## Quick Start

```bash
# 1. Authenticate
openreplay auth --client-secret client_secret.json

# 2. Fetch comments
openreplay fetch

# 3. Generate AI replies
openreplay generate

# 4. Publish replies
openreplay publish
```

## Command Reference

### `openreplay` (help)

Show help and version information.

```bash
openreplay
openreplay --help
openreplay --version
```

### `openreplay auth`

Authenticate with YouTube using OAuth2.

```bash
# Basic authentication
openreplay auth

# With client secret file
openreplay auth --client-secret path/to/client_secret.json
```

**Behavior:**
- Opens browser for OAuth2 flow
- Stores tokens in `tokens/youtube.json`
- Handles token refresh automatically

**Options:**
- `--client-secret PATH`: Path to OAuth client secret JSON file

**Example:**
```bash
$ openreplay auth --client-secret config/client_secret.json
Open this URL in your browser:
https://accounts.google.com/o/oauth2/v2/auth?...

Enter the authorization code: 4/0Aean...
Authentication successful!
Tokens stored in tokens/youtube.json
```

### `openreplay fetch`

Fetch comments from your YouTube video.

```bash
# Basic fetch
openreplay fetch

# Custom output file
openreplay fetch --output workspace/my_comments.json
openreplay fetch -o workspace/my_comments.json
```

**Behavior:**
- Loads video_id from config.yaml
- Authenticates if needed
- Fetches all comments for the video
- Saves to workspace/comments.json

**Options:**
- `--output PATH, -o PATH`: Output file path

**Example:**
```bash
$ openreplay fetch
Fetching comments for video dQw4w9WgXcQ...
Fetched 142 comments from video dQw4w9WgXcQ
Saved to workspace/comments.json
```

### `openreplay generate`

Generate AI responses for fetched comments.

```bash
# Basic generation
openreplay generate

# With custom knowledge base
openreplay generate --knowledge-file knowledge.md

# Custom output
openreplay generate --output workspace/replies.json
```

**Behavior:**
- Loads comments from workspace/comments.json
- Builds prompts using policy and style config
- Calls LLM for each comment
- Applies response template
- Saves to workspace/replies.json

**Options:**
- `--knowledge-file PATH, -k PATH`: Knowledge base file path (default: knowledge.md)
- `--output PATH, -o PATH`: Output file path (default: workspace/replies.json)

**Example:**
```bash
$ openreplay generate
Loading comments...
Found 142 comments
Generating AI responses using qwen3.
Knowledge mode: knowledge_preferred
Response style: friendly

Generated 142 responses
Failed: 0
```

### `openreplay publish`

Publish generated replies to YouTube.

```bash
# Basic publish
openreplay publish

# Preview without publishing
openreplay publish --dry-run

# Custom replies file
openreplay publish --replies-file workspace/replies.json
```

**Behavior:**
- Loads replies from workspace/replies.json
- Authenticates if needed
- Publishes each reply to corresponding comment
- Saves published status to workspace/published.json

**Options:**
- `--replies-file PATH`: Replies file path (default: workspace/replies.json)
- `--dry-run`: Preview without publishing (default: false)

**Example:**
```bash
$ openreplay publish
Publishing 142 replies to YouTube...
Published to comment ckx_123: Thanks for your question! 👍
Published to comment ckx_124: Yes, this is available worldwide! 🌍
...

Published 140 replies
Failed: 2
```

## Working with Configuration

### Video ID Setup

Set your video ID in config.yaml:

```yaml
youtube:
  video_id: dQw4w9WgXcQ
```

### Knowledge Base

Edit `knowledge.md` for AI context:

```markdown
# Knowledge Base

Q: How does this work?
A: We use AI to automatically respond to comments.

Q: Is it free?
A: Yes, the basic version is completely free!
```

### Policy Modes

Choose how AI uses knowledge:

```yaml
policy:
  mode: knowledge_preferred  # or knowledge_only, fallback_only, general
```

### Response Styles

Control AI tone:

```yaml
generation:
  style: friendly  # or professional, enthusiastic, neutral
```

## Common Workflows

### Initial Setup (First Time)

```bash
# 1. Setup configuration
cp config.example.yaml config.yaml
# Edit config.yaml with your video_id

# 2. Authenticate
openreplay auth --client-secret client_secret.json

# 3. Test fetch
openreplay fetch
```

### Regular Comment Management

```bash
# 1. Fetch new comments
openreplay fetch

# 2. Review in workspace/comments.json
# Edit knowledge.md if needed

# 3. Generate replies
openreplay generate

# 4. Review in workspace/replies.json
# Edit manually if needed

# 5. Publish
openreplay publish
```

### Dry-Run Workflow

```bash
# Test without publishing
openreplay publish --dry-run

# Review output
cat workspace/published.json
```

## Output Files

### workspace/comments.json

```json
{
  "comments": [
    {
      "id": "comment_id",
      "content": "Comment text",
      "author": "Author Name",
      "published_at": "2024-01-01T10:00:00Z"
    }
  ],
  "loaded_at": "2024-01-01T12:00:00Z"
}
```

### workspace/replies.json

```json
{
  "replies": [
    {
      "comment_id": "comment_id",
      "original_comment": "Comment text",
      "generated_content": "AI generated text",
      "final_reply": "Final response",
      "knowledge_mode": "knowledge_preferred",
      "style": "friendly",
      "timestamp": "2024-01-01T12:00:00Z",
      "status": "generated"
    }
  ],
  "generated_at": "2024-01-01T12:00:00Z"
}
```

### workspace/published.json

```json
{
  "published": [
    {
      "comment_id": "comment_id",
      "reply_id": "reply_id",
      "timestamp": "2024-01-01T12:00:00Z",
      "status": "success"
    }
  ],
  "published_at": "2024-01-01T12:00:00Z"
}
```

## Tips

1. **Use dry-run first**: Always test publishing with `--dry-run`
2. **Review before publishing**: Check `workspace/replies.json` manually
3. **Edit knowledge base**: Update `knowledge.md` for better AI responses
4. **Token persistence**: Tokens are saved; you only need to auth once
5. **Error handling**: Failed replies are tracked in output files
