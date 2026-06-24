name: Pull Request
description: Create a pull request
title: "[PR]: "

body:
  - type: markdown
    attributes:
      value: |
        Thank you for your contribution!

  - type: dropdown
    id: type
    attributes:
      label: Type of Change
      options:
        - Bug fix
        - New feature
        - Enhancement
        - Documentation
        - Test added
        - Refactoring
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear and concise description of what this PR does
    validations:
      required: true

  - type: textarea
    id: tests
    attributes:
      label: Tests
      description: |
        - [ ] Unit tests added/updated
        - [ ] Integration tests added/updated
        - [ ] Tests pass locally
      value: |
        - [ ] Tests added
        - [ ] Tests pass

  - type: textarea
    id: Checklist
    attributes:
      label: Checklist
      value: |
        - [ ] Code follows project style
        - [ ] Documentation updated
        - [ ] Changelog entry added (if applicable)
        - [ ] No secret keys in code
    validations:
      required: true

  - type: input
    id: issue
    attributes:
      label: Related Issue
      description: If this PR resolves an issue, reference it (e.g., Closes #123)

  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots
      description: Add any relevant screenshots or GIFs
