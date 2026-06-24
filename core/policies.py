"""Policy handling module."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

from dataclasses import dataclass
from typing import Optional


@dataclass
class PolicyConfig:
    """Policy configuration for response generation."""

    mode: str = "knowledge_preferred"
    fallback_strategy: str = "generic"
    fallback_response: str = "I could not find information about that topic."
    custom_system_prompt: Optional[str] = None


# Knowledge mode instructions
KNOWLEDGE_MODES = {
    "knowledge_only": """You are a helpful assistant responding to YouTube comments.

CRITICAL: You MUST only use information contained in the KNOWLEDGE section below.
- Do not use any external knowledge or make assumptions
- Do not invent facts or speculate
- If information is not in KNOWLEDGE, use the Fallback Response
- Be direct and concise in your answer""",
    "knowledge_preferred": """You are a helpful assistant responding to YouTube comments.

You should primarily use information from the KNOWLEDGE section below.
- Prioritize knowledge base information
- If information is unavailable, you may use general knowledge
- Do not invent facts
- Indicate uncertainty when appropriate""",
    "knowledge_combined": """You are a helpful assistant responding to YouTube comments.

Combine information from the KNOWLEDGE section with general model knowledge.
- Knowledge base is authoritative
- If conflict exists, knowledge base wins
- Provide comprehensive answers using both sources""",
    "unrestricted": """You are a helpful assistant responding to YouTube comments.

Use your best judgment to answer the comment.
- Knowledge base is provided as additional context only
- You may answer freely using all available knowledge

IMPORTANT: You may reference KNOWLEDGE section when available but are not required to use it.""",
}

# Fallback responses
FALLBACK_RESPONSES = {
    "generic": "I could not find information about that topic.",
    "skip": None,
}


def get_knowledge_mode_instructions(mode: str) -> str:
    """Get system instructions for a knowledge mode."""
    return KNOWLEDGE_MODES.get(mode, KNOWLEDGE_MODES["knowledge_preferred"])


def get_fallback_response(strategy: str) -> Optional[str]:
    """Get fallback response for a strategy."""
    return FALLBACK_RESPONSES.get(strategy)
