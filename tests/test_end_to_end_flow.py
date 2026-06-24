"""End-to-end flow tests."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from commands.auth import run as auth_run
from commands.fetch import run as fetch_run, save_comments
from commands.generate import generate_replies, Reply
from commands.publish import run as publish_run, load_replies


class TestEndToEndFlow(unittest.TestCase):
    """Test complete workflow end-to-end."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.workspace = Path(self.temp_dir) / "workspace"
        self.workspace.mkdir()
        
        self.comments_file = self.workspace / "comments.json"
        self.replies_file = self.workspace / "replies.json"
        self.published_file = self.workspace / "published.json"
        
        self.test_comments = [
            {
                "id": "comment_1",
                "content": "Can you explain how this works?",
                "author": "user1",
                "published_at": "2024-01-01T10:00:00Z",
            },
            {
                "id": "comment_2",
                "content": "Is this available internationally?",
                "author": "user2",
                "published_at": "2024-01-01T11:00:00Z",
            },
        ]
        save_comments(self.test_comments, str(self.comments_file))

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("providers.youtube.YouTubeProvider.authenticate")
    @patch("providers.youtube.YouTubeProvider.list_comments")
    def test_fetch_command(self, mock_list_comments, mock_authenticate):
        """Test fetch command end-to-end."""
        mock_authenticate.return_value = {
            "access_token": "test_token",
            "expires_at": 9999999999,
        }
        
        mock_list_comments.return_value = []
        
        args = Mock()
        args.output = str(self.comments_file)
        
        fetch_run(args)
        
        self.assertTrue(self.comments_file.exists())
        
        with open(self.comments_file) as f:
            data = json.load(f)
        
        self.assertIn("comments", data)
        self.assertIn("loaded_at", data)

    @patch("llm.generator.requests.post")
    def test_generate_command(self, mock_post):
        """Test generate command end-to-end."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test generated response"}}]
        }
        mock_post.return_value = mock_response
        
        os.chdir(self.temp_dir)
        
        comments = json.loads(self.comments_file.read_text())
        
        replies = generate_replies(
            comments=comments["comments"],
            output_file=str(self.replies_file),
        )
        
        self.assertEqual(len(replies), 2)
        self.assertTrue(self.replies_file.exists())
        
        for reply in replies:
            self.assertEqual(reply.status, "generated")
            self.assertIn("Test generated response", reply.generated_content)

    @patch("providers.youtube.YouTubeProvider.authenticate")
    @patch("providers.youtube.YouTubeProvider.publish_reply")
    def test_publish_command(self, mock_publish, mock_authenticate):
        """Test publish command end-to-end."""
        mock_authenticate.return_value = {
            "access_token": "test_token",
            "expires_at": 9999999999,
        }
        
        mock_publish.return_value = {"id": "reply_123"}
        
        os.chdir(self.temp_dir)
        
        replies = [
            Reply(
                comment_id="comment_1",
                original_comment="Test comment",
                generated_content="Generated",
                final_reply="Final reply",
                knowledge_mode="test",
                style="friendly",
            ),
            Reply(
                comment_id="comment_2",
                original_comment="Test comment 2",
                generated_content="Generated 2",
                final_reply="Final reply 2",
                knowledge_mode="test",
                style="friendly",
            ),
        ]
        
        replies_data = {
            "replies": [r.to_dict() for r in replies],
            "generated_at": "2024-01-01T12:00:00Z",
        }
        self.replies_file.write_text(json.dumps(replies_data))
        
        args = Mock()
        args.replies_file = str(self.replies_file)
        args.dry_run = False
        
        publish_run(args)
        
        self.assertTrue(self.published_file.exists())
        
        with open(self.published_file) as f:
            data = json.load(f)
        
        self.assertIn("published", data)
        self.assertEqual(len(data["published"]), 2)
        
        for pub in data["published"]:
            self.assertEqual(pub["status"], "success")
            self.assertIn("comment_id", pub)
            self.assertIn("reply_id", pub)

    @patch("providers.youtube.YouTubeProvider.authenticate")
    @patch("providers.youtube.YouTubeProvider.publish_reply")
    def test_publish_command_dry_run(self, mock_publish, mock_authenticate):
        """Test publish command with dry-run flag."""
        mock_authenticate.return_value = {
            "access_token": "test_token",
            "expires_at": 9999999999,
        }
        
        os.chdir(self.temp_dir)
        
        replies = [
            Reply(
                comment_id="comment_1",
                original_comment="Test comment",
                generated_content="Generated",
                final_reply="Final reply",
                knowledge_mode="test",
                style="friendly",
            ),
        ]
        
        replies_data = {
            "replies": [r.to_dict() for r in replies],
            "generated_at": "2024-01-01T12:00:00Z",
        }
        self.replies_file.write_text(json.dumps(replies_data))
        
        args = Mock()
        args.replies_file = str(self.replies_file)
        args.dry_run = True
        
        publish_run(args)
        
        mock_publish.assert_not_called()
        
        with open(self.published_file) as f:
            data = json.load(f)
        
        self.assertEqual(data["published"][0]["status"], "skipped (dry run)")


if __name__ == "__main__":
    unittest.main()
