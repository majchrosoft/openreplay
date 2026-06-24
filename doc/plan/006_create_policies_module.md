# 006 - Create Policies Module

## Objective
Create a module to handle different knowledge modes and fallback strategies.

## Input
- Policy configuration from config.yaml
- Knowledge base content
- User comment

## Output
- Strategy selection based on policy configuration

## Deliverables

### Files to Create
1. `core/policies.py` - Policy handling module

### Knowledge Modes
1. Knowledge Only: Only use knowledge base info
2. Knowledge Preferred: Prefer knowledge base, use general knowledge if needed
3. Knowledge + World Knowledge: Combine knowledge base and model knowledge
4. Unrestricted: Free answer,知识 base as additional context

### Fallback Strategies
1. Generic: Return configured fallback response
2. Skip: No response generated
3. Flag: Mark for manual review

### Data Structures
```python
class PolicyConfig:
    mode: str
    fallback_strategy: str
    custom_prompt: str

class PolicyProcessor:
    def apply_mode(prompt, mode)
    def apply_fallback(content, strategy)
    def validate_policy(config)
```

## Testing
- Test each knowledge mode behavior
- Test each fallback strategy
- Verify policy validation works

## Time Estimate
1 hour
