"""Policies module tests."""

import unittest

from core.policies import (
    FALLBACK_RESPONSES,
    KNOWLEDGE_MODES,
    get_fallback_response,
    get_knowledge_mode_instructions,
)


class TestPolicies(unittest.TestCase):
    """Test policy handling."""

    def test_knowledge_modes_exist(self):
        """Test all knowledge modes are defined."""
        modes = ["knowledge_only", "knowledge_preferred", "knowledge_combined", "unrestricted"]
        for mode in modes:
            self.assertIn(mode, KNOWLEDGE_MODES)
            self.assertIsInstance(KNOWLEDGE_MODES[mode], str)
            self.assertTrue(len(KNOWLEDGE_MODES[mode]) > 0)

    def test_get_knowledge_mode_instructions(self):
        """Test getting instructions for a mode."""
        instructions = get_knowledge_mode_instructions("knowledge_only")
        self.assertIn("KNOWLEDGE", instructions)
        self.assertIn("CRITICAL", instructions)

    def test_get_knowledge_mode_invalid_fallback(self):
        """Test invalid mode returns default."""
        instructions = get_knowledge_mode_instructions("invalid_mode")
        self.assertIn("KNOWLEDGE", instructions)

    def test_fallback_strategies(self):
        """Test fallback strategies."""
        self.assertEqual(FALLBACK_RESPONSES["generic"], "I could not find information about that topic.")
        self.assertIsNone(FALLBACK_RESPONSES["skip"])

    def test_get_fallback_response(self):
        """Test getting fallback response."""
        self.assertEqual(get_fallback_response("generic"), "I could not find information about that topic.")
        self.assertIsNone(get_fallback_response("skip"))
        self.assertIsNone(get_fallback_response("invalid"))


if __name__ == "__main__":
    unittest.main()
