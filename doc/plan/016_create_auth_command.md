# 016 - Create Auth Command

## Objective
Create the authentication CLI command.

## Input
- None (command: `openreplay auth`)

## Output
- YouTube authentication tokens stored locally

## Deliverables

### Files to Create
1. `commands/auth.py` - Authentication command

### Features
- Check for existing tokens
- Launch OAuth2 flow
- Open browser for authentication
- Handle OAuth2 callback
- Store tokens in tokens/youtube.json
- Support client_secret.json via --client-secret flag
- Support environment variables (GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET)
- Show success message

### Command Implementation
```python
def main():
    # Check existing tokens
    # If missing/invalid, run OAuth2
    # Display success
```

## Testing
- Test with no existing tokens
- Test with valid existing tokens
- Test token refresh
- Verify output messages

## Time Estimate
1.5 hours
