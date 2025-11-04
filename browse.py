from bookmarks import add_bookmark, view_bookmarks, remove_bookmark

def browse_bible(bible, parser):
    """Browse Bible with enhanced UI removed; replaced by basic interaction."""

    books = list(bible.keys())

    # Display books in a table format (3 columns)
    cols = 4
    col_width = 20  # Adjust this to align columns nicely

    print("Available Books:")
    for i in range(0, len(books), cols):
        row = books[i:i + cols]
        row_display = ""
        for j, book in enumerate(row):
            index = i + j + 1
            row_display += f"[{index:>2}] {book:<{col_width}}"
        print(row_display)
    print('-' * 80)

    try:
        book_index = int(input("Choose a book number: "))
        if not (1 <= book_index <= len(books)):
            print("Invalid book number.")
            input("Press Enter to continue...")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("Press Enter to continue...")
        return

    book_name = books[book_index - 1]
    chapters = list(bible[book_name].keys())

    # Display chapters
    print(f"\nChapters in {book_name}:")
    for i, ch in enumerate(chapters, 1):
        print(f"{ch}", end="  ")
        if i % 20 == 0:  # New line every 20 chapters
            print()
    print("\n" + ('-' * 80))

    chapter = input("Enter chapter number: ")
    if chapter not in bible[book_name]:
        print("Invalid chapter.")
        input("Press Enter to continue...")
        return

    verses = bible[book_name][chapter]

    # Display verses
    print(f"\nVerses in {book_name} Chapter {chapter}:")
    verse_nums = list(verses.keys())
    for i, v in enumerate(verse_nums, 1):
        print(f"{v}", end="  ")
        if i % 20 == 0:  # New line every 20 verses
            print()
    print("\n" + ('-' * 80))

    verse = input("Enter verse number: ")
    if verse not in verses:
        print("Invalid verse.")
        input("Press Enter to continue...")
        return

    # Display the verse
    verse_text = parser.get_verse(book_name, chapter, verse)
    print(f"\n{book_name} {chapter}:{verse}\n{verse_text}\n")

    # Ask to bookmark
    bookmark_choice = input("Bookmark this verse? (y/n): ")
    if bookmark_choice.lower() == "y":
        add_bookmark(book_name, f"{chapter}:{verse}", verse_text)
        print("Bookmark added.")

    input("Press Enter to continue...")

def get_bookmarks_list():
    """Get list of bookmarks from bookmarks module"""
    from bookmarks import _bookmarks
    return [(book, ref, text) for book, ref, text in _bookmarks.values()]

def get_history_list():
    """Get list of search history from history module"""
    from history import search_history
    return list(search_history)