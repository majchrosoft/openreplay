"""Knowledge base loading and management."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

import os
from typing import List, Tuple


class KnowledgeBase:
    """Manages knowledge base content from Q&A files."""

    def __init__(self):
        """Initialize knowledge base."""
        self.qa_pairs: List[Tuple[str, str]] = []
        self.fallback_text: str = ""

    def load_from_file(self, filepath: str) -> bool:
        """Load knowledge base from markdown file."""
        if not os.path.exists(filepath):
            self.qa_pairs = []
            self.fallback_text = ""
            return False

        with open(filepath, "r") as f:
            content = f.read()

        return self.load_from_text(content)

    def load_from_text(self, text: str) -> bool:
        """Load knowledge base from text content."""
        lines = text.strip().split("\n")
        current_question = None
        current_answer = []

        for line in lines:
            line = line.strip()
            if not line:
                if current_question and current_answer:
                    self.qa_pairs.append(
                        (current_question, " ".join(current_answer))
                    )
                    current_question = None
                    current_answer = []
                continue

            if line.startswith("Q:") or line.startswith("Question:"):
                if current_question and current_answer:
                    self.qa_pairs.append(
                        (current_question, " ".join(current_answer))
                    )
                current_question = line[2:].strip()
                current_answer = []
            elif line.startswith("A:") or line.startswith("Answer:"):
                current_answer.append(line[2:].strip())
            elif current_question is not None:
                current_answer.append(line)

        if current_question and current_answer:
            self.qa_pairs.append((current_question, " ".join(current_answer)))

        return True

    def get_all_content(self) -> str:
        """Return all knowledge base content as formatted string."""
        if not self.qa_pairs:
            return self.fallback_text

        parts = []
        for question, answer in self.qa_pairs:
            parts.append(f"Q: {question}\nA: {answer}")
        return "\n\n".join(parts)

    def get_qa_pairs(self) -> List[Tuple[str, str]]:
        """Return all question-answer pairs."""
        return self.qa_pairs.copy()

    def add_fallback_text(self, text: str) -> None:
        """Add fallback text for non-Q&A content."""
        self.fallback_text = text.strip()

    def find_relevant(self, query: str, threshold: float = 0.0) -> List[Tuple[str, str, float]]:
        """Find relevant QA pairs for a query (placeholder for future embedding-based search)."""
        query_lower = query.lower()
        results = []

        for question, answer in self.qa_pairs:
            question_lower = question.lower()
            if query_lower in question_lower or question_lower in query_lower:
                score = 1.0
                results.append((question, answer, score))

        return results


knowledge_base = KnowledgeBase()
