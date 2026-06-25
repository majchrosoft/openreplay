"""Module execution support for OpenReplay."""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz


import argparse
import sys

from openreplay import __version__


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="OpenReplay - AI-powered community management",
        prog="openreplay",
    )
    parser.add_argument(
        "--version", action="store_true", help="Show version and exit"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # auth command
    auth_parser = subparsers.add_parser(
        "auth", help="Authenticate with YouTube account"
    )
    auth_parser.add_argument(
        "--client-secret",
        help="Path to OAuth client secret file",
    )

    # fetch command
    fetch_parser = subparsers.add_parser(
        "fetch", help="Fetch YouTube comments for configured video"
    )
    fetch_parser.add_argument(
        "--output",
        "-o",
        help="Output file for comments",
    )

    # select command
    select_parser = subparsers.add_parser(
        "select", help="Fetch and select YouTube videos"
    )
    select_parser.add_argument(
        "--output",
        "-o",
        help="Output file to save video list",
    )

    # generate command
    generate_parser = subparsers.add_parser(
        "generate", help="Generate AI responses for fetched comments"
    )
    generate_parser.add_argument(
        "--knowledge-file",
        "-k",
        default="knowledge.md",
        help="Knowledge base file path",
    )
    generate_parser.add_argument(
        "--output",
        "-o",
        default="workspace/replies.json",
        help="Output file for replies",
    )

    # publish command
    publish_parser = subparsers.add_parser(
        "publish", help="Publish generated replies to YouTube"
    )
    publish_parser.add_argument(
        "--replies-file",
        default="workspace/replies.json",
        help="Replies file to publish",
    )
    publish_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be published without actually publishing",
    )

    args = parser.parse_args()

    if args.version:
        print(f"OpenReplay v{__version__}")
        sys.exit(0)

    if args.command is None:
        print(f"OpenReplay v{__version__}")
        print("Usage: openreplay <command>")
        print("\nCommands:")
        print("  auth      Authenticate with YouTube")
        print("  fetch     Fetch YouTube comments")
        print("  select    Fetch and select YouTube videos")
        print("  generate  Generate AI responses")
        print("  publish   Publish generated responses")
        sys.exit(0)

    if args.command == "auth":
        from commands.auth import run

        run(args)
    elif args.command == "fetch":
        from commands.fetch import run

        run(args)
    elif args.command == "select":
        from commands.select import run

        run(args)
    elif args.command == "generate":
        from commands.generate import run

        run(args)
    elif args.command == "publish":
        from commands.publish import run

        run(args)


if __name__ == "__main__":
    main()
