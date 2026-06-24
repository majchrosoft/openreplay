"""Provider interface definitions."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

from abc import ABC, abstractmethod


class Provider(ABC):
    """Abstract base class for all providers."""

    @abstractmethod
    def authenticate(self):
        """Execute OAuth2 flow and return credentials."""

    @abstractmethod
    def list_resources(self):
        """List available resources (videos)."""

    @abstractmethod
    def list_comments(self, resource_id):
        """Fetch comments for a specific resource."""

    @abstractmethod
    def publish_reply(self, resource_id, comment_id, reply):
        """Publish a reply to a specific comment."""

    @abstractmethod
    def get_user_info(self):
        """Get authenticated user information."""
