"""Configuration tests."""

import os
import tempfile
import unittest

from openreplay.config import Config


class TestConfig(unittest.TestCase):
    """Test configuration module."""

    def test_default_config(self):
        """Test default configuration values."""
        config = Config("nonexistent.yaml")
        self.assertEqual(config.provider, "youtube")
        self.assertEqual(config.llm_base_url, "http://localhost:11434/v1")
        self.assertEqual(config.llm_api_key, "dummy")
        self.assertEqual(config.policy_mode, "knowledge_preferred")
        self.assertEqual(config.fallback_strategy, "generic")
        self.assertEqual(config.generation_style, "friendly")

    def test_custom_config(self):
        """Test custom configuration values."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(
                """llm:
  base_url: http://custom:8080/v1
  model: custom-model
policy:
  mode: knowledge_only
"""
            )
            temp_path = f.name

        try:
            config = Config(temp_path)
            self.assertEqual(config.provider, "youtube")
            self.assertEqual(config.llm_base_url, "http://custom:8080/v1")
            self.assertEqual(config.llm_model, "custom-model")
            self.assertEqual(config.policy_mode, "knowledge_only")
            self.assertEqual(config.fallback_strategy, "generic")
        finally:
            os.unlink(temp_path)

    def test_dot_notation(self):
        """Test dot notation access."""
        config = Config("nonexistent.yaml")
        self.assertEqual(config.get("llm.base_url"), "http://localhost:11434/v1")
        self.assertEqual(config.get("llm.model"), "qwen3")
        self.assertIsNone(config.get("nonexistent.key"))

    def test_property_access(self):
        """Test property accessors."""
        config = Config("nonexistent.yaml")
        self.assertEqual(config.llm_base_url, "http://localhost:11434/v1")
        self.assertEqual(config.llm_model, "qwen3")
        self.assertEqual(config.policy_mode, "knowledge_preferred")
        self.assertEqual(config.fallback_strategy, "generic")
        self.assertEqual(config.generation_style, "friendly")


if __name__ == "__main__":
    unittest.main()
