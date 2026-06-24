"""
Example Python script showing real-world usage of OpenReplay API.

This demonstrates how to use OpenReplay programmatically rather than via CLI.
"""

# SPDX-License-Identifier: Apache-2.0
# Copyright [2024] Pawel Majchrowicz

import json
from pathlib import Path

from openreplay.config import config
from openreplay.knowledge import KnowledgeBase
from openreplay.template import ResponseTemplate
from llm.generator import LLMGenerator
from core.prompts import build_prompt
from core.policies import PolicyManager
from providers.youtube import YouTubeProvider


def simple_workflow():
    """Minimal example of the complete workflow."""
    
    # 1. Setup
    print("Setting up...")
    provider = YouTubeProvider("client_id", "client_secret")
    
    # 2. Authenticate
    print("Authenticating...")
    provider.authenticate()
    
    # 3. Fetch comments
    print("Fetching comments...")
    video_id = config.video_id
    comments = provider.list_comments(video_id, max_results=10)
    print(f"Fetched {len(comments)} comments")
    
    # 4. Generate replies
    print("Generating replies...")
    knowledge_base = KnowledgeBase()
    knowledge_base.load_from_file("knowledge.md")
    
    template = ResponseTemplate()
    template.load_from_file("response_template.txt")
    
    generator = LLMGenerator(
        base_url=config.llm_base_url,
        api_key=config.llm_api_key,
        model=config.llm_model,
    )
    
    policy = PolicyManager(
        mode=config.policy_mode,
        fallback_strategy=config.fallback_strategy,
    )
    
    for comment in comments:
        prompt = build_prompt(
            comment.text,
            knowledge_base.get_all_content(),
            policy.mode,
            config.generation_style,
        )
        
        response = generator.generate_response(comment.text, prompt)
        reply = template.apply(response)
        
        print(f"Comment: {comment.text[:50]}...")
        print(f"Reply: {reply[:50]}...")
        
        # 5. Publish reply
        result = provider.publish_reply(comment.id, reply)
        print(f"Published reply: {result.get('id')}")
        print()


def batch_workflow():
    """Batch processing example."""
    
    # Load comments from file
    with open("workspace/comments.json") as f:
        data = json.load(f)
        comments = data["comments"]
    
    # Load knowledge
    knowledge_base = KnowledgeBase()
    knowledge_base.load_from_file("knowledge.md")
    
    # Load template
    template = ResponseTemplate()
    template.load_from_file("response_template.txt")
    
    # Generate all replies
    replies = []
    for comment in comments:
        prompt = build_prompt(
            comment["content"],
            knowledge_base.get_all_content(),
            "knowledge_preferred",
            "friendly",
        )
        
        response = "Generated response"
        reply_text = template.apply(response)
        
        replies.append({
            "comment_id": comment["id"],
            "original_comment": comment["content"],
            "generated_content": response,
            "final_reply": reply_text,
            "knowledge_mode": "knowledge_preferred",
            "style": "friendly",
        })
    
    # Save replies
    with open("workspace/replies.json", "w") as f:
        json.dump({"replies": replies}, f, indent=2)
    
    print(f"Generated {len(replies)} replies")


def async_workflow():
    """Example of async processing for better performance."""
    
    import asyncio
    
    async def process_comments():
        provider = YouTubeProvider("client_id", "client_secret")
        await provider.authenticate()
        
        comments = await provider.list_comments("video_id", max_results=100)
        print(f"Processing {len(comments)} comments...")
        
        # Process in batches
        batch_size = 10
        for i in range(0, len(comments), batch_size):
            batch = comments[i:i + batch_size]
            
            # Process batch
            for comment in batch:
                print(f"Processing comment {comment.id}")
                # Your processing logic here
    
    asyncio.run(process_comments())


if __name__ == "__main__":
    print("Example workflows:")
    print("1. simple_workflow() - Single comment processing")
    print("2. batch_workflow() - Batch processing from file")
    print("3. async_workflow() - Async batch processing")
    print()
    print("Uncomment the one you want to run:")
