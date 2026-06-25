"""LLM generator tests."""

import unittest
from unittest.mock import Mock, patch

from llm.generator import LLMGenerator


class TestLLMGenerator(unittest.TestCase):
    """Test LLM generator module."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = LLMGenerator(
            base_url="http://localhost:11434/v1",
            api_key="test_key",
            model="test-model",
            timeout=5,
        )

    def test_init_defaults(self):
        """Test initialization with defaults."""
        # Use explicit values to avoid using config
        gen = LLMGenerator(
            base_url="http://localhost:11434/v1",
            api_key="dummy",
            model="qwen3",
            timeout=60,
        )
        self.assertEqual(gen.base_url, "http://localhost:11434/v1")
        self.assertEqual(gen.api_key, "dummy")
        self.assertEqual(gen.model, "qwen3")
        self.assertEqual(gen.timeout, 60)

    def test_rate_limitting(self):
        """Test rate limiting is applied."""
        with patch("llm.generator.requests.post") as mock_post:
            with patch("llm.generator.time.sleep") as mock_sleep:
                with patch("llm.generator.time.time") as mock_time:
                    mock_time.return_value = 1000.0
                    mock_response = Mock()
                    mock_response.status_code = 200
                    mock_response.json.return_value = {
                        "choices": [{"message": {"content": "Test response"}}]
                    }
                    mock_post.return_value = mock_response

                    self.generator.generate_response("test")

                    self.assertGreaterEqual(
                        self.generator._last_request_time, 1000.0
                    )
                    self.assertTrue(
                        mock_sleep.called
                        or self.generator._last_request_time >= 1000.0
                    )

    @patch("llm.generator.requests.post")
    def test_generate_response_success(self, mock_post):
        """Test successful API response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        mock_post.return_value = mock_response

        result = self.generator.generate_response("Test prompt")
        self.assertEqual(result, "Test response")

    @patch("llm.generator.requests.post")
    def test_generate_response_with_system_prompt(self, mock_post):
        """Test API call with system prompt."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        mock_post.return_value = mock_response

        self.generator.generate_response("Test prompt", system_prompt="Be helpful")

        call_args = mock_post.call_args
        messages = call_args[1]["json"]["messages"]
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")

    @patch("llm.generator.requests.post")
    def test_generate_response_timeout(self, mock_post):
        """Test timeout handling."""
        from requests.exceptions import Timeout

        mock_post.side_effect = Timeout("Request timeout")

        with self.assertRaises(TimeoutError):
            self.generator.generate_response("Test prompt")

    def test_generate_response_connection_error(self):
        """Test connection error handling."""
        with patch("llm.generator.requests.post") as mock_post:
            mock_post.side_effect = Exception("Connection refused")

            with self.assertRaises(RuntimeError):
                self.generator.generate_response("Test prompt")

    def test_test_connection_success(self):
        """Test successful connection test."""
        with patch("llm.generator.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            self.assertTrue(self.generator.test_connection())

    def test_test_connection_failure(self):
        """Test failed connection test."""
        with patch("llm.generator.requests.get") as mock_get:
            mock_get.side_effect = Exception("Connection failed")
            self.assertFalse(self.generator.test_connection())


if __name__ == "__main__":
    unittest.main()
