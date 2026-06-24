"""Template module tests."""

import os
import tempfile
import unittest

from openreplay.template import ResponseTemplate


class TestResponseTemplate(unittest.TestCase):
    """Test response template loading and application."""

    def test_default_template(self):
        """Test default templatewhen file is missing."""
        temp_dir = tempfile.mkdtemp()
        os.chdir(temp_dir)

        template = ResponseTemplate("nonexistent.txt")
        self.assertIn("${content}", template.get_template())

    def test_load_from_file(self):
        """Test loading template from file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Custom: ${content}\n[AI enhanced]")
            temp_path = f.name

        try:
            template = ResponseTemplate(temp_path)
            self.assertIn("Custom: ${content}", template.get_template())
        finally:
            os.unlink(temp_path)

    def test_apply_template(self):
        """Test applying template to content."""
        template = ResponseTemplate()
        result = template.apply("This is a test response.")
        self.assertIn("This is a test response.", result)
        self.assertIn("[AI enhanced]", result)

    def test_placeholder_replacement(self):
        """Test ${content} placeholder is replaced."""
        template = ResponseTemplate()
        content = "Test answer"
        result = template.apply(content)
        self.assertNotIn("${content}", result)
        self.assertIn(content, result)

    def test_empty_file_fallback(self):
        """Test fallback when template file is empty."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("")
            temp_path = f.name

        try:
            template = ResponseTemplate(temp_path)
            self.assertIn("${content}", template.get_template())
        finally:
            os.unlink(temp_path)

    def test_missing_placeholder(self):
        """Test template without placeholder."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("No placeholder here.")
            temp_path = f.name

        try:
            template = ResponseTemplate(temp_path)
            self.assertFalse(template.has_placeholder())
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()
