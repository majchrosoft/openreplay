# 007 - Create Prompts Module

## Objective
Create a module to build prompts for the LLM based on policy, knowledge, and comments.

## Input
- Policy configuration
- Knowledge base content
- User comment
- Response style

## Output
- Complete prompt string ready for LLM API call

## Deliverables

### Files to Create
1. `core/prompts.py` - Prompt building module

### Features
- Build system prompt from policy
- Add knowledge block
- Append user comment
- Apply response style instructions
- Support different prompt structures for different modes

### Prompt Structure
```text
SYSTEM
Behavior instructions based on mode and style

KNOWLEDGE
Knowledge base content

COMMENT
Original user comment
```

### Functions
```python
def build_system_prompt(policy, style)
def build_prompt(comment, knowledge, policy, style)
def validate_prompt(prompt)
```

## Testing
- Verify all three sections are present
- Test different mode instructions are applied
- Test style instructions are applied
- Test mode-specific prompts

## Time Estimate
1.5 hours
