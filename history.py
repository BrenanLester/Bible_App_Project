"""Search history using a fixed-size deque with persistent storage."""
from collections import deque
import json
import os

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")

search_history = deque(maxlen=20)


def _load_history():
    """Load history from JSON file (if exists)."""
    if os.path.isfile(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                search_history.extend(data)
        except Exception as e:
            print(f"⚠️ Failed to load history: {e}")


def _save_history():
    """Save current history to JSON file."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(list(search_history), f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Failed to save history: {e}")


def add_to_history(query: str) -> None:
    if not query:
        return
    search_history.append(query)
    _save_history()


def view_history() -> None:
    if not search_history:
        print("No recent searches.")
        return
    print("\nSearch History:")
    for i, q in enumerate(list(search_history)[::-1], 1):
        print(f"{i}. {q}")


# Automatically load existing history at import
_load_history()
