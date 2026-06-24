name: Feature Request
description: Suggest a new feature or enhancement
title: "[Feature]: "
labels: ["enhancement", "triage"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to suggest a new feature!

  - type: textarea
    id: problem
    attributes:
      label: Problem Description
      description: Is your feature request related to a problem?
      placeholder: "I'm always frustrated when..."
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: A clear and concise description of what you want to happen
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Solutions
      description: A clear and concise description of any alternative solutions or features you've considered

  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Add any other context or screenshots about the feature request here

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - Critical (Blocking usage)
        - High (Important for user experience)
        - Medium (Nice to have)
        - Low (Enhancement/Polish)
    validations:
      required: true
