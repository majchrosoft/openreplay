"""Knowledge loading tests."""

import os
import tempfile
import unittest

from openreplay.knowledge import KnowledgeBase


class TestKnowledgeBase(unittest.TestCase):
    """Test knowledge base loading and parsing."""

    def test_empty_knowledge_base(self):
        """Test empty knowledge base."""
        kb = KnowledgeBase()
        self.assertEqual(kb.get_all_content(), "")

    def test_load_qa_pairs(self):
        """Test loading Q&A pairs from text."""
        text = """Q: How long is shipping?
A: Shipping takes 2-3 business days.

Q: Do you ship internationally?
A: Yes, we ship worldwide."""
        kb = KnowledgeBase()
        kb.load_from_text(text)
        self.assertEqual(len(kb.get_qa_pairs()), 2)

    def test_parse_qa_pairs(self):
        """Test Q&A pair parsing."""
        text = """Q: How long is shipping?
A: Shipping takes 2-3 business days."""
        kb = KnowledgeBase()
        kb.load_from_text(text)
        pairs = kb.get_qa_pairs()
        self.assertEqual(pairs[0][0], "How long is shipping?")
        self.assertEqual(pairs[0][1], "Shipping takes 2-3 business days.")

    def test_load_from_file(self):
        """Test loading from file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("Q: Test question?\nA: Test answer.")
            temp_path = f.name

        try:
            kb = KnowledgeBase()
            kb.load_from_file(temp_path)
            self.assertEqual(len(kb.get_qa_pairs()), 1)
        finally:
            os.unlink(temp_path)

    def test_missing_file_handling(self):
        """Test handling of missing file."""
        kb = KnowledgeBase()
        result = kb.load_from_file("nonexistent.md")
        self.assertFalse(result)
        self.assertEqual(len(kb.get_qa_pairs()), 0)

    def test_get_all_content(self):
        """Test get_all_content formatting."""
        text = """Q: Question?
A: Answer."""
        kb = KnowledgeBase()
        kb.load_from_text(text)
        content = kb.get_all_content()
        self.assertIn("Q: Question?", content)
        self.assertIn("A: Answer", content)

    def test_empty_file_handling(self):
        """Test handling of empty file."""
        kb = KnowledgeBase()
        result = kb.load_from_text("")
        self.assertTrue(result)
        self.assertEqual(len(kb.get_qa_pairs()), 0)

    def test_fallback_text(self):
        """Test fallback text functionality."""
        kb = KnowledgeBase()
        kb.add_fallback_text("Additional context information.")
        self.assertEqual(kb.get_all_content(), "Additional context information.")


if __name__ == "__main__":
    unittest.main()
