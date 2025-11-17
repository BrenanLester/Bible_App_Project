import json
import os
import os
import json
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

        # === Display history in table format ===
    def display_table(self):
        """Display search history in a beautiful table format."""
        CYAN = "\033[96m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        CREAM = "\033[38;5;230m"
        RESET = "\033[0m"
        RED = "\033[91m"
        
        history_items = self.list_all()
        
        if not history_items:
            # Center "no history" message
            terminal_width = 200
            no_history_msg = "No search history found."
            no_history_padding = (terminal_width - len(no_history_msg)) // 2
            print(f"{' ' * no_history_padding}{RED}{no_history_msg}{RESET}")
            return False  # Return False to indicate no history
            
        
        # Set terminal width to 120
        terminal_width = 166
        table_width = 96  # Fixed width for perfect alignment
        
        # Center the table
        border_padding = (terminal_width - table_width) // 2
        
        # Print table header
        print(f"{' ' * border_padding}{CYAN}┌{'─' * 146}┐{RESET}")
        print(f"{' ' * border_padding}{CYAN}│{RESET}{YELLOW}{' SEARCH HISTORY ':^146}{RESET}{CYAN}│{RESET}")
        print(f"{' ' * border_padding}{CYAN}├{'─' * 146}┤{RESET}")
        print(f"{' ' * border_padding}{CYAN}│{RESET}{GREEN} {'No.':<4}{CREAM}│{' WORD / VERSE  ':<139} {RESET}{CYAN}│{RESET}")
        print(f"{' ' * border_padding}{CYAN}├{'─' * 146}┤{RESET}")

        # Print history items from JSON data
        for i, query in enumerate(history_items, 1):
            # Truncate long queries to fit table
            display_query = query if len(query) <= 138 else query[:135] + "..."
            print(f"{' ' * border_padding}{CYAN}│{RESET}{GREEN} {i:<4}{CREAM}│ {display_query:<139}{RESET}{CYAN}│{RESET}")

        # Print table footer
        print(f"{' ' * border_padding}{CYAN}└{'─' * 146}┘{RESET}")
        print(f"{' ' * border_padding}{GREEN}Total searches: {len(history_items)}{RESET}")

        return True
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

# For backward compatibility
def view_history():
    history = SearchHistory()
    history.display_table()


    
