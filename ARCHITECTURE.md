# Architecture Guide

Understanding OpenReplay's system architecture.

## Overview

OpenReplay follows a modular architecture designed for extensibility and maintainability.

```
OpenReplay Architecture
┌─────────────────────────────────────────────────────────────┐
│                    OpenReplay CLI                           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │  auth   │  │  fetch  │  │generate │  │publish  │        │
│  │ command │  │ command │  │ command │  │ command │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
│        │            │            │            │              │
│        └────────────┴────────────┴────────────┘              │
│                           │                                  │
│                  ┌────────▼────────┐                         │
│                  │   core/         │                         │
│                  │  - prompts      │                         │
│                  │  - policies     │                         │
│                  └────────┬────────┘                         │
│                           │                                  │
│        ┌──────────────────┴──────────────────┐              │
│        │             providers/              │              │
│        │  - youtube (OAuth, API, fetch, etc) │              │
│        └──────────────────┬──────────────────┘              │
│                           │                                  │
│        ┌──────────────────┴──────────────────┐              │
│        │           openreplay/               │              │
│        │  - config  - knowledge  - template  │              │
│        └──────────────────┬──────────────────┘              │
│                           │                                  │
│        ┌──────────────────┴──────────────────┐              │
│        │         llm/                        │              │
│        │      - generator (API calls)        │              │
│        └─────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┴────────────────┐
          │    external services            │
          │  - YouTube API                  │
          │  - LLM (Ollama/OpenAI, etc)     │
          └─────────────────────────────────┘
```

## Modules

### Command Module (`commands/`)

CLI command implementations.

**Files:**
- `auth.py` - Authentication command
- `fetch.py` - Comment fetching command
- `generate.py` - AI reply generation command
- `publish.py` - Reply publishing command

**Function:**
- Parse CLI arguments
- Coordinate between components
- Handle user interaction

**Example:**
```python
def run(args):
    """Execute auth command."""
    provider = YouTubeProvider()
    tokens = provider.authenticate()
```

### Core Module (`core/`)

Core logic and configuration.

**Files:**
- `prompts.py` - Prompt building for LLM
- `policies.py` - Knowledge policy handling

**Function:**
- Build prompts with context
- Handle knowledge base modes
- Manage fallback strategies

**Example:**
```python
def build_prompt(comment, knowledge, mode, style):
    """Build prompt for LLM."""
    system = f"You are a {style} assistant..."
```

### LLM Module (`llm/`)

LLM integration layer.

**Files:**
- `generator.py` - API calls to LLM

**Function:**
- Connect to OpenAI-compatible APIs
- Handle API keys
- Return AI responses

**Example:**
```python
def generate_response(prompt, system_message):
    """Call LLM and return response."""
    response = requests.post(...)
    return response.json()["choices"][0]["message"]["content"]
```

### Provider Module (`providers/`)

Provider implementations (YouTube, future platforms).

**Files:**
- `base.py` - Provider interface
- `youtube.py` - YouTube implementation

**Function:**
- OAuth2 authentication
- API calls to external services
- Data extraction/unification

**Example:**
```python
class YouTubeProvider(Provider):
    def list_comments(self, video_id):
        """Fetch comments from YouTube."""
```

### OpenReplay Module (`openreplay/`)

Core application logic.

**Files:**
- `config.py` - Configuration management
- `knowledge.py` - Knowledge base loading
- `template.py` - Response template handling
- `__main__.py` - CLI entry point

**Function:**
- Load configuration from YAML
- Parse knowledge base Q&A
- Apply response templates

**Example:**
```python
config = Config()
video_id = config.video_id
```

## Data Flow

### Comment Processing Pipeline

```
1. User runs: openreplay fetch
      │
      ▼
2. Load config (video_id)
      │
      ▼
3. Authenticate with YouTube
      │
      ▼
4. Call YouTube API: commentThreads.list
      │
      ▼
5. Parse response into Comment objects
      │
      ▼
6. Save to workspace/comments.json
```

```
1. User runs: openreplay generate
      │
      ▼
2. Load comments from JSON
      │
      ▼
3. Load knowledge base from markdown
      │
      ▼
4. For each comment:
   │
   ├─ Build prompt (system + knowledge + comment)
   │
   ├─ Call LLM API
   │
   ├─ Parse response
   │
   ├─ Apply template
   │
   └─ Store reply
      │
      ▼
5. Save to workspace/replies.json
```

```
1. User runs: openreplay publish
      │
      ▼
2. Load replies from JSON
      │
      ▼
3. For each reply:
   │
   ├─ Authenticate with YouTube
   │
   ├─ Call YouTube API: comments.insert
   │
   ├─ Store reply ID
   │
   └─ Track status
      │
      ▼
5. Save to workspace/published.json
```

## Configuration Management

### Config Class

Single source of truth for configuration.

**Features:**
- YAML loading
- Default values
- Dot notation access
- Deep merging

**Usage:**
```python
from openreplay.config import config

# Access values
video_id = config.video_id
model = config.llm_model
mode = config.policy_mode
```

### Configuration Sources

1. `config.yaml` - User configuration
2. Environment variables - Provider credentials
3. Defaults - Hardcoded fallbacks

## Policy System

### Knowledge Modes

| Mode | Behavior |
|------|-- ------|
| `knowledge_preferred` | Use knowledge if available, fallback otherwise |
| `knowledge_only` | Use only knowledge base |
| `fallback_only` | Skip knowledge, use generic fallback |
| `general` | No knowledge, default behavior |

### Fallback Strategies

| Strategy | Response |
|---------|----------|
| `generic` | Generic helpful response |
| `personalized` | Personalized based on knowledge patterns |
| `no_response` | Don't respond |

## Provider Interface

All providers must implement:

```python
class Provider(ABC):
    @abstractmethod
    def authenticate(self) -> dict:
        """Execute OAuth2 flow and return credentials."""
    
    @abstractmethod
    def list_resources(self) -> List[Video]:
        """List available resources (videos)."""
    
    @abstractmethod
    def list_comments(self, resource_id) -> List[Comment]:
        """Fetch comments for a specific resource."""
    
    @abstractmethod
    def publish_reply(self, comment_id, reply_content) -> dict:
        """Publish a reply to a specific comment."""
    
    @abstractmethod
    def get_user_info(self) -> dict:
        """Get authenticated user information."""
```

## Testing Architecture

### Unit Tests

Test individual components in isolation.

```python
def test_build_prompt():
    prompt = build_prompt("Test", "Knowledge", "mode", "style")
    assert "Test" in prompt
    assert "Knowledge" in prompt
```

### Integration Tests

Test component interactions.

```python
@patch("llm.generator.requests.post")
def test_generate_replies_with_mock(mock_post):
    # Test complete generate flow with mocked LLM
```

### End-to-End Tests

Test complete users workflows.

```python
def test_fetch_command():
    # Test full fetch workflow
    # Verify file output

def test_generate_command():
    # Test full generate workflow
    # Verify prompts, LLM calls, file output
```

## Extensibility

### Adding New Provider

1. Create `providers/newprovider.py`
2. Implement `Provider` abstract methods
3. Add command in `commands/`
4. Register in `__main__.py`

### Adding New Knowledge Mode

1. Update `core/policies.py`
2. Add mode to policy mode list
3. Update documentation

### Adding New Response Style

1. Update prompt templates in `core/prompts.py`
2. Update USAGE.md documentation

## Security Considerations

- Tokens stored locally (tokens/youtube.json)
- Config may contain API keys (use .gitignore)
- OAuth2 for YouTube authentication
- No secrets logged

## Performance Considerations

- paginate through API results
- token caching and refresh
- batch processing (future)
- async I/O (future)
