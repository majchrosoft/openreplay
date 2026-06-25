# Troubleshooting Guide

## Common Issues

### Issue: "Connection refused" when generating AI responses

**Error:** `ConnectionRefusedError: [Errno 61] Connection refused` on port 11434

**Cause:** Ollama LLM server is not running. The `generate` command requires a local LLM server accessible at `http://localhost:11434`.

**Solution:**

1. **Install and start Ollama:**
   ```bash
   # macOS
   brew install ollama
   ollama serve
   
   # Or download from https://ollama.com/download
   ```

2. **Pull the required model:**
   ```bash
   # The config uses qwen3 by default
   ollama pull qwen3
   ```

3. **Verify Ollama is running:**
   ```bash
   curl http://localhost:11434/
   # Should return: Ollama is running
   ```

4. **Test the model:**
   ```bash
   ollama run qwen3
   > Hello
   # Should respond to your message
   ```

**Alternative: Use a different LLM provider**

Edit `config.yaml` to use a different LLM endpoint:

```yaml
llm:
  base_url: http://your-llm-api.com/v1
  api_key: your-api-key
  model: your-model-name
```

---

### Issue: "No filter selected" when listing videos

**Error:** `400 Client Error: Bad Request - No filter selected. Expected one of: myRating, id, chart`

**Cause:** The YouTube API `videos.list` endpoint requires specific filter parameters.

**Solution:** Already fixed in latest version. The code now uses `playlistItems.list` endpoint with the uploads playlist ID instead.

---

### Issue: "Invalid request" during YouTube authentication

**Error:** `400 invalid_request` or "The out-of-band (OOB) flow has been blocked"

**Cause:** The old OAuth implementation used the deprecated OOB (out-of-band) flow.

**Solution:** Already fixed in latest version. The code now uses `google-auth-oauthlib`'s `InstalledAppFlow.run_local_server()` which implements the modern localhost redirect flow.

---

### Issue: "No comments to process"

**Error:** "No comments to process. Run 'openreplay fetch' first."

**Cause:** Comments haven't been fetched yet.

**Solution:**
```bash
# First authenticate
openreplay auth

# Select a video
openreplay select

# Fetch comments
openreplay fetch

# Then generate responses
openreplay generate
```

---

### Issue: "LLM API error" with timeout or other errors

**Possible Causes:**
1. LLM server is slow or unresponsive
2. Model is large and takes time to load
3. API key is missing or invalid
4. Model doesn't support the API format

**Solutions:**

1. **Increase timeout in config:**
   ```yaml
   llm:
     timeout: 60  # Default is 30 seconds
   ```

2. **Use a smaller/faster model:**
   ```yaml
   llm:
     model: qwen2.5:0.5b  # Very fast, low quality
   ```

3. **Check LLM server logs:**
   ```bash
   # For Ollama
   ollama logs
   ```

4. **Test with curl:**
   ```bash
   curl http://localhost:11434/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "qwen3",
       "messages": [{"role": "user", "content": "Hello"}],
       "temperature": 0.7
     }'
   ```

---

## Debug Mode

Run commands with verbose logging:

```bash
# For generate command
python3 -m commands.generate --knowledge-file knowledge.md --output workspace/replies.json
```

---

## Verification Checklist

- [ ] Ollama is running: `curl http://localhost:11434/`
- [ ] Model is installed: `ollama list`
- [ ] YouTube authenticated: `tokens/youtube.json` exists
- [ ] Video selected: `config.yaml` has `youtube.video_id`
- [ ] Comments fetched: `workspace/comments.json` exists with comments
- [ ] Knowledge base exists: `knowledge.md` exists (or edit config to use empty knowledge)
