# 002 - Create Config Module

## Objective
Create a configuration module that loads and validates settings from config.yaml.

## Input
- `config.yaml` file with the project configuration

## Output
- Config module that reads and parses YAML configuration
- Configuration data structure accessible throughout the application

## Deliverables

### Configuration Schema
- provider (string): Currently only "youtube"
- youtube (dict): Provider-specific settings
  - video_id (string): YouTube video identifier
- llm (dict): LLM endpoint configuration
  - base_url (string): API endpoint URL
  - api_key (string): API key for authentication
  - model (string): Model name to use
- policy (dict): Response policy settings
  - mode (string): Knowledge mode (only, preferred, combined, unrestricted)
- fallback (dict): Fallback strategy configuration
  - strategy (string): How to handle missing information (generic, skip, flag)
- generation (dict): Generation settings
  - style (string): Response style (professional, friendly, expert, marketing, custom)

### Files to Create
1. `openreplay/config.py` - Configuration loader and validator

### Features
- Load configuration from config.yaml
- Validate required fields
- Provide fallback defaults
- Expose configuration via simple attribute access
- Handle missing configuration files gracefully

## Testing
- Verify loading valid config.yaml
- Test missing file handling
- Test default value application
- Test invalid value rejection

## Time Estimate
1 hour
