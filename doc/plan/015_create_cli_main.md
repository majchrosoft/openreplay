# 015 - Create CLI Main Entry Point

## Objective
Create the main CLI entry point with command structure.

## Input
- Command-line arguments

## Output
- Executed command function

## Deliverables

### Files to Create
1. `main.py` - CLI entry point
2. `openreplay/__main__.py` - Module execution

### CLI Commands
```bash
openreplay auth
openreplay fetch
openreplay generate
openreplay publish
openreplay --help
```

### Implementation
```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="OpenReplay CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    # auth command
    auth_parser = subparsers.add_parser("auth", help="Authenticate with YouTube")
    
    # fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch YouTube comments")
    
    # generate command
    generate_parser = subparsers.add_parser("generate", help="Generate AI replies")
    
    # publish command
    publish_parser = subparsers.add_parser("publish", help="Publish replies to YouTube")
    
    args = parser.parse_args()
    
    if args.command == "auth":
        from commands.auth import main as auth_main
        auth_main()
    elif args.command == "fetch":
        from commands.fetch import main as fetch_main
        fetch_main()
    # ... etc
```

## Testing
- Test all commands exist
- Test help output
- Test command routing

## Time Estimate
1 hour
