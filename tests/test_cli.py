"""CLI tests."""

import sys
import unittest
from unittest.mock import patch

from openreplay.__main__ import main


class TestCLI(unittest.TestCase):
    """Test CLI entry point."""

    def test_main_no_command(self):
        """Test main with no command shows help."""
        with patch("sys.argv", ["openreplay"]):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)

    def test_main_version_flag(self):
        """Test --version flag."""
        with patch("sys.argv", ["openreplay", "--version"]):
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)

    @patch("commands.auth.run")
    def test_main_auth_command(self, mock_auth):
        """Test auth command execution."""
        with patch("sys.argv", ["openreplay", "auth"]):
            main()
            mock_auth.assert_called_once()

    @patch("commands.fetch.run")
    def test_main_fetch_command(self, mock_fetch):
        """Test fetch command execution."""
        with patch("sys.argv", ["openreplay", "fetch"]):
            main()
            mock_fetch.assert_called_once()

    @patch("commands.generate.run")
    def test_main_generate_command(self, mock_generate):
        """Test generate command execution."""
        with patch("sys.argv", ["openreplay", "generate"]):
            main()
            mock_generate.assert_called_once()

    @patch("commands.publish.run")
    def test_main_publish_command(self, mock_publish):
        """Test publish command execution."""
        with patch("sys.argv", ["openreplay", "publish"]):
            main()
            mock_publish.assert_called_once()


if __name__ == "__main__":
    unittest.main()
