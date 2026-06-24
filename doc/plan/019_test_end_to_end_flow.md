# 019 - Test End-to-End Flow

## Objective
Test the complete workflow from start to finish.

## Input
- None (integration test)

## Output
- Verified end-to-end functionality

## Deliverables

### Test Scenarios
1. Fresh setup (no config, no tokens):
   - Create config.yaml
   - Run auth (manual OAuth)
   - Run fetch
   - Run generate
   - Run publish

2. Resume scenario:
   - Run fetch (skip auth)
   - Run generate
   - Run publish

3. Error handling:
   - Missing config
   - Invalid tokens
   - API errors

### Verification Steps
- All commands execute without errors
- Files are created in correct locations
- Data is properly stored
- Generated replies match expected format

## Testing
- Manual testing of complete workflow
- Error injection testing
- Edge case verification

## Time Estimate
2 hours
