# Configuration Guide

This guide explains all configuration options for OpenReplay.

## Basic Configuration

Create a `config.yaml` file in the project root:

```yaml
provider: youtube
youtube:
  video_id: YOUR_VIDEO_ID

llm:
  base_url: http://localhost:11434/v1
  api_key: dummy
  model: qwen3

policy:
  mode: knowledge_preferred

generation:
  style: friendly
```

## Provider Configuration

### Provider (Optional)

Specifies which provider to use.

```yaml
provider: youtube
```

**Available Providers:**
- `youtube` - YouTube comment management

## YouTube Configuration

### video_id (Required)

The YouTube video ID to manage comments for.

```yaml
youtube:
  video_id: dQw4w9WgXcQ  # Example: Rick Astley - Never Gonna Give You Up
```

** How to Find Your Video ID:**
- In YouTube URL: `https://www.youtube.com/watch?v=VIDEO_ID`
- The video ID is the string after `v=`

## LLM Configuration

### base_url (Optional)

The base URL for your LLM API endpoint.

```yaml
llm:
  base_url: http://localhost:11434/v1
```

**Common Endpoints:**
- Local Ollama: `http://localhost:11434/v1`
- OpenAI: `https://api.openai.com/v1`
- Other OpenAI-compatible APIs

### api_key (Optional)

API key for your LLM provider.

```yaml
llm:
  api_key: your_api_key_here
```

**Note:** For local Ollama, you can use any dummy value.

### model (Optional)

The LLM model name to use.

```yaml
llm:
  model: qwen3
```

**Common Models:**
- `qwen3` - Qwen 3 (local)
- `gpt-4` - OpenAI GPT-4
- `gpt-3.5-turbo` - OpenAI GPT-3.5
- `mistral` - Mistral AI

## Policy Configuration

### mode (Optional)

Controls how knowledge base is used.

```yaml
policy:
  mode: knowledge_preferred
```

**Available Modes:**

| Mode | Description |
|------|-------------|
| `knowledge_preferred` | Use knowledge base if available, fallback to general |
| `knowledge_only` | Only use knowledge base, no fallback |
| `fallback_only` | Skip knowledge base, use fallback |
| `general` | No knowledge base, use default behavior |

## Generation Configuration

### style (Optional)

Controls the tone of AI-generated responses.

```yaml
generation:
  style: friendly
```

**Available Styles:**

| Style | Description |
|-------|-------------|
| `friendly` | Warm, approachable tone |
| `professional` | Formal, business tone |
| `enthusiastic` | Energetic, excited tone |
| `neutral` | Balanced, objective tone |

## Full Example Configuration

```yaml
# Provider selection
provider: youtube

# YouTube settings
youtube:
  video_id: dQw4w9WgXcQ

# LLM settings
llm:
  base_url: http://localhost:11434/v1
  api_key: dummy
  model: qwen3

# Knowledge behavior
policy:
  mode: knowledge_preferred

# Response tone
generation:
  style: friendly
```

## Environment Variables

You can also set OAuth credentials via environment variables:

```bash
export GOOGLE_OAUTH_CLIENT_ID="your_client_id"
export GOOGLE_OAUTH_CLIENT_SECRET="your_client_secret"
```

Or create a `.env` file in the project root:

```
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
```

Using `.env` is recommended for local development and simplifies authentication without needing to specify `--client-secret` flag.

## Configuration Validation

OpenReplay validates configuration on startup:
- Missing required fields show helpful error messages
- Invalid URLs are detected
- Unknown modes/styles show available options
