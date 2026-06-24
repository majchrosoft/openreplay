# OpenReplay

## Vision

OpenReplay is a self-hosted AI-powered community management platform.

The goal is to help content creators and businesses answer comments on social media platforms using Large Language Models (LLMs) while maintaining control over:

* knowledge sources
* response policies
* hallucination levels
* approval workflow
* publishing permissions

The platform must support any OpenAI-compatible LLM endpoint, including:

* OpenAI
* OpenRouter
* Ollama
* LM Studio
* LocalAI
* vLLM
* custom OpenAI-compatible servers

The first supported provider will be YouTube.

---

# Core Use Case

A user wants to answer comments under a YouTube video.

The user:

1. Connects a YouTube account via OAuth2.
2. Selects a video.
3. Loads comments.
4. Provides a knowledge base (FAQ).
5. Configures response policies.
6. Generates AI responses.
7. Reviews generated responses.
8. Publishes selected responses.

---

# Product Principles

## Human In Control

AI must never publish responses automatically by default.

Default workflow:

Load → Generate → Review → Publish

---

## Bring Your Own LLM

OpenReplay does not provide models.

Users configure:

* endpoint URL
* API key
* model name

Example:

```env
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=dummy
LLM_MODEL=qwen3:latest
```

---

## Knowledge First

Responses should prioritize user-provided information whenever possible.

Knowledge sources become the primary source of truth.

---

## Provider Agnostic Architecture

The platform must allow future providers:

* YouTube
* Reddit
* LinkedIn
* Facebook
* Instagram
* X

without major architectural changes.

---

# MVP Scope

Version 1 supports:

## Providers

* YouTube only

## Knowledge Sources

* FAQ textarea

## LLM

* OpenAI-compatible API

## Workflow

* Generate responses
* Preview responses
* Publish responses

No vector database.

No embeddings.

No PDF processing.

No automatic scheduling.

No auto-publishing.

---

# User Flow

## Step 1

Configure LLM.

Fields:

* Base URL
* API Key
* Model Name

Test Connection button.

---

## Step 2

Connect YouTube Account.

OAuth2 flow.

Store tokens securely.

---

## Step 3

Select Video.

Display:

* title
* published date
* comment count

---

## Step 4

Provide Knowledge Base.

Textarea:

```text
Frequently asked questions.

Product information.

Policies.

Business information.

Anything AI should know.
```

---

## Step 5

Configure Response Policy.

---

# Knowledge Modes

## Knowledge Only

AI may only use information contained in the provided knowledge base.

If information is missing:

Return configured fallback response.

Example:

"I could not find information about that topic."

No assumptions.

No external knowledge.

---

## Knowledge Preferred

AI should prioritize the knowledge base.

If information is unavailable:

AI may use general knowledge.

AI should indicate uncertainty where appropriate.

---

## Knowledge + World Knowledge

AI should combine:

* knowledge base
* general model knowledge

Knowledge base remains authoritative.

If conflicts occur:

Knowledge base wins.

---

## Unrestricted

AI may answer freely using all available knowledge.

Knowledge base is only additional context.

---

# Missing Information Policies

When AI cannot answer:

## Fallback Response

Example:

```text
I could not find information about that topic.
```

---

## Skip Comment

No response generated.

---

## Mark For Review

Flag comment for manual handling.

---

# Response Style

Supported styles:

## Professional

Formal business tone.

---

## Friendly

Friendly and conversational.

---

## Expert

Technical and authoritative.

---

## Marketing

Promotional and engagement-focused.

---

## Custom

User-defined system prompt.

---

# Response Template

Generated content is injected into a template.

Example:

```text
${content}

[AI enhanced]

This response was generated using AI assistance.
While every effort is made to ensure accuracy,
AI systems may occasionally make mistakes.
This response should not be considered legal,
medical, or financial advice.
```

`${content}` must be replaced with generated output.

---

# Generation Pipeline

For each comment:

1. Load comment.
2. Build prompt.
3. Send request to LLM.
4. Receive response.
5. Apply template.
6. Store draft.
7. Display preview.

---

# Prompt Construction

System Prompt:

Contains:

* behavior instructions
* selected mode
* style rules
* fallback policy

Knowledge Block:

Contains FAQ.

User Prompt:

Contains original comment.

Final prompt structure:

```text
SYSTEM

Behavior and policy instructions.

KNOWLEDGE

Knowledge base content.

COMMENT

Original user comment.
```

---

# Review Queue

Generated responses enter review state.

Statuses:

* Draft
* Approved
* Rejected
* Published

---

# Bulk Operations

Supported actions:

* Approve Selected
* Reject Selected
* Publish Selected
* Regenerate Selected

---

# Data Model

## Providers

```text
id
name
type
```

## Accounts

```text
id
provider_id
external_account_id
access_token
refresh_token
```

## Resources

Represents videos.

```text
id
provider_id
external_id
title
```

## Comments

```text
id
resource_id
external_id
author
content
```

## Knowledge Bases

```text
id
name
content
```

## Response Policies

```text
id
knowledge_mode
fallback_policy
style
custom_prompt
```

## Responses

```text
id
comment_id
content
status
published_at
```

---

# API Abstractions

Provider interface:

```php
ProviderInterface
```

Methods:

```php
authenticate()

listResources()

listComments()

publishReply()
```

All future providers must implement this contract.

---

# Security

Never expose:

* API keys
* OAuth tokens

Encrypt sensitive data.

Use least-privilege scopes.

---

# Future Roadmap

## Phase 2

Knowledge improvements:

* Markdown files
* PDF files
* Multiple knowledge sources

---

## Phase 3

RAG support:

* embeddings
* vector search
* chunk retrieval

---

## Phase 4

Additional providers:

* Reddit
* LinkedIn
* Facebook
* Instagram
* X

---

## Phase 5

Automation:

* scheduled processing
* inbox mode
* AI triage
* sentiment analysis

---

# Suggested Technology Stack

Backend:

* Laravel 12

Frontend:

* Livewire 4

Database:

* SQLite (default)
* MySQL/PostgreSQL (optional)

Authentication:

* Laravel Breeze

OAuth:

* Laravel Socialite

HTTP:

* Laravel HTTP Client

Queue:

* Laravel Queues

Deployment:

* Docker
* Docker Compose

---

# Definition of Done for MVP

A user can:

1. Configure an OpenAI-compatible LLM.
2. Connect a YouTube account.
3. Select a video.
4. Load comments.
5. Provide FAQ knowledge.
6. Generate AI responses.
7. Review generated responses.
8. Publish approved responses.

No manual database operations required.

Runs locally using a single Docker Compose command.

