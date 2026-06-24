# 005 - Create Response Template Module

## Objective
Create a module to load and apply response templates to generated content.

## Input
- response_template.txt file with ${content} placeholder
- Generated content string

## Output
- Fully formatted response string with template applied

## Deliverables

### Files to Create
1. `openreplay/template.py` - Template loading and application module

### Features
- Load template from response_template.txt
- Support ${content} placeholder replacement
- Handle missing template files with default fallback
- Support additional placeholders (future extensibility)
- Validate template format before application

## Testing
- Load sample template file
- Verify ${content} placeholder is replaced
- Test missing template fallback

## Time Estimate
30 minutes
