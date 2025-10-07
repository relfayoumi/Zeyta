#!/usr/bin/env python3
"""
Demonstration of the History Control Feature.

This script demonstrates:
1. Creating chat sessions with timestamped messages
2. Searching past conversations
3. Memory query detection
4. How the LLM can access past conversations

Note: This is a demonstration script that simulates the feature.
For actual use, the feature is integrated into the main conversation loop.
"""
import sys
import os
import json
from pathlib import Path
from datetime import datetime
import time

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.context import ContextManager


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_subsection(title):
    """Print a formatted subsection header"""
    print(f"\n--- {title} ---")


def demo_basic_chat_logging():
    """Demonstrate basic chat logging with timestamps"""
    print_section("DEMO 1: Chat Logging with Timestamps")
    
    # Create a temporary directory for demo
    demo_dir = Path("demo_chat_logs")
    demo_dir.mkdir(exist_ok=True)
    
    print("\nCreating a new chat session...")
    context = ContextManager("You are a helpful AI assistant.", log_dir=str(demo_dir))
    
    print("\nSimulating a conversation:")
    
    # Simulate conversation
    conversations = [
        ("user", "Hello, I'm learning Python programming."),
        ("assistant", "That's great! Python is an excellent language for beginners and experts alike."),
        ("user", "Can you tell me about machine learning?"),
        ("assistant", "Machine learning is a subset of AI that allows computers to learn from data."),
        ("user", "Thanks for the help!"),
        ("assistant", "You're welcome! Feel free to ask anytime."),
    ]
    
    for role, content in conversations:
        context.add_message(role, content)
        print(f"  {role}: {content}")
        time.sleep(0.1)  # Small delay to show timestamp differences
    
    context.save_snapshot()
    
    print(f"\n✓ Chat session saved to: {context.session_file}")
    
    # Show the saved content
    print_subsection("Saved Chat Log Content")
    with open(context.session_file, 'r') as f:
        data = json.load(f)
    
    for msg in data[:3]:  # Show first 3 messages
        timestamp = msg.get('timestamp', 'N/A')
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')[:50] + "..." if len(msg.get('content', '')) > 50 else msg.get('content', '')
        print(f"  [{timestamp}] {role}: {content}")
    
    print(f"  ... and {len(data) - 3} more messages")
    
    return demo_dir


def demo_search_past_conversations(demo_dir):
    """Demonstrate searching past conversations"""
    print_section("DEMO 2: Searching Past Conversations")
    
    # Create a new session (simulating a new conversation the next day)
    print("\nStarting a new chat session...")
    time.sleep(1.1)  # Ensure different timestamp
    context = ContextManager("You are a helpful AI assistant.", log_dir=str(demo_dir))
    
    print("\nSearching for 'Python' in past conversations...")
    results = context.search_past("Python", limit=5)
    
    if results:
        print(f"Found {len(results)} messages containing 'Python':")
        for i, msg in enumerate(results, 1):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            timestamp = msg.get('timestamp', 'unknown')
            file = msg.get('file', 'unknown')
            print(f"\n  Result {i}:")
            print(f"    File: {file}")
            print(f"    Time: {timestamp}")
            print(f"    {role}: {content}")
    else:
        print("No results found.")
    
    print_subsection("Searching for 'machine learning'")
    results = context.search_past("machine learning", limit=3)
    if results:
        print(f"Found {len(results)} messages:")
        for msg in results:
            print(f"  - {msg.get('role')}: {msg.get('content')[:60]}...")


def demo_memory_query_detection(demo_dir):
    """Demonstrate memory query detection"""
    print_section("DEMO 3: Memory Query Detection")
    
    context = ContextManager("You are a helpful AI assistant.", log_dir=str(demo_dir))
    
    test_queries = [
        ("Do you remember what I said about Python?", True),
        ("Can you recall our conversation about machine learning?", True),
        ("What did we discuss earlier?", True),
        ("What is the weather today?", False),
        ("How do I write a for loop?", False),
        ("You mentioned something about AI last time", True),
    ]
    
    print("\nTesting memory query detection:")
    for query, expected in test_queries:
        is_memory_query = context.detect_memory_query(query)
        status = "✓" if is_memory_query == expected else "✗"
        detected = "MEMORY QUERY" if is_memory_query else "regular query"
        print(f"\n  {status} '{query}'")
        print(f"     → Detected as: {detected}")


def demo_memory_search_and_format(demo_dir):
    """Demonstrate integrated memory search and formatting"""
    print_section("DEMO 4: Memory Search and Formatting for LLM")
    
    context = ContextManager("You are a helpful AI assistant.", log_dir=str(demo_dir))
    
    query = "Do you remember what I asked about Python and machine learning?"
    
    print(f"\nUser query: '{query}'")
    print("\nSearching past conversations and formatting for LLM context...")
    
    memories = context.search_and_format_memories(query, limit=5)
    
    if memories:
        print("\n" + "-" * 70)
        print("FORMATTED MEMORY CONTEXT (injected into LLM):")
        print("-" * 70)
        print(memories)
        print("-" * 70)
        print("\n✓ This context would be injected into the LLM's message history")
        print("  to help it answer the user's question using past conversations.")
    else:
        print("\nNo relevant memories found.")


def demo_how_it_works_with_llm():
    """Explain how the feature integrates with the LLM"""
    print_section("DEMO 5: Integration with LLM")
    
    print("""
The history control feature works automatically in the main conversation loop:

1. USER ASKS A QUESTION
   Example: "Do you remember what I said about Python?"
   
2. MEMORY DETECTION
   The system detects keywords like 'remember', 'recall', etc.
   
3. SEARCH PAST CONVERSATIONS
   The system searches all past chat log files for relevant content.
   It extracts key terms from the user's query (e.g., 'Python').
   
4. FORMAT RESULTS
   Search results are formatted with timestamps and roles:
   "[2024-01-01T10:00:00] user: I'm learning Python programming."
   
5. INJECT INTO LLM CONTEXT
   The formatted memories are added to the message history as a system message
   just before the LLM generates its response.
   
6. LLM GENERATES RESPONSE
   The LLM can now reference the past conversations in its response:
   "Yes, I remember! You mentioned you were learning Python programming..."

CONFIGURATION:
   Set ENABLE_HISTORY_SEARCH = True in config.py to enable this feature.
   Set ENABLE_HISTORY_SEARCH = False to disable automatic memory search.

The feature is transparent and requires no user intervention - it just works!
    """)


def cleanup_demo(demo_dir):
    """Ask if user wants to clean up demo files"""
    print_section("Cleanup")
    
    response = input(f"\nDelete demo chat logs in '{demo_dir}'? (y/n): ").lower().strip()
    
    if response == 'y':
        import shutil
        shutil.rmtree(demo_dir)
        print(f"✓ Deleted {demo_dir}")
    else:
        print(f"Demo files kept in: {demo_dir}")
        print("You can examine the JSON files to see the timestamped chat logs.")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("  HISTORY CONTROL FEATURE DEMONSTRATION")
    print("  Simulated Long-Term Memory for AI Conversations")
    print("=" * 70)
    
    try:
        # Run demonstrations
        demo_dir = demo_basic_chat_logging()
        demo_search_past_conversations(demo_dir)
        demo_memory_query_detection(demo_dir)
        demo_memory_search_and_format(demo_dir)
        demo_how_it_works_with_llm()
        
        print_section("SUMMARY")
        print("""
✓ Chat logs are saved with timestamps for each message
✓ Past conversations can be searched using keywords
✓ Memory queries are automatically detected
✓ Relevant past conversations are injected into LLM context
✓ Feature can be enabled/disabled via configuration

This feature enables the AI to have "long-term memory" by accessing
past conversation logs when users ask questions like "Do you remember...?"
        """)
        
        cleanup_demo(demo_dir)
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
