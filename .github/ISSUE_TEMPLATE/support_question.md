name: Support Question
description: Ask a question about using OpenReplay
title: "[Question]: "
labels: ["question", "triage"]

body:
  - type: markdown
    attributes:
      value: |
        Please check the documentation and existing issues before asking your question.

  - type: textarea
    id: question
    attributes:
      label: Your Question
      description: A clear and concise question about OpenReplay
    validations:
      required: true

  - type: textarea
    id: context
    attributes:
      label: Context
      description: How has this issue affected you? What are you trying to do?

  - type: textarea
    id: what-trying
    attributes:
      label: What You're Trying to Do
      description: A clear description of your goal

  - type: textarea
    id: attempts
    attributes:
      label: What You've Tried
      description: What have you already tried?

  - type: input
    id: version
    attributes:
      label: OpenReplay Version
      placeholder: "e.g., v0.1.0"

  - type: input
    id: python-version
    attributes:
      label: Python Version
      placeholder: "e.g., 3.10.5"
