# Contributing to OpenReplay

Thank you for your interest in contributing to OpenReplay!

## Getting Started

### Development Setup

1. Fork the repository
2. Clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/openreplay.git
cd openreplay
```

3. Install development dependencies:

```bash
pip install -e ".[dev]"
```

4. Run tests to verify setup:

```bash
python3 -m pytest tests/
```

### Code Style

OpenReplay follows PEP 8 style guidelines with the following additions:

- Use type hints for all functions
- Docstrings for all public functions (Google style)
- Max line length: 100 characters
- 4 spaces per indentation level

**Example:**
```python
def process_comments(comments: List[Comment], output: str) -> List[Reply]:
    """Process comments and generate AI replies.
    
    Args:
        comments: List of YouTube comment objects
        output: Path to save replies
        
    Returns:
        List of generated Reply objects
    """
    replies = []
    for comment in comments:
        reply = generate_reply(comment)
        replies.append(reply)
    
    save_replies(replies, output)
    return replies
````

### Development Workflow

1. Create a branch for your feature:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Add tests for new functionality
4. Run all tests:

```bash
python3 -m pytest tests/ -v
````

5. Lint your code:

```bash
python3 -m flake8 commands/ core/ llm/ providers/ tests/
````

6. Commit your changes:

```bash
git add .
git commit -m "feat: add new feature"
```

7. Push to your fork:

```bash
git push origin feature/your-feature-name
````

8. Open a Pull Request

## Pull Request Guidelines

Before submitting a PR:

- [ ] Tests pass (`python3 -m pytest tests/`)
- [ ] Lint passes (`python3 -m flake8`)
- [ ] Documentation updated
- [ ] CHANGELOG entry added (if applicable)
- [ ] Commit messages follow conventional commits

PR title format:
```
type: description

type = feat | fix | docs | test | refactor | chore
```

Examples:
- `feat: add Twitter provider support`
- `fix: handle missing config file`
- `docs: update usage guide`
- `test: add integration tests`

## Testing

### Unit Tests

Add tests for new features:

```python
# tests/test_new_feature.py

class TestNewFeature(unittest.TestCase):
    def test_feature_works(self):
        result = new_feature()
        self.assertEqual(result, expected)
```

Run tests:
```bash
python3 -m pytest tests/test_new_feature.py -v
````

### Integration Tests

Test component interactions:

```python
@patch("llm.generator.requests.post")
def test_end_to_end(self, mock_post):
    # Test complete workflow
    pass
````

## Documentation

### Updating Docs

1. Edit relevant `.md` files in project root
2. Update CLI help text in `openreplay/__main__.py`
3. Add/modify examples

### Adding New Feature Docs

1. Update USAGE.md with new command/options
2. Add example workflow
3. Update ARCHITECTURE.md if needed

## Code Review Process

1. Automated checks run on PR
2. Reviewer provides feedback
3. Address feedback with additional commits
4. Merge when approved

## Questions?

- Open an issue for questions
- Check existing documentation
- Review example code in the repository

## Recognition

Contributors are listed in:
- Contributors section in README
- CHANGELOG for significant contributions

Thank you for contributing to OpenReplay!
