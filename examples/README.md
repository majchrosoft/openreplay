# Examples

This directory contains example files to help you get started with OpenReplay.

## Example Files

### Configuration

- `config.example.yaml` - Complete example configuration with all options documented
- `config.example.yaml` - Minimal configuration for quick start

### Knowledge Base

- `knowledge.example.md` - Sample knowledge base for a tech YouTube channel
- Includes Q&A pairs for common questions
- Shows different topic categories

### Response Templates

- `response_template.example.txt` - Template with placeholders
- Multiple style examples (friendly, professional, enthusiastic, neutral)
- Advanced templates with video references and social links

## Getting Started

1. Copy example files to your project:

```bash
cp examples/config.example.yaml config.yaml
cp examples/knowledge.example.md knowledge.md
cp examples/response_template.example.txt response_template.txt
```

2. Edit the files with your specific information

3. Run OpenReplay:

```bash
openreplay auth --client-secret client_secret.json
openreplay fetch
openreplay generate
openreplay publish
```

## Customization

### Changing Response Style

Edit `response_template.txt`:

```txt
{{generated_content}}

Thanks for asking! Check out my video on [topic] for more details. 🚀
```

### Adding More Knowledge

Edit `knowledge.md`:

```markdown
Q: Your new question?
A: Your new answer goes here!
```

## Troubleshooting

If examples don't work:

1. Check file paths in commands
2. Verify YouTube credentials
3. Ensure LLM service is running
4. Check knowledge.md syntax

## Need More Help?

- See [USAGE.md](../USAGE.md) for command details
- See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) for常见 issues
- Open an issue on GitHub for bug reports
