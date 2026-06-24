import unittest
from unittest.mock import Mock, patch

from commands.generate import generate_replies


class TestGenerateIntegration(unittest.TestCase):
    """Integration tests for generate pipeline."""

    @patch("llm.generator.requests.post")
    def test_generate_replies_with_mock(self, mock_post):
        """Test generate_replies with mocked LLM."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test generated response"}}]
        }
        mock_post.return_value = mock_response

        comments = [{"id": "1", "content": "Test comment"}]

        replies = generate_replies(comments=comments, output_file="/tmp/test_replies.json")

        self.assertEqual(len(replies), 1)
        self.assertEqual(replies[0].status, "generated")
        self.assertIn("Test generated response", replies[0].generated_content)


if __name__ == "__main__":
    unittest.main()
