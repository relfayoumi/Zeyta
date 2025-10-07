# Zeyta Examples

This directory contains example scripts and demonstrations for the Zeyta AI Assistant.

## Available Examples

### History Control Demo
**File:** `demo_history_control.py`

Demonstrates the History Control feature which provides simulated long-term memory for the AI assistant.

**Features demonstrated:**
- Creating chat sessions with timestamped messages
- Searching past conversations
- Memory query detection
- How the LLM can access past conversations

**Usage:**
```bash
python examples/demo_history_control.py
```

**Note:** This is a demonstration script that simulates the feature. For actual use, the feature is integrated into the main conversation loop.

**Documentation:** See [docs/HISTORY_CONTROL.md](../docs/HISTORY_CONTROL.md) for more information.

## Adding New Examples

When adding new example scripts to this directory:

1. Follow the existing code style and structure
2. Include clear docstrings explaining what the example demonstrates
3. Add a section to this README describing the example
4. Ensure the example can be run standalone with minimal dependencies

## Navigation

- [Back to Main README](../README.md)
- [Documentation](../docs/)
- [Testing Tools](../testing/)
