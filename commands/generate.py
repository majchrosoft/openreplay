"""Generate command implementation."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from openreplay.config import config
from openreplay.knowledge import knowledge_base
from openreplay.template import template
from llm.generator import generator as llm_generator
from core.prompts import build_prompt


class Reply:
    """Represents a generated reply."""

    def __init__(
        self,
        comment_id: str,
        original_comment: str,
        generated_content: str,
        final_reply: str,
        knowledge_mode: str,
        style: str,
        timestamp: Optional[datetime] = None,
        status: str = "generated",
        error: Optional[str] = None,
    ):
        self.comment_id = comment_id
        self.original_comment = original_comment
        self.generated_content = generated_content
        self.final_reply = final_reply
        self.knowledge_mode = knowledge_mode
        self.style = style
        self.timestamp = timestamp or datetime.now()
        self.status = status
        self.error = error

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "comment_id": self.comment_id,
            "original_comment": self.original_comment,
            "generated_content": self.generated_content,
            "final_reply": self.final_reply,
            "knowledge_mode": self.knowledge_mode,
            "style": self.style,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "error": self.error,
        }


def load_comments(filepath: str = "workspace/comments.json") -> list:
    """Load comments from JSON file."""
    path = Path(filepath)
    if not path.exists():
        return []

    with open(path, "r") as f:
        data = json.load(f)
        return data.get("comments", [])


def save_replies(
    replies: list[Reply], filepath: str = "workspace/replies.json"
) -> None:
    """Save replies to JSON file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "replies": [reply.to_dict() for reply in replies],
        "generated_at": datetime.now().isoformat(),
    }

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def generate_replies(
    comments: Optional[list] = None,
    knowledge_file: str = "knowledge.md",
    output_file: str = "workspace/replies.json",
) -> list[Reply]:
    """Generate AI replies for all comments.

    Args:
        comments: List of comment dicts. If None, loads from file.
        knowledge_file: Path to knowledge base file.
        output_file: Path to save replies.

    Returns:
        List of generated Reply objects.
    """
    if comments is None:
        comments = load_comments()

    # Load knowledge base
    knowledge_base.load_from_file(knowledge_file)

    replies = []

    for comment in comments:
        comment_id = comment.get("id", "unknown")
        comment_text = comment.get("content", "")

        try:
            # Build prompt
            system_prompt = build_prompt(
                comment_text,
                knowledge_base.get_all_content(),
                config.policy_mode,
                config.generation_style,
            )

            # Get just the system part for LLM call
            system_parts = system_prompt.split("KNOWLEDGE")[0].strip()

            # Generate response
            generated_content = llm_generator.generate_response(comment_text, system_parts)

            # Apply template
            final_reply = template.apply(generated_content)

            reply = Reply(
                comment_id=comment_id,
                original_comment=comment_text,
                generated_content=generated_content,
                final_reply=final_reply,
                knowledge_mode=config.policy_mode,
                style=config.generation_style,
            )
        except Exception as e:
            reply = Reply(
                comment_id=comment_id,
                original_comment=comment_text,
                generated_content="",
                final_reply="",
                knowledge_mode=config.policy_mode,
                style=config.generation_style,
                status="failed",
                error=str(e),
            )

        replies.append(reply)

    # Save replies
    save_replies(replies, output_file)

    return replies


def run(args):
    """Execute generate command."""
    print("Loading comments...")
    comments = load_comments()
    print(f"Found {len(comments)} comments")

    if not comments:
        print("No comments to process. Run 'openreplay fetch' first.")
        return

    print(f"Generating AI responses using {config.llm_model}...")
    print(f"Knowledge mode: {config.policy_mode}")
    print(f"Response style: {config.generation_style}")

    knowledge_file = getattr(args, "knowledge_file", "knowledge.md")
    output_file = getattr(args, "output", "workspace/replies.json")

    try:
        replies = generate_replies(
            comments=comments,
            knowledge_file=knowledge_file,
            output_file=output_file,
        )
        successful = sum(1 for r in replies if r.status == "generated")
        failed = sum(1 for r in replies if r.status == "failed")

        print(f"\nGenerated {successful} responses")
        if failed > 0:
            print(f"Failed: {failed}")
    except Exception as e:
        print(f"Error during generation: {e}")
        raise
