"""Response template loading and application."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

import os
from typing import Optional


class ResponseTemplate:
    """Manages response templates for AI replies."""

    DEFAULT_TEMPLATE = """${content}

[AI enhanced]

This response was generated with AI assistance."""

    def __init__(self, template_path: str = "response_template.txt"):
        """Initialize template manager."""
        self.template_path = template_path
        self.template: str = self.DEFAULT_TEMPLATE
        self._load()

    def _load(self) -> None:
        """Load template from file or use default."""
        if not os.path.exists(self.template_path):
            return

        with open(self.template_path, "r") as f:
            content = f.read().strip()
            if content:
                self.template = content

    def apply(self, content: str) -> str:
        """Apply template to content by replacing ${content} placeholder."""
        return self.template.replace("${content}", content)

    def get_template(self) -> str:
        """Return the template string."""
        return self.template

    def has_placeholder(self) -> bool:
        """Check if template contains the required placeholder."""
        return "${content}" in self.template


template = ResponseTemplate()
