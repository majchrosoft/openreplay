# 008 - Create LLM Generator Module

## Objective
Create a module to make API calls to the LLM endpoint.

## Input
- Complete prompt string
- LLM configuration (base_url, api_key, model)

## Output
- Generated text response

## Deliverables

### Files to Create
1. `llm/generator.py` - LLM API calling module

### Features
- Send POST request to LLM endpoint
- Handle OpenAI-compatible API format
- Support streaming responses (future)
- Error handling for connection issues
- Timeout handling

### API Call Structure
```python
def generate_response(prompt, config):
    headers = {"Authorization": f"Bearer {config.api_key}"}
    data = {"model": config.model, "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(config.base_url + "/chat/completions", json=data)
    return response.json()["choices"][0]["message"]["content"]
```

## Testing
- Test with dummy API key (should fail gracefully)
- Test connection to local LLM if available
- Verify response parsing works
- Test error handling (timeout, connection refused)

## Time Estimate
1.5 hours
