"""Generate command tests."""

import json
import tempfile
import unittest
from unittest.mock import patch

from commands.generate import Reply, generate_replies, load_comments, save_replies


class TestGenerateCommand(unittest.TestCase):
    """Test generate command."""

    def test_reply_to_dict(self):
        """Test Reply object serialization."""
        reply = Reply(
            comment_id="123",
            original_comment="Test comment",
            generated_content="Test response",
            final_reply="Final: Test response",
            knowledge_mode="knowledge_preferred",
            style="friendly",
        )
        result = reply.to_dict()
        self.assertEqual(result["comment_id"], "123")
        self.assertEqual(result["original_comment"], "Test comment")
        self.assertEqual(result["status"], "generated")

    def test_load_comments_empty_file(self):
        """Test loading comments from empty file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"comments": []}, f)
            temp_path = f.name

        try:
            comments = load_comments(temp_path)
            self.assertEqual(len(comments), 0)
        finally:
            import os

            os.unlink(temp_path)

    def test_load_comments_valid_file(self):
        """Test loading comments from valid file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(
                {"comments": [{"id": "1", "content": "First"}, {"id": "2", "content": "Second"}]},
                f,
            )
            temp_path = f.name

        try:
            comments = load_comments(temp_path)
            self.assertEqual(len(comments), 2)
            self.assertEqual(comments[0]["id"], "1")
        finally:
            import os

            os.unlink(temp_path)

    def test_save_replies(self):
        """Test saving replies to file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            reply = Reply(
                comment_id="123",
                original_comment="Test",
                generated_content="Response",
                final_reply="Final",
                knowledge_mode="test",
                style="test",
            )
            save_replies([reply], temp_path)

            with open(temp_path, "r") as f:
                data = json.load(f)

            self.assertIn("replies", data)
            self.assertEqual(len(data["replies"]), 1)
            self.assertEqual(data["replies"][0]["comment_id"], "123")
        finally:
            import os

            os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()
