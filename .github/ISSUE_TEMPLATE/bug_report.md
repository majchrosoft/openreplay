name: Bug Report
description: File a bug report to help us improve
title: "[Bug]: "
labels: ["bug", "priority-high"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!

  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear and concise description of what the bug is
      placeholder: "When I do X, Y happens instead of Z..."
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the behavior
      placeholder: |
        1. Go to '...'
        2. Click on '....'
        3. Scroll down to '....'
        4. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
      description: A clear and concise description of what you expected to happen
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual behavior
      description: A clear and concise description of what actually happened
    validations:
      required: true

  - type: dropdown
    id: os
    attributes:
      label: OS
      options:
        - macOS
        - Linux
        - Windows
        - Other
    validations:
      required: true

  - type: input
    id: python-version
    attributes:
      label: Python Version
      placeholder: "e.g., 3.10.5"
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Relevant log output
      description: Please copy and paste any relevant log output
      render: shell

  - type: textarea
    id: additional
    attributes:
      label: Additional context
      description: Add any other context about the problem here
