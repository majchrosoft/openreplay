# 010 - Create YouTube OAuth2 Authentication

## Objective
Implement YouTube OAuth2 authentication flow.

## Input
- None (starts from scratch)

## Output
- Authenticated YouTube session with stored tokens

## Deliverables

### Files to Create
1. `providers/youtube.py` - YouTube provider implementation

### Features
- OAuth2 flow implementation
- Browser opening for authentication
- Token storage in tokens/youtube.json
- Token refresh handling
- API key fallback support

### Authentication Flow
1. Check for existing tokens
2. If missing, open browser for OAuth2
3. Handle callback and receive tokens
4. Store tokens locally
5. Validate tokens work

### Storage
```
tokens/
└── youtube.json
    {
        "access_token": "...",
        "refresh_token": "...",
        "expires_at": timestamp,
        "token_type": "Bearer"
    }
```

## Testing
- Test OAuth2 flow simulation
- Verify token storage
- Test token reuse
- Test expired token refresh

## Time Estimate
2 hours
