"""Bookmarks Manager — uses OrderedDict for O(1) lookup and stable order.

This module:
- Stores bookmarks in memory and in a JSON file.
- Allows adding, viewing, and removing bookmarks.
- Auto-saves bookmarks so they persist between runs.
"""

import json
import os
from ascii_art import BOOKMARK_ART
from collections import OrderedDict
import shutil
import re

def get_terminal_width():
    """Get the current terminal width."""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80  # Default fallback width

def strip_colors(text):
    """Remove ANSI color codes for length calculation."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def center_content(content, is_multiline=False):
    """Center content in the terminal."""
    terminal_width = get_terminal_width()
    
    if is_multiline:
        # For multiline content like ASCII art
        lines = content.split('\n')
        centered_lines = []
        
        for line in lines:
            clean_line = strip_colors(line)
            padding = (terminal_width - len(clean_line)) // 2
            centered_lines.append(" " * max(0, padding) + line)
        
        return '\n'.join(centered_lines)
    else:
        # For single line content
        clean_content = strip_colors(content)
        padding = (terminal_width - len(clean_content)) // 2
        return " " * max(0, padding) + content

# JSON file for saving bookmarks
BOOKMARKS_FILE = os.path.join(os.path.dirname(__file__), "bookmarks.json")

# In-memory bookmarks structure
_bookmarks = OrderedDict()

# === Colors (ANSI) ===
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RESET  = "\033[0m"
CYAN   = "\033[96m"
RED    = "\033[91m"

def _make_key(book, reference):
    """Create a unique key for each verse."""
    return f"{book} {reference}".strip()


def _load_bookmarks():
    """Load bookmarks from JSON file (if exists)."""
    try:
        if os.path.isfile(BOOKMARKS_FILE):
            try:
                with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        print(f"{RED}⚠️  Warning: Invalid bookmarks format. Starting fresh.{RESET}")
                        return
                    
                    for item in data:
                        # Validate item structure
                        if not isinstance(item, dict) or "book" not in item or "reference" not in item or "text" not in item:
                            print(f"{RED}⚠️  Warning: Skipping invalid bookmark entry.{RESET}")
                            continue
                        
                        key = _make_key(item["book"], item["reference"])
                        _bookmarks[key] = (item["book"], item["reference"], item["text"])
            except json.JSONDecodeError as e:
                print(f"{RED}⚠️  Failed to load bookmarks (JSON error): {e}{RESET}")
                _bookmarks.clear()
            except Exception as e:
                print(f"{RED}⚠️  Failed to load bookmarks: {e}{RESET}")
                _bookmarks.clear()
    except Exception as e:
        print(f"{RED}⚠️  Unexpected error loading bookmarks: {e}{RESET}")


def _save_bookmarks():
    """Save current bookmarks to JSON file."""
    try:
        with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
            data = [
                {"book": b, "reference": r, "text": t}
                for b, r, t in _bookmarks.values()
            ]
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"{RED}⚠️  Failed to save bookmarks (file error): {e}{RESET}")
    except Exception as e:
        print(f"{RED}⚠️  Failed to save bookmarks: {e}{RESET}")


def add_bookmark(book, reference, verse_text):
    """Add a bookmark and save it permanently."""
    try:
        if not book or not reference or not verse_text:
            print(f"{RED}❌ Error: Bookmark data cannot be empty.{RESET}")
            return False
        
        key = _make_key(book, reference)
        _bookmarks[key] = (book, reference, verse_text)
        _save_bookmarks()
        print(f"✅ {GREEN}Bookmarked: {book} {reference}{RESET}")
        return True
    except Exception as e:
        print(f"{RED}❌ Error adding bookmark: {e}{RESET}")
        return False


def view_bookmarks():
    """Display all saved bookmarks with full verse text (no truncation)."""
    try:
        # Manually adjust ASCII art position
        manual_padding = 50  # ← CHANGE THIS NUMBER TO ADJUST POSITION
        lines = BOOKMARK_ART.split('\n')
        for line in lines:
            print(" " * manual_padding + f"{YELLOW}{line}{RESET}")
        
        if not _bookmarks:
            # Manually adjust "No bookmarks" position
            manual_padding = 90  # ← CHANGE THIS NUMBER TO ADJUST POSITION
            print(" ")
            print(" " * manual_padding + f"{YELLOW}No bookmarks yet.{RESET}")
            print(" " * manual_padding + f"{CYAN}══════════════════════════════════════════════════{RESET}")
            return
            
        # Center the bookmark count header
        print(center_content(f"\n{YELLOW} Your Saved Bookmarks ({len(_bookmarks)} total):{RESET}"))
        
        # Create a centered content area
        terminal_width = get_terminal_width()
        content_width = min(240, terminal_width - 5)  # Content width with margins
        border_line = f"{CYAN}{'─' * content_width}{RESET}"
        
        # Calculate padding for the content block
        content_padding = (terminal_width - content_width) // 2
        
        print(" " * content_padding + border_line)
        
        for i, (key, value) in enumerate(_bookmarks.items(), 1):
            book, reference, text = value
            
            # Bookmark header - number stays on left within centered block
            bookmark_header = f"{i}. {CYAN}{book} {reference}{RESET}"
            # Pad to create centered block with left-aligned content
            header_clean = strip_colors(bookmark_header)
            available_width = content_width - len(header_clean)
            print(" " * content_padding + bookmark_header)
            
            # Verse text - also within the centered block
            verse_display = f"   {GREEN}{text}{RESET}"
            print(" " * content_padding + verse_display)
            
            # Border between bookmarks
            print(" " * content_padding + border_line)
            
    except Exception as e:
        print(f"{RED}❌ Error viewing bookmarks: {e}{RESET}")


def remove_bookmark(index=None, key=None):
    """Remove a bookmark by index or key."""
    try:
        if key is not None:
            if key in _bookmarks:
                removed = _bookmarks.pop(key)
                _save_bookmarks()
                print(f"🗑️  {RED}Removed: {removed[0]} {removed[1]}{RESET}")
                return True
            else:
                print(f"{RED}❌ Bookmark key not found.{RESET}")
                return False

        if index is None:
            print(f"{RED}❌ Provide index or key to remove.{RESET}")
            return False

        if not isinstance(index, int) or index < 1:
            print(f"{RED}❌ Invalid bookmark index.{RESET}")
            return False

        keys = list(_bookmarks.keys())
        if index > len(keys):
            print(f"{RED}❌ Invalid bookmark number. Valid range: 1-{len(keys)}{RESET}")
            return False
        
        real_key = keys[index - 1]
        removed = _bookmarks.pop(real_key)
        _save_bookmarks()
        print(f"🗑️  {RED}Removed: {removed[0]} {removed[1]}{RESET}")
        return True
    except IndexError:
        print(f"{RED}❌ Invalid bookmark number.{RESET}")
        return False
    except Exception as e:
        print(f"{RED}❌ Error removing bookmark: {e}{RESET}")
        return False


def clear_all_bookmarks():
    """
    Clear all bookmarks with confirmation.
    
    Returns:
        bool: True if cleared, False if cancelled
    """
    try:
        if not _bookmarks:
            print(f"{YELLOW}⚠️  No bookmarks to clear.{RESET}")
            return False
        
        # Confirmation prompt
        confirm = input(f"{RED}⚠️  This will DELETE all {len(_bookmarks)} bookmarks! Are you sure? (y/n): {RESET}").strip().lower()
        
        if confirm == 'y':
            _bookmarks.clear()
            _save_bookmarks()
            print(f"{GREEN}✅ All bookmarks cleared successfully!{RESET}")
            return True
        else:
            print(f"{YELLOW}❎ Bookmark clearing cancelled.{RESET}")
            return False
    except Exception as e:
        print(f"{RED}❌ Error clearing bookmarks: {e}{RESET}")
        return False


# Automatically load existing bookmarks at import
_load_bookmarks()
