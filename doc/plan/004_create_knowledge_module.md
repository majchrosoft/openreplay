# 004 - Create Knowledge Loading Functions

## Objective
Create functions to load and parse the knowledge base from knowledge.md file.

## Input
- knowledge.md file with Q&A format content

## Output
- Knowledge data structure that can be queried by the prompt builder

## Deliverables

### Files to Create
1. `openreplay/knowledge.py` - Knowledge loading module

### Features
- Parse knowledge.md file (Q&A format)
- Extract question-answer pairs
- Support markdown format with Q: and A: prefixes
- Store knowledge as structured data
- Handle empty or missing knowledge files
- Support multiple knowledge sources (future extensibility)

### Data Structure
```python
class KnowledgeBase:
    def __init__(self):
        self.qa_pairs = []  # List of (question, answer) tuples
        self.fallback_text = ""  # Plain text fallback
    
    def load_from_file(filepath)
    def load_from_text(text)
    def get_all_content()
    def find_relevant(answer, threshold)
```

## Testing
- Load sample knowledge.md file
- Verify Q&A parsing works correctly
- Handle missing file gracefully
- Test empty file handling

## Time Estimate
1 hour
