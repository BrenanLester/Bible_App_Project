"""Bookmarks Manager — uses OrderedDict for O(1) lookup and stable order.

This module:
- Stores bookmarks in memory and in a JSON file.
- Allows adding, viewing, and removing bookmarks.
- Auto-saves bookmarks so they persist between runs.
"""

import json
import os
from collections import OrderedDict

# JSON file for saving bookmarks
BOOKMARKS_FILE = os.path.join(os.path.dirname(__file__), "bookmarks.json")

# In-memory bookmarks structure
_bookmarks = OrderedDict()


def _make_key(book, reference):
    """Create a unique key for each verse."""
    return f"{book} {reference}".strip()


def _load_bookmarks():
    """Load bookmarks from JSON file (if exists)."""
    if os.path.isfile(BOOKMARKS_FILE):
        try:
            with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    key = _make_key(item["book"], item["reference"])
                    _bookmarks[key] = (item["book"], item["reference"], item["text"])
        except Exception as e:
            print(f"⚠️ Failed to load bookmarks: {e}")


def _save_bookmarks():
    """Save current bookmarks to JSON file."""
    try:
        with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
            data = [
                {"book": b, "reference": r, "text": t}
                for b, r, t in _bookmarks.values()
            ]
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Failed to save bookmarks: {e}")


def add_bookmark(book, reference, verse_text):
    """Add a bookmark and save it permanently."""
    key = _make_key(book, reference)
    _bookmarks[key] = (book, reference, verse_text)
    _save_bookmarks()
    print(f"✅ Bookmarked: {book} {reference}")


def view_bookmarks():
    """Display all saved bookmarks."""
    if not _bookmarks:
        print("\nNo bookmarks yet.")
        return
    print("\n📚 Your Bookmarks:")
    for i, (key, value) in enumerate(_bookmarks.items(), 1):
        book, reference, text = value
        print(f"{i}. {book} {reference} - {text}")


def remove_bookmark(index=None, key=None):
    """Remove a bookmark by index or key."""
    try:
        if key is not None:
            if key in _bookmarks:
                removed = _bookmarks.pop(key)
                _save_bookmarks()
                print(f"🗑️ Removed: {removed[0]} {removed[1]}")
                return True
            print("Bookmark key not found.")
            return False

        if index is None:
            print("Provide index or key to remove.")
            return False

        keys = list(_bookmarks.keys())
        real_key = keys[index - 1]
        removed = _bookmarks.pop(real_key)
        _save_bookmarks()
        print(f"🗑️ Removed: {removed[0]} {removed[1]}")
        return True
    except IndexError:
        print("Invalid bookmark number.")
        return False


# Automatically load existing bookmarks at import
_load_bookmarks()
