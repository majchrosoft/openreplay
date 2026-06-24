name: Security Issue
description: Report a security vulnerability
title: "[Security]: "
labels: ["security", "priority-critical"]

body:
  - type: markdown
    attributes:
      value: |
        **Please do NOT report security vulnerabilities publicly.**
        
        Email us directly at security@openreplay.example.com with details.

  - type: textarea
    id: details
    attributes:
      label: Issue Details
      description: Describe the security issue
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: How can this vulnerability be exploited?

  - type: input
    id: version
    attributes:
      label: Affected Version
      placeholder: "e.g., v0.1.0"

  - type: dropdown
    id: severity
    attributes:
      label: Severity
      options:
        - Critical (Remote code execution, data breach)
        - High (Privilege escalation, authentication bypass)
        - Medium (Information disclosure, DoS)
        - Low (Minor info exposure)
