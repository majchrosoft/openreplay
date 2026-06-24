"""LLM generator module for API calls."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

import time
from typing import Optional

import requests


class LLMGenerator:
    """Generates AI responses using LLM API."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434/v1",
        api_key: str = "dummy",
        model: str = "qwen3",
        timeout: int = 60,
    ):
        """Initialize LLM generator."""
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self._last_request_time = 0
        self._rate_limit_delay = 0.1

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Generate a response from the LLM.

        Args:
            prompt: The user prompt text
            system_prompt: Optional system prompt to set behavior

        Returns:
            Generated response text

        Raises:
            ConnectionError: If API call fails
            TimeoutError: If request times out
        """
        # Rate limiting
        elapsed = time.time() - self._last_request_time
        if elapsed < self._rate_limit_delay:
            time.sleep(self._rate_limit_delay - elapsed)
        self._last_request_time = time.time()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=data,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request to {self.base_url} timed out")
        except Exception as e:
            raise RuntimeError(f"LLM API error: {e}")

    def test_connection(self) -> bool:
        """Test if LLM endpoint is reachable.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                timeout=5,
            )
            return response.status_code == 200
        except Exception:
            return False


generator = LLMGenerator()
