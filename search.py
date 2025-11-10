import re
import os
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from bible_parser_json import JSONBibleParser
from ascii_art import SEARCH_ART
from history import SearchHistory

# Create a function to add to history
def add_to_search_history(query):
    history = SearchHistory()
    history.add(query)

# === Colors (ANSI) ===
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RESET  = "\033[0m"
CYAN   = "\033[96m"

# === Input style for placeholder ===
style = Style.from_dict({'placeholder': '#888888 italic'})

# === Highlight matches (exact word only) ===
def highlight_all(text, words):
    for word in words:
        if word.strip():
            text = re.sub(
                fr"(?i)\b({re.escape(word)})\b",
                f"{GREEN}\\1{RESET}",
                text
            )
    return text

# === Validate input ===
def is_valid_reference(query):
    return bool(re.fullmatch(r"[A-Za-z0-9 ':]+", query.strip()))

# === Search function ===
def search_bible(bible, query):
    results = []
    words = query.lower().strip().split()

    # Case 1: Exact verse search (e.g., Genesis 2:2)
    if len(words) >= 2 and ":" in words[1]:
        book_query = words[0]
        chap_verse = words[1].split(":")
        if len(chap_verse) == 2 and chap_verse[0].isdigit() and chap_verse[1].isdigit():
            chapter_query, verse_query = chap_verse
            for book, chapters in bible.items():
                if book.lower().startswith(book_query) and chapter_query in chapters:
                    if verse_query in chapters[chapter_query]:
                        text = chapters[chapter_query][verse_query]
                        results.append((book, chapter_query, verse_query, text, True))
                        return results
        else:
            print("❌ Invalid format! Use: Genesis 2:2 (book chapter:verse).")
            return []

    # Case 2: Normal keyword or book search (exact words only)
    for book, chapters in bible.items():
        book_match = any(re.search(fr"\b{re.escape(w)}\b", book.lower()) for w in words)
        for chapter, verses in chapters.items():
            for verse, text in verses.items():
                text_match = any(re.search(fr"\b{re.escape(w)}\b", text.lower()) for w in words)
                if book_match or text_match:
                    results.append((book, chapter, verse, text, book_match))
    return results

# === Show results in pages (10 at a time) ===
def show_paginated_results(found, words):
    PAGE_SIZE = 10
    total = len(found)
    index = 0

    while index < total:
        end = min(index + PAGE_SIZE, total)
        for book, chap, verse, text, book_match in found[index:end]:
            display_book = highlight_all(book, words) if book_match else book
            display_chap = highlight_all(str(chap), words)
            display_verse = highlight_all(str(verse), words)
            display_text = highlight_all(text, words)
            print(f"{CYAN}{display_book} {display_chap}:{display_verse}{RESET}")
            print(display_text + "\n")

        index += PAGE_SIZE
        if index < total:
            remaining = total - index
            cont = input(f"🔽 Press Enter to see next {min(PAGE_SIZE, remaining)} results (or type 'q' to stop): ")
            if cont.lower() == 'q':
                break
        else:
            print(f"✅ End of results. Displayed all {total} matches.\n")

            # === Show results in pages with bookmarking option after each page ===
def show_paginated_results_with_bookmarking(found, words):
    PAGE_SIZE = 10
    total = len(found)
    index = 0

    while index < total:
        end = min(index + PAGE_SIZE, total)
        
        # Show current page
        print(f"\n{GREEN}=== Page {(index // PAGE_SIZE) + 1} ==={RESET}")
        for i, (book, chap, verse, text, book_match) in enumerate(found[index:end], index + 1):
            display_book = highlight_all(book, words) if book_match else book
            display_chap = highlight_all(str(chap), words)
            display_verse = highlight_all(str(verse), words)
            display_text = highlight_all(text, words)
            print(f"{i}. {display_book} {display_chap}:{display_verse}{RESET}")
            print(display_text + "\n")

        # Offer bookmarking for current page
        bookmark_choice = input(f"{GREEN}Bookmark from this page? (y/n/next/q to quit): {RESET}").strip().lower()
        
        if bookmark_choice == 'q':
            return True  # Return to search menu
        elif bookmark_choice == 'y':
            try:
                start_num = index + 1
                end_num = end
                idx = int(input(f"{GREEN}Enter result number to bookmark ({start_num}-{end_num}): {RESET}"))
                if start_num <= idx <= end_num:
                    book, chap, verse, text, _ = found[idx - 1]
                    from bookmarks import add_bookmark
                    add_bookmark(book, f"{chap}:{verse}", text)
                    print("✅ Bookmark added!")
                else:
                    print(f"❌ Please enter a number between {start_num} and {end_num}.")
            except ValueError:
                print("❌ Please enter a valid number.")
        elif bookmark_choice == 'next':
            # Continue to next page without bookmarking
            pass
        # If 'n', just continue to next page
        
        index += PAGE_SIZE
        if index >= total:
            print(f"✅ End of results. Displayed all {total} matches.\n")
            break

    return False  # Continue in search interface

# === Bookmark handling in search results ===
def handle_bookmark_selection(results, words):
    # Show only first 10 results for bookmarking
    display_count = min(10, len(results))
    
    print(f"\n{GREEN}=== Search Results (First {display_count} shown) ==={RESET}")
    for i, (book, chap, verse, text, book_match) in enumerate(results[:display_count], 1):
        display_book = highlight_all(book, words) if book_match else book
        display_chap = highlight_all(str(chap), words)
        display_verse = highlight_all(str(verse), words)
        print(f"{i}. {display_book} {display_chap}:{display_verse}")
        print(f"   {text}\n")
    
    # Ask if user wants to bookmark
    bookmark_choice = input(f"{GREEN}Bookmark a result? (y/n/q to quit): {RESET}").strip().lower()
    
    if bookmark_choice == 'q':
        return True  # Return to search menu
    
    if bookmark_choice == 'y':
        try:
            idx = int(input(f"{GREEN}Enter result number to bookmark (1-{display_count}): {RESET}"))
            if 1 <= idx <= display_count:
                book, chap, verse, text, _ = results[idx - 1]
                from bookmarks import add_bookmark
                add_bookmark(book, f"{chap}:{verse}", text)
                print("✅ Bookmark added!")
            else:
                print(f"❌ Please enter a number between 1 and {display_count}.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    return False  # Continue in search interface

# === Main Search Interface ===
def search_interface(bible):
    print(CYAN + SEARCH_ART + RESET)
    print(f"{CYAN}📖 Bible Search — KJV Edition{RESET}")
    print("Search by keyword(s), book name, or exact reference (e.g., Genesis 2:2).")
    print("Exact word matching is enabled. Press 'q' to return to main menu.\n")

    while True:
        # Inline placeholder beside 🔍
        query = prompt(
            'Search🔍:  ',
            placeholder='ex:Genesis 1:1 or love... (or "q" to quit)',
            style=style
        ).strip()

        if query.lower() == "q":
            print(f"{CYAN}Returning to main menu...{RESET}")
            return True  # Signal to return to main menu

        if not query:
            continue

        if not is_valid_reference(query):
            print("❌ Invalid input! Only letters, numbers, spaces, and ':' are allowed.\n")
            continue

        # Add to search history
        add_to_search_history(query)
        
        found = search_bible(bible, query)
        if not found:
            print("❌ No results found.\n")
        else:
            words = query.split()
            # Show paginated results with bookmarking option after each page
            should_return = show_paginated_results_with_bookmarking(found, words)
            if should_return:
                return True  # Return to main menu if user pressed 'q'

# === Standalone execution (for testing) ===
if __name__ == "__main__":
    print("Loading Bible...")
    json_path = os.path.join(os.path.dirname(__file__), "kjv.json")
    parser = JSONBibleParser(json_path)
    bible_data = parser.load()
    print(f"✅ Bible loaded! {len(bible_data)} books ready.\n")
    search_interface(bible_data)