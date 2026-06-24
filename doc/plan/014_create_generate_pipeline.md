# 014 - Create Generate Pipeline

## Objective
Create the main generate pipeline that processes all comments.

## Input
- Comments from workspace/comments.json
- Knowledge base from knowledge.md
- Policy configuration
- LLM configuration

## Output
- Generated replies saved to workspace/replies.json

## Deliverables

### Files to Create
1. `commands/generate.py` - Main generation pipeline

### Pipeline Steps
1. Load comments from comments.json
2. Load knowledge base from knowledge.md
3. Load LLM configuration
4. Load response template
5. For each comment:
   - Build prompt using policy and style
   - Call LLM generator
   - Apply response template
   - Store reply with metadata
6. Save all replies to replies.json

### Reply Storage
```python
class Reply:
    comment_id: str
    original_comment: str
    generated_content: str
    final_reply: str
    knowledge_mode: str
    style: str
    timestamp: datetime
    status: str  # generated, failed
```

## Testing
- Test with sample comments
- Verify all steps execute
- Verify output storage
- Test error handling per comment

## Time Estimate
2 hours
