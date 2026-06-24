"""Prompts module tests."""

import unittest

from core.prompts import build_prompt, build_system_prompt


class TestPrompts(unittest.TestCase):
    """Test prompt building."""

    def test_build_system_prompt_basic(self):
        """Test basic system prompt construction."""
        prompt = build_system_prompt("knowledge_preferred", "friendly")
        self.assertIn("KNOWLEDGE", prompt)
        self.assertIn("friendly", prompt, "Style should be mentioned")

    def test_build_system_prompt_modes(self):
        """Test system prompt for different modes."""
        modes = ["knowledge_only", "knowledge_preferred", "knowledge_combined", "unrestricted"]
        for mode in modes:
            prompt = build_system_prompt(mode, "professional")
            self.assertIn("KNOWLEDGE", prompt)
            self.assertIsInstance(prompt, str)
            self.assertTrue(len(prompt) > 0)

    def test_build_system_prompt_styles(self):
        """Test system prompt for different styles."""
        styles = ["professional", "friendly", "expert", "marketing"]
        for style in styles:
            prompt = build_system_prompt("knowledge_preferred", style)
            self.assertIsInstance(prompt, str)
            self.assertTrue(len(prompt) > 0)

    def test_build_complete_prompt(self):
        """Test complete prompt construction."""
        comment = "What is your return policy?"
        knowledge = "Q: Return policy?\nA: 30 days."
        mode = "knowledge_only"
        style = "professional"

        prompt = build_prompt(comment, knowledge, mode, style)

        self.assertIn("KNOWLEDGE", prompt)
        self.assertIn("COMMENT", prompt)
        self.assertIn(comment, prompt)
        self.assertIn(knowledge, prompt)

    def test_build_prompt_empty_knowledge(self):
        """Test prompt with empty knowledge base."""
        comment = "Test comment"
        prompt = build_prompt(comment, "", "knowledge_preferred", "friendly")

        self.assertIn("KNOWLEDGE", prompt)
        self.assertIn("No knowledge base provided", prompt)

    def test_build_prompt_custom_system(self):
        """Test prompt with custom system prompt."""
        comment = "Test comment"
        knowledge = "Test knowledge"
        custom = "Always be polite and use emojis."

        prompt = build_prompt(
            comment,
            knowledge,
            "unrestricted",
            "friendly",
            custom_prompt=custom,
        )

        self.assertIn("CUSTOM INSTRUCTIONS", prompt)
        self.assertIn(custom, prompt)

    def test_prompt_structure(self):
        """Test prompt has three required sections."""
        comment = "Question?"
        knowledge = "Answer."
        prompt = build_prompt(comment, knowledge, "knowledge_preferred", "professional")

        sections = ["SYSTEM", "KNOWLEDGE", "COMMENT"]
        for section in sections:
            self.assertIn(section, prompt)


if __name__ == "__main__":
    unittest.main()
