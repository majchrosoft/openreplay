# 001 - Setup Project Structure

## Objective
Create the basic directory structure and project files for the OpenReplay CLI application.

## Input
- None (initial project setup)

## Output
- Project directory structure
- Python project files (pyproject.toml)
- Basic Python package files

## Deliverables

### Directory Structure
```
openreplay/
├── config.yaml
├── knowledge.md
├── response_template.txt
├── main.py
├── openreplay/
│   ├── __init__.py
│   ├── config.py
│   ├── __main__.py
├── providers/
│   ├── __init__.py
│   └── youtube.py
├── llm/
│   ├── __init__.py
│   └── generator.py
├── core/
│   ├── __init__.py
│   ├── policies.py
│   └── prompts.py
├── commands/
│   ├── __init__.py
│   ├── auth.py
│   ├── fetch.py
│   ├── generate.py
│   └── publish.py
└── workspace/
    ├── comments.json
    ├── replies.json
    └── published.json
```

### Files to Create
1. `pyproject.toml` - Project metadata and dependencies
2. `openreplay/__init__.py` - Package initialization
3. `main.py` - CLI entry point
4. `openreplay/__main__.py` - Module execution
5. `openreplay/config.py` - Configuration module skeleton
6. `providers/__init__.py` - Providers package
7. `providers/youtube.py` - YouTube provider skeleton
8. `llm/__init__.py` - LLM package
9. `llm/generator.py` - Generator skeleton
10. `core/__init__.py` - Core package
11. `core/policies.py` - Policies skeleton
12. `core/prompts.py` - Prompts skeleton
13. `commands/__init__.py` - Commands package
14. `workspace/` - Directory for JSON files

## Testing
- Verify all directories and files are created
- Run `python -m openreplay` successfully (should show basic CLI output)
- Verify no import errors

## Time Estimate
30 minutes
