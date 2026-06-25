# OpenReplay

Self-hosted AI-powered community management platform for YouTube.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

⚠️ **ALPHA STATUS - USE WITH CAUTION**

This project is in active development and **must be used with caution**. The author takes **no responsibility** for any issues, data loss, or unintended behavior that may result from using this software. **Run on your own responsibility.**

**Known limitations:**
- Code was prepared via vibe coding technique
- OAuth authentication uses localhost callback (requires local environment)
- LLM integration requires local Ollama or compatible API

## Overview

OpenReplay automates YouTube community management using AI. It fetches comments from your videos, generates intelligent AI-powered responses using your own knowledge base, and can automatically publish them.

**Key Features:**
- 🤖 AI-powered comment responses
- 📚 Custom knowledge base integration
- 🔄 OAuth2 authentication
- 📊 Command-line interface
- 🧪 End-to-end testing

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- YouTube API credentials (OAuth2)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/majchrosoft/openreplay.git
cd openreplay
```

2. Install dependencies:

```bash
pip install -e .
```

3. Create configuration file:

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` with your settings.

4. Set up environment variables (optional, replaces client_secret.json):

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your Google OAuth credentials:

```
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
```

You can still use `client_secret.json` instead by passing `--client-secret` flag.

## Configuration

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

### Setting Your Video ID

To fetch comments from a specific YouTube video, you need to set `youtube.video_id` in your configuration.

**Option 1: Interactive Selection (Recommended)**

Use the `select` command to fetch and choose from your YouTube videos:

```bash
openreplay select
```

This command will:
- List all your uploaded videos with titles and comment counts
- Let you select a video by number
- Automatically update your configuration

**Option 2: Manual Configuration**

Manually edit `config.yaml` and set the video ID:

```yaml
youtube:
  video_id: dQw4w9WgXcQ
```

You can find the video ID in the YouTube URL (e.g., `https://youtube.com/watch?v=dQw4w9WgXcQ`).

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `provider` | Provider name (youtube) | `youtube` |
| `youtube.video_id` | Target YouTube video ID | `null` |
| `llm.base_url` | LLM API endpoint | `http://localhost:11434/v1` |
| `llm.api_key` | LLM API key | `dummy` |
| `llm.model` | LLM model name | `qwen3` |
| `policy.mode` | Knowledge policy mode | `knowledge_preferred` |
| `generation.style` | Response style | `friendly` |

## Usage

### Authentication

First, authenticate with YouTube:

```bash
openreplay auth --client-secret path/to/client_secret.json
```

Or use environment variables in `.env`:

```
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
```

This will open a browser window for OAuth2 authentication and store tokens in `tokens/youtube.json`.

### Fetch and Select Video

List and select a video from your channel:

```bash
openreplay select
```

This will display all your uploaded videos and let you choose one. The selected video ID will be saved to `config.yaml`.

### Fetch Comments

Fetch comments from your configured video:

```bash
openreplay fetch
```

Comments are saved to `workspace/comments.json`.

#### Getting OAuth Credentials

**Option 1: Using client_secret.json**

The `client_secret.json` file is obtained from **Google Cloud Console**:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable **YouTube Data API v3** (APIs & Services → Library)
4. Create OAuth credentials (APIs & Services → Credentials → Create Credentials → OAuth client ID)
5. Set application type to **"Desktop app"**
6. Download the JSON file and save as `client_secret.json`

**Option 2: Using .env file**

Create `.env` file in project root with:

```
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
```

For detailed instructions, see `examples/client_secret.example.json`.

### Generate Replies

Generate AI responses:

```bash
openreplay generate [--knowledge-file knowledge.md] [--output workspace/replies.json]
```

Replies are saved to `workspace/replies.json`.

### Publish Replies

Publish to YouTube:

```bash
openreplay publish [--replies-file workspace/replies.json] [--dry-run]
```

Use `--dry-run` to preview without actually publishing.

## Commands

```bash
openreplay --help

Commands:
  auth      Authenticate with YouTube
  fetch     Fetch YouTube comments
  select    Fetch and select YouTube videos
  generate  Generate AI responses
  publish   Publish generated responses
```

## Knowledge Base

Edit `knowledge.md` to provide context for AI responses:

```markdown
# Knowledge Base

Q: How does this work?
A: This works by following a simple process. First, you configure the settings, then process the data, and finally review the results.

Q: Is this available internationally?
A: Yes, this service is available worldwide.
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     OpenReplay CLI                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Auth      │  │   Fetch     │  │  Generate   │          │
│  │  Command    │  │  Command    │  │  Command    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                        │                                      │
│  ┌─────────────┐       ▼        ┌─────────────┐              │
│  │  Publish    │◄─────Comment    │  LLM        │              │
│  │  Command    │       Data       │  Generator  │              │
│  └─────────────┘                  └─────────────┘              │
│                        │                                      │
│  ┌─────────────┐       ▼        ┌─────────────┐              │
│  │  YouTube    │◄──────Replies───►│  Knowledge  │              │
│  │  Provider   │                  │  Base       │              │
│  └─────────────┘                  └─────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

## Testing

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test file
python3 -m pytest tests/test_generate.py
```

## Project Status

**Current Status:** Alpha

**Implemented:**
- ✅ Project structure
- ✅ Configuration management
- ✅ Knowledge base loading
- ✅ Policy and prompt system
- ✅ LLM integration
- ✅ YouTube provider (OAuth, fetch, publish)
- ✅ CLI commands (auth, fetch, select, generate, publish)
- ✅ Unit and integration tests
- ✅ End-to-end flow tests

**Planned:**
- ⏳ CI/CD pipeline
- ⏳ Comprehensive documentation
- ⏳ Example files
- ⏳ CHANGELOG
- ⏳ GitHub repository setup

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Acknowledgments

- Uses [Google OAuth2](https://developers.google.com/identity/protocols/oauth2)
- LLM integration compatible with OpenAI-compatible APIs
