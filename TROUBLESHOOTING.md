# Troubleshooting Guide

Common issues and solutions for OpenReplay.

## Authentication Issues

### "Client ID and client secret must be provided"

**Error:**
```
ValueError: Client ID and client secret must be provided
```

**Solution:**
- Create OAuth credentials in [Google Cloud Console](https://console.cloud.google.com/)
- Download client secret JSON file
- Use: `openreplay auth --client-secret client_secret.json`

### "Not authenticated. Call authenticate() first."

**Error:**
```
ValueError: Not authenticated. Call authenticate() first.
```

**Solution:**
- Run: `openreplay auth --client-secret client_secret.json`
- Check `tokens/youtube.json` exists

### Token Expiration

**Symptoms:**
- API calls failing with 401 errors
- "Token expired" messages

**Solution:**
- Tokens auto-refresh when expired
- If issues persist, re-authenticate: `openreplay auth --client-secret client_secret.json`

## Configuration Issues

### "No video_id configured in config.yaml"

**Error:**
```
Error: No video_id configured in config.yaml
```

**Solution:**
Edit `config.yaml`:
```yaml
youtube:
  video_id: YOUR_VIDEO_ID
```

### "config.yaml not found"

**Symptoms:**
- Warning about missing config file
- Script continues with defaults

**Solution:**
Create `config.yaml`:
```bash
cp config.example.yaml config.yaml
# Edit with your values
```

## Fetch Issues

### "Failed to fetch comments"

**Causes:**
- Invalid video ID
- No comments on video
- Authentication issues

**Solution:**
1. Verify video_id in config.yaml
2. Check video has comments on YouTube
3. Re-authenticate: `openreplay auth --client-secret client_secret.json`

### Empty comments array

**Symptoms:**
```
No comments to process. Run 'openreplay fetch' first.
```

**Solution:**
- Video may have no comments
- Check video on YouTube directly
- Try fetch with different video

## Generation Issues

### "No comments to process"

**Solution:**
- Run fetch first: `openreplay fetch`
- Check `workspace/comments.json` exists and has content

### LLM Connection Failed

**Symptoms:**
- "Connection refused" errors
- "Connection timed out"

**Solution:**
1. Check LLM service running: `curl http://localhost:11434/api/tags`
2. Update config.yaml with correct base_url
3. For OpenAI: Set correct API key and model

### Knowledge Base Not Loading

**Symptoms:**
- "File not found" errors for knowledge.md

**Solution:**
Create knowledge base:
```bash
cat > knowledge.md << EOF
# Knowledge Base

Q: How does this work?
A: This works by following a simple process.

Q: Is this available internationally?
A: Yes, this service is available worldwide.
EOF
```

## Publish Issues

### "Authentication error"

**Solution:**
- Re-authenticate before publishing: `openreplay auth --client-secret client_secret.json`
- Check tokens/youtube.json is valid

### Partial failures

**Symptoms:**
```
Published 140 replies
Failed: 2
```

**Solution:**
- Check `workspace/published.json` for failed items
- Retry failed replies manually if needed
- Some comments may have been deleted/privacy settings

### Dry-run shows different results

**Symptoms:**
- Actual publish differs from dry-run

**Solution:**
- Dry-run shows what *would* be published
- Comments may be deleted between dry-run and actual publish
- Status is tracked in `workspace/published.json`

## File Issues

### Files not being created

**Symptoms:**
- No output in workspace/

**Solution:**
Check directory permissions:
```bash
mkdir -p workspace
chmod 755 workspace
```

### Wrong file paths

**Solution:**
Use correct paths or defaults:
```bash
openreplay fetch -o workspace/comments.json
openreplay generate -o workspace/replies.json
openreplay publish --replies-file workspace/replies.json
```

## Performance Issues

### Slow comment fetching

**Causes:**
- Many comments (pagination)
- Network latency

**Solutions:**
- Fetch only recent comments (future feature)
- Check internet connection
- Consider rate limits

### Slow AI generation

**Causes:**
- Large knowledge base
- Complex prompts
- Slow LLM service

**Solutions:**
- Optimize knowledge.md (remove redundant Q&A)
- Use faster LLM (change model in config.yaml)
- Batch process (future feature)

## Common Error Messages

| Error | Cause | Solution |
|-------|------|--------|
| "Not authenticated" | No valid tokens | `openreplay auth` |
| "Video not found" | Invalid video_id | Check config.yaml |
| "No comments" | Video has no comments | Check video on YouTube |
| "Connection refused" | LLM service down | Start Ollama or check API |
| "Rate limit exceeded" | Too many requests | Wait and retry |

## Getting Help

1. **Check logs**: Examine workspace files for errors
2. **Review docs**: See USAGE.md for command details
3. **Test flow**: Run each command step-by-step
4. **Configuration**: Verify all required fields in config.yaml

## Debug Mode

Enable verbose output:
```bash
python3 -m openreplay --debug
```

## Feature Requests

See [CONTRIBUTING.md](CONTRIBUTING.md) for contributing guidelines.
