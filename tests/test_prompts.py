"""Prompts module tests."""

import unittest

from core.prompts import build_prompt, build_system_prompt


class TestPrompts(unittest.TestCase):
    """Test prompt building."""

    def test_build_system_prompt_basic(self):
        """Test basic system prompt construction."""
        system, user = build_prompt("test", "Q: A?\nA: B", "knowledge_preferred", "friendly")
        self.assertIn("KNOWLEDGE", system)
        self.assertIn("friendly", system, "Style should be mentioned")

    def test_build_system_prompt_modes(self):
        """Test system prompt for different modes."""
        modes = ["knowledge_only", "knowledge_preferred", "knowledge_combined", "unrestricted"]
        for mode in modes:
            system, user = build_prompt("test", "Q: A?\nA: B", mode, "professional")
            self.assertIn("KNOWLEDGE", system)
            self.assertIsInstance(system, str)
            self.assertIsInstance(user, str)
            self.assertTrue(len(system) > 0)
            self.assertTrue(len(user) > 0)

    def test_build_system_prompt_styles(self):
        """Test system prompt for different styles."""
        styles = ["professional", "friendly", "expert", "marketing"]
        for style in styles:
            system, user = build_prompt("test", "Q: A?\nA: B", "knowledge_preferred", style)
            self.assertIsInstance(system, str)
            self.assertIsInstance(user, str)
            self.assertTrue(len(system) > 0)
            self.assertTrue(len(user) > 0)

    def test_build_complete_prompt(self):
        """Test complete prompt construction."""
        comment = "What is your return policy?"
        knowledge = "Q: Return policy?\nA: 30 days."
        mode = "knowledge_only"
        style = "professional"

        system, user = build_prompt(comment, knowledge, mode, style)

        self.assertIn("KNOWLEDGE", user)
        self.assertIn("COMMENT", user)
        self.assertIn(comment, user)
        self.assertIn(knowledge, user)
        self.assertIn("KNOWLEDGE", system)
        self.assertIn("You MUST only use information", system)

    def test_build_prompt_empty_knowledge(self):
        """Test prompt with empty knowledge base."""
        comment = "Test comment"
        system, user = build_prompt(comment, "", "knowledge_preferred", "friendly")

        self.assertIn("KNOWLEDGE", user)
        self.assertIn("No knowledge base provided", user)

    def test_build_prompt_custom_system(self):
        """Test prompt with custom system prompt."""
        comment = "Test comment"
        knowledge = "Test knowledge"
        custom = "Always be polite and use emojis."

        system, user = build_prompt(
            comment,
            knowledge,
            "unrestricted",
            "friendly",
            custom_prompt=custom,
        )

        self.assertIn("CUSTOM INSTRUCTIONS", system)
        self.assertIn(custom, system)

    def test_prompt_structure(self):
        """Test prompt has three required sections."""
        comment = "Question?"
        knowledge = "Answer."
        system, user = build_prompt(comment, knowledge, "knowledge_preferred", "professional")

        self.assertIn("KNOWLEDGE", system)
        self.assertIn("KNOWLEDGE", user)
        self.assertIn("COMMENT", user)


if __name__ == "__main__":
    unittest.main()
