import os
import json
from config import HISTORY_FILE, PATHS

def load_history():
    """Load conversation history from JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception as e:
        print(f"[HistoryManager] Warning: Failed to load history ({e}). Resetting.")
        return []

def save_history(history):
    """Save conversation history to JSON file."""
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[HistoryManager] Error saving history: {e}")
        return False

def clear_history():
    """Clear saved conversation history."""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        return True
    except Exception as e:
        print(f"[HistoryManager] Error clearing history: {e}")
        return False
