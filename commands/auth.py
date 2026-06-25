"""Authentication command."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

import argparse
import os
from dotenv import load_dotenv

from providers.youtube import YouTubeProvider

load_dotenv()


def run(args: argparse.Namespace):
    """Execute auth command."""
    client_secret_path = getattr(args, "client_secret", None)
    
    if client_secret_path:
        import json
        with open(client_secret_path, "r") as f:
            client_info = json.load(f)
        client_id = client_info.get("installed", {}).get("client_id")
        client_secret = client_info.get("installed", {}).get("client_secret")
    else:
        client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    
    provider = YouTubeProvider(client_id=client_id, client_secret=client_secret)
    
    try:
        tokens = provider.authenticate()
        print("\nAuthentication successful!")
        print("Tokens stored in tokens/youtube.json")
    except ValueError as e:
        print(f"Authentication failed: {e}")
        raise
    except Exception as e:
        print(f"Authentication failed: {e}")
        raise
