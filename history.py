import json
import os
from collections import deque

class SearchHistory:
    def __init__(self, history_path="history.json"):
        self.history_path = history_path
        self.history = deque()   # No maxlen, unlimited size
        self.load_history()

    # === Load existing history from file ===
    def load_history(self):
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.history = deque(data)  # No limit
            except json.JSONDecodeError:
                self.history = deque()
        else:
            self.history = deque()

    # === Save current history to file ===
    def save_history(self):
        try:
            with open(self.history_path, "w", encoding="utf-8") as f:
                json.dump(list(self.history), f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving history: {e}")

    # === Add new search query ===
    def add(self, query):
        """Add query to history with error handling."""
        try:
            if not query or not query.strip():
                return False
            
            if query not in self.history:
                self.history.appendleft(query)
                self.save_history()
                return True
            return False
        except Exception as e:
            print(f"⚠️  Error adding to history: {e}")
            return False

    def list_all(self):
        """Return all history items safely."""
        try:
            return list(self.history)
        except Exception as e:
            print(f"⚠️  Error retrieving history: {e}")
            return []

    # === Update an entry ===
    def update(self, old_query, new_query):
        try:
            idx = self.history.index(old_query)
            self.history[idx] = new_query
            self.save_history()
            return True
        except ValueError:
            return False
        except Exception as e:
            print(f"⚠️  Error updating history: {e}")
            return False

    # === Delete an entry ===
    def delete(self, query):
        try:
            self.history.remove(query)
            self.save_history()
            return True
        except ValueError:
            return False
        except Exception as e:
            print(f"⚠️  Error deleting from history: {e}")
            return False

    # === Clear all history ===
    def clear(self):
        """Clear history with error handling."""
        try:
            self.history.clear()
            self.save_history()
            return True
        except Exception as e:
            print(f"⚠️  Error clearing history: {e}")
            return False