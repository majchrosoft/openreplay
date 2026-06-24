# OpenReplay

Self-hosted AI-powered community management platform.

## Contributing

We welcome contributions from the community! Here's how you can help:

### Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

### How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to your branch: `git push origin feature/your-feature`
7. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/openreplay.git
cd openreplay

# Install dependencies
pip install -e .
pip install -e ".[dev]"

# Run tests
python -m pytest tests/

# Run linter
python -m flake8 .
```

### Pull Request Process

1. Update the README.md with details of changes (if needed)
2. Add tests for new functionality
3. Ensure all tests pass
4. Add a changelog entry (if significant)
5. The PR will be merged once you have the sign-off of two maintainers

### Good First Issues

Look for issues tagged with "good first issue" or "help wanted".

Thank you for contributing to OpenReplay!
