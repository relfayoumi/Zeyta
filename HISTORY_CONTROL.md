# History Control Feature

## Overview

The History Control feature provides **simulated long-term memory** for the AI assistant by automatically saving chat conversations with timestamps and enabling intelligent search and retrieval of past conversations.

## Features

### 1. **Timestamped Chat Logs**
Every message in a conversation is automatically saved with:
- **Role** (user/assistant/system)
- **Content** (the actual message)
- **Timestamp** (ISO 8601 format: `2024-01-01T10:30:45.123456`)
- **Session File** (unique file per conversation session)

Example chat log entry:
```json
{
  "role": "user",
  "content": "What is Python?",
  "timestamp": "2024-01-01T10:30:45.123456"
}
```

### 2. **Automatic Memory Query Detection**
The system automatically detects when users are asking about past conversations using keywords such as:
- "remember"
- "recall"
- "what did"
- "earlier"
- "before"
- "previous"
- "last time"
- "you said"
- "we talked about"
- "mentioned"
- "discussed"
- "conversation about"

### 3. **Intelligent Past Conversation Search**
When a memory query is detected, the system:
1. Extracts key terms from the user's query
2. Searches all past chat log files
3. Returns relevant messages with timestamps
4. Formats results for LLM context injection

### 4. **Transparent LLM Integration**
The feature works seamlessly with the existing LLM:
- Detects memory queries automatically
- Searches past conversations
- Injects relevant context into the LLM's message history
- The LLM can then reference past conversations in its responses

## Configuration

### Enable/Disable the Feature

In `config.py`, set:

```python
# Enable automatic history search when memory keywords are detected
ENABLE_HISTORY_SEARCH = True  # Set to False to disable

# Maximum number of past messages to retrieve
CHAT_QUERY_MAX_RESULTS = 5

# Directory where chat logs are stored
CHAT_LOG_DIR = "chat_logs"
```

### Default Configuration

By default, the feature is **enabled** (`ENABLE_HISTORY_SEARCH = True`). If the configuration option is missing, the feature defaults to enabled.

## How It Works

### Workflow

```
1. User asks: "Do you remember what I said about Python?"
   ↓
2. System detects "remember" keyword → Memory query detected
   ↓
3. System extracts key terms: ["Python"]
   ↓
4. System searches past chat logs for messages containing "Python"
   ↓
5. Results formatted with timestamps:
   "[2024-01-01T10:00:00] user: I'm learning Python programming."
   ↓
6. Context injected into LLM as a system message:
   "[MEMORY RECALL]
   Relevant past conversations:
   1. [2024-01-01T10:00:00] user: I'm learning Python programming.
   2. [2024-01-01T10:00:05] assistant: That's great! Python is excellent..."
   ↓
7. LLM generates response using past context:
   "Yes, I remember! You mentioned you were learning Python programming..."
```

### Chat Log Storage

Chat logs are stored in the `chat_logs/` directory (configurable):
```
chat_logs/
├── chat_2024-01-01_10-30-45.json  # Session 1
├── chat_2024-01-01_14-22-10.json  # Session 2
└── chat_2024-01-02_09-15-33.json  # Session 3
```

Each file contains a complete conversation session with timestamped messages.

## API Reference

### ContextManager Methods

#### `add_message(role: str, content: str) -> None`
Adds a message to the current session with automatic timestamp.

```python
context.add_message("user", "Hello, AI!")
# Automatically adds timestamp
```

#### `search_past(term: str, limit: int = 5) -> List[Dict]`
Searches past conversations for messages containing the term.

```python
results = context.search_past("Python", limit=5)
# Returns: [{"role": "user", "content": "...", "timestamp": "...", "file": "..."}, ...]
```

#### `detect_memory_query(user_input: str) -> bool`
Detects if a user's input is asking about past conversations.

```python
is_memory = context.detect_memory_query("Do you remember what I said?")
# Returns: True
```

#### `search_and_format_memories(query: str, limit: int = 5) -> Optional[str]`
Searches past conversations and formats results for LLM context.

```python
memories = context.search_and_format_memories("What did we discuss about Python?", limit=5)
# Returns formatted string with past conversations
```

#### `format_search_results_for_context(results: List[Dict]) -> str`
Formats search results into a readable string for the LLM.

```python
formatted = context.format_search_results_for_context(results)
# Returns: "Relevant past conversations:\n1. [timestamp] role: content\n..."
```

## Usage Examples

### Example 1: Basic Memory Query

**User:** "Do you remember what I asked you about yesterday?"

**System:**
1. Detects "remember" keyword
2. Searches past logs for relevant content
3. Injects past conversations into context
4. LLM responds with reference to past conversations

### Example 2: Specific Topic Recall

**User:** "Can you recall our conversation about machine learning?"

**System:**
1. Detects "recall" and "conversation about" keywords
2. Extracts "machine learning" as search term
3. Finds all messages containing "machine learning"
4. Formats and injects into LLM context
5. LLM provides answer based on past discussions

### Example 3: Multiple Topics

**User:** "What did we discuss about Python and AI?"

**System:**
1. Detects "what did" and "discuss" keywords
2. Extracts "Python" and "AI" as search terms
3. Searches for both terms
4. Returns combined results
5. LLM references both topics from past conversations

## Testing

### Run Tests

```bash
python tests/test_history_control.py
```

### Run Demonstration

```bash
python demo_history_control.py
```

The demonstration script shows:
- Chat logging with timestamps
- Searching past conversations
- Memory query detection
- Memory formatting for LLM
- Complete workflow explanation

## Technical Details

### Message Structure

```python
{
    "role": "user" | "assistant" | "system",
    "content": "The message text",
    "timestamp": "2024-01-01T10:30:45.123456"  # ISO 8601 format
}
```

### Search Algorithm

1. **Query Processing:**
   - Extract words longer than 3 characters
   - Use as search terms

2. **File Traversal:**
   - Search past logs in reverse chronological order (newest first)
   - Skip current session file

3. **Matching:**
   - Case-insensitive content matching
   - Limit results to prevent overwhelming the LLM

4. **Result Formatting:**
   - Include timestamp, role, and content
   - Maintain chronological order

### LLM Context Injection

When a memory query is detected, the system injects a special system message:

```python
{
    "role": "system",
    "content": "[MEMORY RECALL]\n<formatted memories>\n\nUse the above past conversation context to answer the user's question if relevant."
}
```

This is inserted just before the user's question, allowing the LLM to reference the past context.

## Performance Considerations

- **File I/O:** Past logs are read on-demand only when memory queries are detected
- **Search Efficiency:** Searches stop after finding the requested number of results
- **Context Size:** Limited to `CHAT_QUERY_MAX_RESULTS` to prevent token overflow
- **Current Session:** Current session file is excluded from "past" searches

## Backwards Compatibility

The feature is fully backwards compatible:
- Existing chat logs without timestamps still work
- The `timestamp` field is optional when reading logs
- Existing code that doesn't use the feature continues to work
- The `Brain` class accepts an optional `context_manager` parameter (defaults to `None`)

## Future Enhancements

Potential improvements:
- Semantic search using embeddings
- Summary-based memory (condense old conversations)
- User-triggered memory save points
- Memory importance scoring
- Configurable keyword sets
- Vector database integration for large-scale memory

## Troubleshooting

### Issue: Memory queries not detected

**Solution:** Check that keywords are in the user's input. Add custom keywords by modifying `detect_memory_query()` in `core/context.py`.

### Issue: No past conversations found

**Solution:** Ensure chat logs exist in the `CHAT_LOG_DIR` directory. The current session is excluded from searches.

### Issue: Feature not working

**Solution:** Verify `ENABLE_HISTORY_SEARCH = True` in `config.py` and that the `Brain` is initialized with the `context_manager` parameter.

## License

This feature is part of the Zeyta project and follows the same license.

## Contributing

To contribute improvements to the History Control feature:
1. Add tests to `tests/test_history_control.py`
2. Update this documentation
3. Submit a pull request

---

**Note:** This feature provides simulated long-term memory by searching past conversation logs. It does not modify or merge past conversations into the current session - it only provides relevant context when needed.
