"""Configuration management module."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

import os
from typing import Any, Dict, Optional

import yaml


class Config:
    """Configuration manager for OpenReplay."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._defaults: Dict[str, Any] = {
            "provider": "youtube",
            "youtube": {"video_id": None},
            "llm": {
                "base_url": "http://localhost:11434/v1",
                "api_key": "dummy",
                "model": "qwen3",
                "timeout": 60,
            },
            "policy": {"mode": "knowledge_preferred"},
            "fallback": {"strategy": "generic"},
            "generation": {"style": "friendly"},
        }
        self.load()

    def load(self) -> None:
        """Load configuration from config.yaml."""
        if not os.path.exists(self.config_path):
            self._config = self._defaults.copy()
            return

        with open(self.config_path, "r") as f:
            user_config = yaml.safe_load(f) or {}

        self._config = self._deep_merge(self._defaults.copy(), user_config)

    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in update.items():
            if isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = self._deep_merge(result.get(key, {}), value)
            else:
                result[key] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    @property
    def provider(self) -> str:
        """Get provider name."""
        return self.get("provider", "youtube")

    @property
    def video_id(self) -> Optional[str]:
        """Get YouTube video ID."""
        return self.get("youtube.video_id")

    @property
    def llm_base_url(self) -> str:
        """Get LLM base URL."""
        return self.get("llm.base_url", "http://localhost:11434/v1")

    @property
    def llm_api_key(self) -> str:
        """Get LLM API key."""
        return self.get("llm.api_key", "dummy")

    @property
    def llm_model(self) -> str:
        """Get LLM model name."""
        return self.get("llm.model", "qwen3")

    @property
    def llm_timeout(self) -> int:
        """Get LLM timeout in seconds."""
        return self.get("llm.timeout", 60)

    @property
    def policy_mode(self) -> str:
        """Get policy mode."""
        return self.get("policy.mode", "knowledge_preferred")

    @property
    def fallback_strategy(self) -> str:
        """Get fallback strategy."""
        return self.get("fallback.strategy", "generic")

    @property
    def generation_style(self) -> str:
        """Get generation style."""
        return self.get("generation.style", "friendly")


config = Config()
