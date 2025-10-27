"""Terminal-Based Bible App using JSON Bible data.

This version reads `kjv.json` and includes:
- Verse Search (with algorithm in search.py)
- Bookmarks (add, view, remove)
- Verse of the Day (random)
- Search History (queue)
- Browse feature with Book → Chapter → Verse hierarchy
"""

import os
from bible_parser_json import JSONBibleParser
from search import search_bible
from bookmarks import add_bookmark, view_bookmarks, remove_bookmark
from history import add_to_history, view_history
from verse_of_the_day import verse_of_the_day

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_candidate = os.path.join(script_dir, 'kjv.json')

    parser = JSONBibleParser(json_candidate)
    try:
        bible = parser.load()
    except Exception as e:
        print('Failed to load JSON Bible:', e)
        return

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
            query = input("Enter keyword or phrase: ").strip()
            add_to_history(query)
            results = search_bible(bible, query)
            if results:
                for i, (book, ref, text) in enumerate(results, 1):
                    print(f"{i}. {book} {ref} - {text}")
                if input("Bookmark a result? (y/n): ").strip().lower() == "y":
                    try:
                        idx = int(input("Number to bookmark: "))
                        if 1 <= idx <= len(results):
                            book, ref, text = results[idx - 1]
                            add_bookmark(book, ref, text)
                        else:
                            print("Invalid number.")
                    except ValueError:
                        print("Invalid input.")
            else:
                print("No results found.")

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
    if input("Bookmark this verse? (y/n): ").strip().lower() == "y":
        add_bookmark(book_name, f"{chapter}:{verse}", verse_text)
        print("✅ Verse bookmarked!")


if __name__ == "__main__":
    main()
