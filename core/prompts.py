"""Prompt building module for LLM API calls."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

from typing import Optional

from core.policies import get_knowledge_mode_instructions


def build_system_prompt(mode: str, style: str, custom_prompt: Optional[str] = None) -> str:
    """Build the system prompt based on mode and style."""
    system = get_knowledge_mode_instructions(mode)

    if custom_prompt:
        system += f"\n\nCUSTOM INSTRUCTIONS:\n{custom_prompt}"

    style_instructions = _get_style_instructions(style)
    if style_instructions:
        system += f"\n\n{style_instructions}"

    return system


def _get_style_instructions(style: str) -> str:
    """Get style-specific instructions."""
    styles = {
        "professional": """Respond in a professional, formal business tone.
Maintain authority and expertise in your responses.""",
        "friendly": """Respond in a friendly, conversational tone.
Be approachable and use a warm, engaging style.""",
        "expert": """Respond in a technical, authoritative manner.
Use precise language and demonstrate deep knowledge.""",
        "marketing": """Respond in a promotional and engaging style.
Focus on benefits, use persuasive language, and encourage action.""",
        "custom": """Use appropriate style based on context.""",
    }
    return styles.get(style, styles["custom"])


def build_prompt(
    comment: str,
    knowledge: str,
    mode: str,
    style: str,
    custom_prompt: Optional[str] = None,
) -> str:
    """Build a complete prompt for the LLM.

    Prompt structure:
    SYSTEM
    Behavior instructions based on mode and style

    KNOWLEDGE
    Knowledge base content

    COMMENT
    Original user comment
    """
    system = build_system_prompt(mode, style, custom_prompt)
    system += """

IMPORTANT: Format your response as plain text only.
Do not use markdown formatting.
Keep the response concise and directly address the comment."""

    knowledge_block = f"""KNOWLEDGE

{knowledge}

IMPORTANT: Follow the rules from SYSTEM based on your knowledge mode."""
    if not knowledge.strip():
        knowledge_block = """KNOWLEDGE

No knowledge base provided."""

    user_prompt = f"""COMMENT

User comment: "{comment}"

Please generate a response."""

    return f"{system}\n\n{knowledge_block}\n\n{user_prompt}"
