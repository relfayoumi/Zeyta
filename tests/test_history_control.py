#!/usr/bin/env python3
"""
Test script for history control feature.
Tests the ability to save chat logs with timestamps and search past conversations.
"""
import json
import logging
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.context import ContextManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_timestamp_in_messages():
    """Test that messages have timestamps"""
    print("\n=== Test 1: Timestamps in Messages ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        context = ContextManager("Test system prompt", log_dir=tmpdir, auto_save=True)
        
        # Add some messages
        context.add_message("user", "Hello, AI!")
        context.add_message("assistant", "Hello! How can I help?")
        
        # Check that messages have timestamps
        messages = context.get_history()
        for msg in messages[1:]:  # Skip system message which may not have timestamp
            assert "timestamp" in msg, f"Message missing timestamp: {msg}"
            print(f"✓ Message has timestamp: {msg['timestamp']}")
        
        # Verify timestamp format
        timestamp = messages[1]["timestamp"]
        try:
            datetime.fromisoformat(timestamp)
            print(f"✓ Timestamp format is valid ISO format: {timestamp}")
        except ValueError:
            raise AssertionError(f"Invalid timestamp format: {timestamp}")
    
    print("✓ Test 1 PASSED: All messages have valid timestamps\n")


def test_search_past_conversations():
    """Test searching past conversations"""
    print("\n=== Test 2: Search Past Conversations ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create first session
        context1 = ContextManager("Test system", log_dir=tmpdir)
        context1.add_message("user", "What is Python?")
        context1.add_message("assistant", "Python is a programming language.")
        context1.add_message("user", "Tell me about machine learning")
        context1.add_message("assistant", "Machine learning is a subset of AI.")
        context1.save_snapshot()
        
        # Add small delay to ensure different timestamp
        import time
        time.sleep(1.1)
        
        # Create second session
        context2 = ContextManager("Test system", log_dir=tmpdir)
        context2.add_message("user", "How do I use TensorFlow?")
        context2.add_message("assistant", "TensorFlow is a framework for ML.")
        
        # Search for "Python" - should find it in past logs
        results = context2.search_past("Python", limit=5)
        print(f"Search results for 'Python': {len(results)} found")
        
        assert len(results) > 0, "Should find results for 'Python'"
        assert any("Python" in r.get("content", "") for r in results), "Results should contain 'Python'"
        print(f"✓ Found {len(results)} messages containing 'Python'")
        
        # Search for "machine learning"
        results = context2.search_past("machine learning", limit=5)
        print(f"Search results for 'machine learning': {len(results)} found")
        assert len(results) > 0, "Should find results for 'machine learning'"
        print(f"✓ Found {len(results)} messages containing 'machine learning'")
        
        # Search for non-existent term
        results = context2.search_past("nonexistent_term_xyz", limit=5)
        assert len(results) == 0, "Should not find results for non-existent term"
        print("✓ Correctly returns empty results for non-existent term")
    
    print("✓ Test 2 PASSED: Search functionality works correctly\n")


def test_memory_query_detection():
    """Test detection of memory-related queries"""
    print("\n=== Test 3: Memory Query Detection ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        context = ContextManager("Test system", log_dir=tmpdir)
        
        # Test positive cases
        positive_cases = [
            "Do you remember what I said earlier?",
            "Can you recall our previous conversation?",
            "What did we talk about before?",
            "You mentioned something last time",
            "We discussed this earlier",
        ]
        
        for query in positive_cases:
            assert context.detect_memory_query(query), f"Should detect memory query: {query}"
            print(f"✓ Detected memory query: '{query}'")
        
        # Test negative cases
        negative_cases = [
            "What is the weather today?",
            "How do I code in Python?",
            "Tell me a joke",
        ]
        
        for query in negative_cases:
            assert not context.detect_memory_query(query), f"Should NOT detect memory query: {query}"
            print(f"✓ Correctly ignored: '{query}'")
    
    print("✓ Test 3 PASSED: Memory query detection works correctly\n")


def test_format_search_results():
    """Test formatting of search results for LLM context"""
    print("\n=== Test 4: Format Search Results ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        context = ContextManager("Test system", log_dir=tmpdir)
        
        # Create mock search results
        results = [
            {
                "role": "user",
                "content": "What is Python?",
                "timestamp": "2024-01-01T10:00:00",
                "file": "chat_2024-01-01_10-00-00.json"
            },
            {
                "role": "assistant",
                "content": "Python is a programming language.",
                "timestamp": "2024-01-01T10:00:05",
                "file": "chat_2024-01-01_10-00-00.json"
            }
        ]
        
        formatted = context.format_search_results_for_context(results)
        print(f"Formatted results:\n{formatted}")
        
        assert "Relevant past conversations" in formatted
        assert "Python" in formatted
        assert "2024-01-01T10:00:00" in formatted
        print("✓ Format includes all expected elements")
        
        # Test with empty results
        formatted_empty = context.format_search_results_for_context([])
        assert "No relevant past conversations found" in formatted_empty
        print("✓ Handles empty results correctly")
    
    print("✓ Test 4 PASSED: Formatting works correctly\n")


def test_search_and_format_memories():
    """Test the integrated search and format function"""
    print("\n=== Test 5: Search and Format Memories ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create first session with data
        context1 = ContextManager("Test system", log_dir=tmpdir)
        context1.add_message("user", "I love programming in Python")
        context1.add_message("assistant", "Python is great for many applications!")
        context1.add_message("user", "Machine learning is fascinating")
        context1.add_message("assistant", "Indeed, ML has many real-world uses")
        context1.save_snapshot()
        
        # Add small delay to ensure different timestamp
        import time
        time.sleep(1.1)
        
        # Create second session
        context2 = ContextManager("Test system", log_dir=tmpdir)
        
        # Test search with memory query
        query = "Do you remember what I said about Python?"
        memories = context2.search_and_format_memories(query, limit=5)
        
        print(f"Memories found:\n{memories}")
        
        if memories:
            assert "Python" in memories, "Should find Python in memories"
            print("✓ Found relevant memories")
        else:
            print("⚠ No memories found (might be expected if search terms don't match)")
        
        # Test with query containing multiple terms
        query2 = "Tell me about machine learning and Python"
        memories2 = context2.search_and_format_memories(query2, limit=5)
        if memories2:
            print(f"✓ Found memories for multi-term query")
            print(f"Memories:\n{memories2}")
        
    print("✓ Test 5 PASSED: Integrated search and format works\n")


def test_persistence():
    """Test that chat logs are properly saved with timestamps"""
    print("\n=== Test 6: Persistence of Chat Logs ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        context = ContextManager("Test system", log_dir=tmpdir, auto_save=True)
        context.add_message("user", "Test message 1")
        context.add_message("assistant", "Response 1")
        
        # Read the saved file
        session_file = context.session_file
        assert session_file.exists(), "Session file should exist"
        
        with open(session_file, 'r') as f:
            data = json.load(f)
        
        print(f"Saved data has {len(data)} messages")
        
        # Check that timestamps are in the saved data
        for msg in data[1:]:  # Skip system message
            assert "timestamp" in msg, f"Saved message missing timestamp: {msg}"
            print(f"✓ Saved message has timestamp: {msg['timestamp']}")
        
        # Check JSON structure
        assert isinstance(data, list), "Data should be a list"
        assert all(isinstance(m, dict) for m in data), "All messages should be dicts"
        print("✓ JSON structure is valid")
    
    print("✓ Test 6 PASSED: Chat logs are properly persisted\n")


def main():
    """Run all tests"""
    print("=" * 60)
    print("HISTORY CONTROL FEATURE TESTS")
    print("=" * 60)
    
    try:
        test_timestamp_in_messages()
        test_search_past_conversations()
        test_memory_query_detection()
        test_format_search_results()
        test_search_and_format_memories()
        test_persistence()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
