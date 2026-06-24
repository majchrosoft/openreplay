# OpenReplay POC - Planning Document

## Objective

Build the smallest possible Proof of Concept (POC) for OpenReplay.

The purpose of this phase is to validate:

* YouTube OAuth2 integration
* Comment retrieval
* LLM-based reply generation
* Knowledge-based response control
* Reply publishing

This phase is intentionally focused on functionality rather than user experience.

No web application should be built at this stage.

No database should be introduced.

No frontend framework should be used.

No user management should exist.

No multi-user support should exist.

The entire system should operate as a local command-line application.

---

# Vision

OpenReplay is a self-hosted AI-powered community management tool.

Users connect a social platform account, provide knowledge sources, configure AI behavior, generate replies, review them, and optionally publish them.

The long-term vision includes:

* multiple social media providers
* multiple knowledge sources
* RAG
* approval workflows
* web interface
* automation

However, none of these features are required for the POC.

---

# POC Scope

The POC must prove that the core workflow works end-to-end.

Workflow:

```text
Authenticate
    ↓
Fetch comments
    ↓
Generate replies
    ↓
Review replies
    ↓
Publish replies
```

Only YouTube is supported.

Only a local LLM endpoint is required.

Only local files are used for configuration and storage.

---

# Technical Requirements

## Language

Python

Reasoning:

* Native ecosystem for AI development.
* Easy future integration with:

  * LiteLLM
  * LangGraph
  * LlamaIndex
  * Haystack
  * MCP
  * local models

---

## Architecture

The application should be implemented as a CLI application.

No web UI.

No REST API.

No database.

No Docker requirement for the first iteration.

Simple local execution:

```bash
python main.py
```

or

```bash
openreplay <command>
```

---

# Project Structure

```text
openreplay/

config.yaml

knowledge.md

response_template.txt

workspace/

providers/
    youtube.py

llm/
    generator.py

core/
    policies.py
    prompts.py

commands/
    auth.py
    fetch.py
    generate.py
    publish.py

tokens/
```

---

# Commands

## Authentication

```bash
openreplay auth
```

Responsibilities:

* Execute OAuth2 flow.
* Open browser.
* Authenticate user.
* Obtain access token.
* Obtain refresh token.
* Store credentials locally.

Output:

```text
tokens/youtube.json
```

---

## Fetch Comments

```bash
openreplay fetch
```

Responsibilities:

* Read configuration.
* Connect to YouTube.
* Retrieve comments.
* Store comments locally.

Output:

```text
workspace/comments.json
```

---

## Generate Replies

```bash
openreplay generate
```

Responsibilities:

* Load comments.
* Load knowledge base.
* Build prompts.
* Generate responses using configured LLM.
* Apply selected policy.
* Apply response template.
* Save generated replies.

Output:

```text
workspace/replies.json
```

---

## Publish Replies

```bash
openreplay publish
```

Responsibilities:

* Load generated replies.
* Publish replies using YouTube API.
* Mark successful publications.

Output:

```text
workspace/published.json
```

---

# Configuration

## config.yaml

Example:

```yaml
provider: youtube

youtube:
  video_id: VIDEO_ID

llm:
  base_url: http://localhost:11434/v1
  api_key: dummy
  model: qwen3

policy:
  mode: knowledge_preferred

fallback:
  strategy: generic

generation:
  style: friendly
```

The application must be fully configurable through this file.

No hardcoded values.

---

# Knowledge Base

## knowledge.md

The user provides domain knowledge.

Example:

```markdown
Q: How long is shipping?

A: Shipping takes 2-3 business days.

Q: Do you ship internationally?

A: Yes.
```

This file becomes the primary context supplied to the LLM.

---

# Response Template

## response_template.txt

Example:

```text
${content}

[AI enhanced]

This response was generated with AI assistance.
```

The system replaces:

```text
${content}
```

with generated content.

---

# Knowledge Modes

The POC must support all modes from the beginning because they are one of the project's core differentiators.

---

## Knowledge Only

Rules:

* AI may only use information contained in the knowledge base.
* No external knowledge.
* No assumptions.
* No speculation.

If answer cannot be found:

Use configured fallback strategy.

---

## Knowledge Preferred

Rules:

* Knowledge base is preferred.
* General model knowledge may be used if necessary.
* AI should avoid inventing facts.

---

## Knowledge + World Knowledge

Rules:

* Combine knowledge base and model knowledge.
* Knowledge base remains authoritative.
* If conflict exists, knowledge base wins.

---

## Unrestricted

Rules:

* AI may answer freely.
* Knowledge base is treated as additional context.
* Maximum flexibility.

---

# Fallback Strategies

When information is unavailable:

---

## Generic Response

Example:

```text
I could not find information about that topic.
```

---

## Skip

No reply generated.

---

## Flag

Mark comment for manual review.

---

# Generation Pipeline

For every comment:

1. Load comment.
2. Load knowledge base.
3. Build prompt.
4. Apply selected knowledge mode.
5. Send request to LLM.
6. Receive response.
7. Apply template.
8. Save result.

No publishing occurs during generation.

Generation and publishing are separate steps.

---

# Prompt Builder

Prompt construction must be modular.

Structure:

```text
SYSTEM

Behavior instructions.

KNOWLEDGE

Knowledge base.

COMMENT

User comment.
```

Knowledge mode determines which instructions are inserted into the SYSTEM section.

---

# Provider Abstraction

Even though only YouTube is implemented, architecture should support future providers.

Define provider contract:

```python
class Provider:
    authenticate()
    fetch_comments()
    publish_reply()
```

Future providers:

* Reddit
* LinkedIn
* Facebook
* Instagram
* X

must be able to reuse the same workflow.

---

# Success Criteria

The POC is considered successful when:

1. User authenticates with YouTube.
2. Comments can be fetched.
3. Knowledge base can be loaded.
4. LLM generates replies.
5. Different knowledge modes produce different behaviors.
6. Replies are stored locally.
7. Replies can be published through YouTube API.
8. Entire workflow works from the command line.

No web interface is required.

No database is required.

No advanced AI framework is required.

The objective is validation of the core concept, not production readiness.
