<<<<<<< HEAD
"""Terminal-Based Bible App using JSON Bible data.

This version reads `kjv.json` and includes:
- Verse Search (with algorithm in search.py)
- Bookmarks (add, view, remove)
- Verse of the Day (random)
- Search History (queue)
- Browse feature with Book → Chapter → Verse hierarchy
"""

import os
import time
from bible_parser_json import JSONBibleParser
from search import search_bible
from bookmarks import add_bookmark, view_bookmarks, remove_bookmark
from history import add_to_history, view_history
from verse_of_the_day import verse_of_the_day

def main():
=======
"""Terminal-Based Bible App using JSON Bible data."""
import os
import time
import sys
from bible_parser_json import JSONBibleParser
from bookmarks import add_bookmark, view_bookmarks, remove_bookmark
from verse_of_the_day import verse_of_the_day
from ascii_art import HEADER_ART  # ← IMPORT FROM NEW FILE

# === CORE FUNCTIONS ===
def typewriter(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_section_header(title):
    """Show header with a section title"""
    clear_screen()
    show_header()
    CYAN = "\033[96m"
    RESET = "\033[0m"
    print(CYAN + f"\n╔════════════════════════════╗")
    print(f"║      {title:^16}      ║")
    print(f"╚════════════════════════════╝" + RESET)

# === Styled Terminal Header ===
def show_header():
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    
    lines = HEADER_ART.split('\n')
    
    for line in lines:
        if any(pattern in line for pattern in ['╔╗', '╠╩╗', '╚═╝', '8888', '888888']):
            # This is a text line - make it white with cyan borders
            if line.startswith(" / /\\"):
                print(CYAN + " / /\\" + WHITE + line[5:-5] + CYAN + "/ /\\ " + RESET)
            elif line.startswith("/ /\\ \\"):
                print(CYAN + "/ /\\ \\" + WHITE + line[6:-6] + CYAN + "/ /\\ \\" + RESET)
            elif line.startswith("\\ \\/ /"):
                print(CYAN + "\\ \\/ /" + WHITE + line[6:-6] + CYAN + "\\ \\/ /" + RESET)
            elif line.startswith(" \\/ /"):
                print(CYAN + " \\/ / " + WHITE + line[5:-5] + CYAN + " \\/ / " + RESET)
            else:
                print(WHITE + line + RESET)
        else:
            # This is a border line - make it cyan
            print(CYAN + line + RESET)

# === MAIN APPLICATION ===
def main():
    show_header()

>>>>>>> 738c17f541b87184a916976e82abde23c6fb46d2
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_candidate = os.path.join(script_dir, 'kjv.json')

    parser = JSONBibleParser(json_candidate)
    try:
        bible = parser.load()
    except Exception as e:
        print('Failed to load JSON Bible:', e)
        return

<<<<<<< HEAD
    # === 🕊️ Show Verse of the Day at startup ===
    print("\n📖 Verse of the Day 📖")
    print(verse_of_the_day(bible))
    print("\n========================")

    while True:
        print('\n=== JSON Bible App ===')
        print('[1] Search Verse')
        print('[2] Browse')
        print('[3] View / Remove Bookmarks')
        print('[4] Search History')
        print('[5] Exit')

        choice = input('Enter choice: ').strip()

        # === Option 1: Search Verse ===
        if choice == "1":
=======
    # === VERSE OF THE DAY ===
    print("\n📖 Verse of the Day 📖\n")
    
    votd = verse_of_the_day(bible)
    print("\n")
    typewriter(f"📖 {votd}", delay=0.08)
  

    # Wait and clear screen
    GREEN = "\033[92m"
    RESET = "\033[0m"
    CYAN = "\033[96m"
    input(f"{GREEN}\n\n\nWELCOME TO BIBLE TERMINAL EDITION! FOR MAIN MENU CLICK \"ENTER\"{RESET}")
    clear_screen()
    show_header()

    while True:
        # === MAIN MENU ===
        GREEN = "\033[92m"
        RESET = "\033[0m"
        CYAN = "\033[96m"

        print(CYAN + "\n╔════════════════════════════╗" )
        print("║        MAIN  MENU          ║")
        print("╚════════════════════════════╝"+RESET)

        print(f"{GREEN}[1]{RESET} Search Verse")
        print(f"{GREEN}[2]{RESET} Browse")
        print(f"{GREEN}[3]{RESET} View / Remove Bookmarks")
        print(f"{GREEN}[4]{RESET} Search History")
        print(f"{GREEN}[5]{RESET} Exit")

        choice = input('\nEnter choice: ').strip()

        if choice == "1":
            show_section_header("SEARCH VERSE")
            from search import search_bible
            from history import add_to_history
>>>>>>> 738c17f541b87184a916976e82abde23c6fb46d2
            query = input("Enter keyword or phrase: ").strip()
            add_to_history(query)
            results = search_bible(bible, query)
            if results:
                for i, (book, ref, text) in enumerate(results, 1):
                    print(f"{i}. {book} {ref} - {text}")
<<<<<<< HEAD
                if input("Bookmark a result? (y/n): ").strip().lower() == "y":
=======
                if input("\nBookmark a result? (y/n): ").strip().lower() == "y":
>>>>>>> 738c17f541b87184a916976e82abde23c6fb46d2
                    try:
                        idx = int(input("Number to bookmark: "))
                        if 1 <= idx <= len(results):
                            book, ref, text = results[idx - 1]
                            add_bookmark(book, ref, text)
<<<<<<< HEAD
                        else:
                            print("Invalid number.")
=======
                            print("✅ Bookmark added!")
>>>>>>> 738c17f541b87184a916976e82abde23c6fb46d2
                    except ValueError:
                        print("Invalid input.")
            else:
                print("No results found.")
<<<<<<< HEAD

        # === Option 2: Browse Bible ===
        elif choice == "2":
            browse_bible(bible, parser)

        # === Option 3: Bookmarks ===
        elif choice == "3":
            view_bookmarks()
            if input("Remove a bookmark? (y/n): ").strip().lower() == "y":
                try:
                    num = int(input("Enter bookmark number: "))
                    remove_bookmark(num)
                except ValueError:
                    print("Invalid input.")

        # === Option 4: Verse of the Day ===
        elif choice == "4":
            verse_of_the_day(bible)

        # === Option 5: Search History ===
        elif choice == "5":
            view_history()

        # === Option 6: Exit ===
        elif choice == "6":
            print("👋 Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid menu number.")


# --- New Feature: Browse Bible ---
=======
            input(f"\n{GREEN}Press Enter to return to main menu...{RESET}")
            clear_screen()
            show_header()

        elif choice == "2":
            show_section_header("BROWSE BIBLE")
            browse_bible(bible, parser)
            input(f"\n{GREEN}Press Enter to return to main menu...{RESET}")
            clear_screen()
            show_header()

        elif choice == "3":
            show_section_header("BOOKMARKS")
            view_bookmarks()
            if input("\nRemove a bookmark? (y/n): ").strip().lower() == "y":
                try:
                    num = int(input("Enter bookmark number: "))
                    remove_bookmark(num)
                    print("✅ Bookmark removed!")
                except ValueError:
                    print("Invalid input.")
            input(f"\n{GREEN}Press Enter to return to main menu...{RESET}")
            clear_screen()
            show_header()

        elif choice == "4":
            show_section_header("SEARCH HISTORY")
            from history import view_history
            view_history()
            input(f"\n{GREEN}Press Enter to return to main menu...{RESET}")
            clear_screen()
            show_header()

        elif choice == "5":
            clear_screen()
            show_header()
            print(f"\n{GREEN}👋 Thank you for using Bible Terminal Edition! Goodbye!{RESET}")
            break

        else:
            print("Invalid choice.")
            time.sleep(1)
            clear_screen()
            show_header()

# === BROWSE BIBLE FUNCTION ===
>>>>>>> 738c17f541b87184a916976e82abde23c6fb46d2
def browse_bible(bible, parser):
    print("\n📖 Browse the Bible 📖")
    books = list(bible.keys())

    # Step 1: Choose Book
    for i, book in enumerate(books, 1):
        print(f"[{i}] {book}")
    try:
        book_index = int(input("\nChoose a book number: "))
        if not (1 <= book_index <= len(books)):
            print("Invalid book number.")
            return
    except ValueError:
        print("Invalid input.")
        return

    book_name = books[book_index - 1]
    chapters = list(bible[book_name].keys())

    # Step 2: Choose Chapter
    print(f"\nChapters in {book_name}:")
    for ch in chapters:
        print(ch, end=" ")
    print()
    chapter = input("Enter chapter number: ").strip()
    if chapter not in bible[book_name]:
        print("Invalid chapter.")
        return

    verses = bible[book_name][chapter]

    # Step 3: Choose Verse
    print(f"\nVerses in {book_name} {chapter}:")
    verse_nums = list(verses.keys())
    for v in verse_nums:
        print(v, end=" ")
    print()
    verse = input("Enter verse number: ").strip()
    if verse not in verses:
        print("Invalid verse.")
        return

    # Step 4: Display Verse Text
    verse_text = parser.get_verse(book_name, chapter, verse)
    print(f"\n📜 {book_name} {chapter}:{verse} — {verse_text}")

    # Step 5: Ask to Bookmark
<<<<<<< HEAD
    if input("Bookmark this verse? (y/n): ").strip().lower() == "y":
        add_bookmark(book_name, f"{chapter}:{verse}", verse_text)
        print("✅ Verse bookmarked!")


if __name__ == "__main__":
    main()
=======
    if input("\nBookmark this verse? (y/n): ").strip().lower() == "y":
        add_bookmark(book_name, f"{chapter}:{verse}", verse_text)
        print("✅ Verse bookmarked!")

if __name__ == "__main__":
    main()
>>>>>>> 738c17f541b87184a916976e82abde23c6fb46d2
