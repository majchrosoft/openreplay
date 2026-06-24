# 026 - Add CI/CD Pipeline

## Objective
Set up continuous integration for automated testing.

## Input
- GitHub repository

## Output
- Working CI/CD pipeline

## Deliverables

### Files to Create
1. `.github/workflows/tests.yml` - Test workflow
2. `.github/workflows/lint.yml` - Lint workflow

### CI Features
- Run tests on push
- Run linter checks
- Format verification
- Build verification

### Configuration
- Python version: 3.11+
- Test command: `pytest`
- Linter: `ruff` or `flake8`

## Testing
- Push sample changes
- Verify CI runs
- Verify test results appear

## Time Estimate
2 hours
