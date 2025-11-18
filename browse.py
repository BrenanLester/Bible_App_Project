# browse.py
from bookmarks import add_bookmark
from ascii_art import BROWSE_ART
import re
import shutil
import sys

def strip_colors(text):
    """Remove ANSI color codes for length calculation."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def center_content(content, terminal_width):
    """Center content with specified terminal width."""
    clean_content = strip_colors(content)
    padding = (terminal_width - len(clean_content)) // 2
    return " " * max(0, padding) + content

def browse_bible(bible, parser):
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    # Center ASCII art
    terminal_width = 220  # ← CHANGE THIS FOR ASCII ART
    lines = BROWSE_ART.split('\n')
    for line in lines:
        clean_line = strip_colors(line)
        padding = (terminal_width - len(clean_line)) // 2
        print(" " * padding + f"{CYAN}{line}{RESET}")

    # Center titles
    terminal_width = 210  # ← CHANGE THIS FOR TITLES
    print(center_content(f"{CYAN}KJV VERSION OF THE BIBLE{RESET}", terminal_width))
    print(center_content(f"{YELLOW}Type 'back' to go back or 'exit' to return to menu{RESET}", terminal_width))

    # Define all 66 Bible books in order
    all_books = [
        # Old Testament (39 books)
        'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
        'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings',
        '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job',
        'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah',
        'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
        'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah',
        'Haggai', 'Zechariah', 'Malachi',
        # New Testament (27 books)
        'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians',
        '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians',
        '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus',
        'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John',
        '3 John', 'Jude', 'Revelation'
    ]

    # Display all 66 books visualization
    terminal_width = 215 # ← CHANGE THIS FOR BOOKS GRID
    print(" ")
    print(center_content(f"{CYAN}┌─────────────────────────────────────────────────────────────────────────┐{RESET}", terminal_width))
    print(center_content(f"{CYAN}│                        ALL BIBLE BOOKS (66 TOTAL)                       │{RESET}", terminal_width))
    print(center_content(f"{CYAN}└─────────────────────────────────────────────────────────────────────────┘{RESET}", terminal_width))
    print(" ")
    print(center_content(f"{YELLOW}Bible Books Overview:{RESET}", terminal_width))
    print(center_content(f"{CYAN}┌─────────────────────────────────────────────────────────────────────────┐{RESET}", terminal_width))

    # Display books in 3-column grid
    total_books = len(all_books)
    columns = 3
    rows_needed = (total_books + columns - 1) // columns

    for row in range(rows_needed):
        line = f"{CYAN}│{RESET}"

        for col in range(columns):
            book_index = row + (col * rows_needed)
            if book_index < total_books:
                book_name = all_books[book_index]
                line += f" {GREEN}[{book_index + 1:2d}]{RESET} {book_name:<18}"
            else:
                line += " " * 25  # Space for empty column

        line += f" {CYAN}│{RESET}"
        print(center_content(line, terminal_width))

    print(center_content(f"{CYAN}└─────────────────────────────────────────────────────────────────────────┘{RESET}", terminal_width))

    # Choose Testament
    terminal_width = 210  # ← CHANGE THIS FOR TESTAMENT CHOICE
    print(" ")
    print(center_content(f"{YELLOW}Choose Testament:{RESET}", terminal_width))
    print(center_content(f"{GREEN}[1]{RESET} Old Testament (39 books)", terminal_width))
    print(center_content(f"{GREEN}[2]{RESET} New Testament (27 books)", terminal_width))
    print(" ")
    # Loop until valid testament choice, or back/exit
    while True:
        testament_choice = input(center_content(f"{YELLOW}Enter choice (1-2) or 'back': {RESET}", terminal_width)).strip()
        if testament_choice.lower() == 'back':
            return
        if testament_choice.lower() == 'exit':
            return True
        if testament_choice == "1":
            available_books = [book for book in bible.keys() if book in all_books[:39]]
            testament_name = "Old Testament"
            break
        elif testament_choice == "2":
            available_books = [book for book in bible.keys() if book in all_books[39:]]
            testament_name = "New Testament"
            break
        else:
            print(center_content("❌ Invalid choice. Please enter 1 or 2.", terminal_width))
            continue

    # Testament header
    terminal_width = 220 # ← CHANGE THIS FOR TESTAMENT HEADER
    print(" ")
    print(center_content(f"{CYAN}┌──────────────────────────────────┐{RESET}", terminal_width))
    print(center_content(f"{CYAN} │        {testament_name:^20}      │ {RESET}", terminal_width))
    print(center_content(f"{CYAN}└──────────────────────────────────┘{RESET}", terminal_width))

    # Book selection grid
    terminal_width = 220  # ← CHANGE THIS FOR BOOK SELECTION
    print(" ")
    print(center_content(f"{YELLOW}Books:{RESET}", terminal_width))
    print(center_content(f"{CYAN}┌────────────────────────────────────────────────────────────────┐{RESET}", terminal_width))

    total_books = len(available_books)
    columns = 3
    rows_needed = (total_books + columns - 1) // columns

    for row in range(rows_needed):
        line = f"{CYAN}│{RESET}"

        for col in range(columns):
            book_index = row + (col * rows_needed)
            if book_index < total_books:
                book_name = available_books[book_index]
                line += f" {GREEN}[{book_index + 1:2d}]{RESET} {book_name:<15}"
            else:
                line += " " * 22  # Space for empty column

        line += f" {CYAN}│{RESET}"
        print(center_content(line, terminal_width))

    print(center_content(f"{CYAN}└────────────────────────────────────────────────────────────────┘{RESET}", terminal_width))
    print(" ")
    # Prompt for book selection; re-prompt on invalid input
    while True:
        book_choice = input(center_content(f"{YELLOW}Choose a book number (1-{len(available_books)}) or 'back': {RESET}", terminal_width)).strip()
        if book_choice.lower() == 'back':
            return browse_bible(bible, parser)
        if book_choice.lower() == 'exit':
            return True
        try:
            book_index = int(book_choice)
            if not (1 <= book_index <= len(available_books)):
                print(center_content("❌ Invalid book number. Please try again.", terminal_width))
                continue
            break
        except ValueError:
            print(center_content("❌ Invalid input. Enter a number, 'back' or 'exit'.", terminal_width))
            continue

    book_name = available_books[book_index - 1]
    chapters = list(bible[book_name].keys())

    # Chapter selection
    terminal_width = 220 # ← CHANGE THIS FOR CHAPTER SELECTION
    print(" ")
    print(center_content(f"{CYAN}┌──────────────────────────────────┐{RESET}", terminal_width))
    print(center_content(f"{CYAN}│       Chapters in {book_name:<12}   │{RESET}", terminal_width))
    print(center_content(f"{CYAN}└──────────────────────────────────┘{RESET}", terminal_width))
    print(" ")
    print(center_content(f"{YELLOW}Chapters:{RESET}", terminal_width))

    # Center chapter numbers
    chapters_line = ""
    for i, ch in enumerate(chapters, 1):
        if i % 10 == 0 or i == len(chapters):
            chapters_line += f"{GREEN}{ch}{RESET}"
            print(center_content(chapters_line, terminal_width))
            chapters_line = ""
        else:
            chapters_line += f"{GREEN}{ch}{RESET} "

    if chapters_line:
        print(center_content(chapters_line, terminal_width))
    print(" ")
    # Prompt for chapter selection; re-prompt on invalid input
    while True:
        chapter_choice = input(center_content(f"{YELLOW}Enter chapter number or 'back': {RESET}", terminal_width)).strip()
        if chapter_choice.lower() == 'back':
            return browse_bible(bible, parser)
        if chapter_choice.lower() == 'exit':
            return True
        if chapter_choice in bible[book_name]:
            chapter = chapter_choice
            break
        else:
            print(center_content("❌ Invalid chapter. Please try again.", terminal_width))
            continue

    verses = bible[book_name][chapter]

    # Verse selection (no box, matching chapters style)
    terminal_width = 220 # ← CHANGE THIS FOR VERSE SELECTION
    print(" ")
    print(center_content(f"{YELLOW}Verses:{RESET}", terminal_width))
    verse_nums = list(verses.keys())
    
    # Display verses without box (matching chapters display)
    verses_line = ""
    for i, verse_num in enumerate(verse_nums, 1):
        if i % 10 == 0 or i == len(verse_nums):
            verses_line += f"{GREEN}{verse_num}{RESET}"
            print(center_content(verses_line, terminal_width))
            verses_line = ""
        else:
            verses_line += f"{GREEN}{verse_num}{RESET} "
    
    if verses_line:
        print(center_content(verses_line, terminal_width))
    print(" ")
    # Prompt for verse selection; re-prompt on invalid input
    while True:
        verse_choice = input(center_content(f"{YELLOW}Enter verse number or 'back': {RESET}", terminal_width)).strip()
        if verse_choice.lower() == 'back':
            return browse_bible(bible, parser)
        if verse_choice.lower() == 'exit':
            return True
        verse = verse_choice
        if verse in verses:
            break
        else:
            print(center_content("❌ Invalid verse. Please enter a valid verse number.", terminal_width))
            continue

    # Display Verse Text
    WHITE = "\033[97m"
    CREAM = "\033[38;5;223m"
    verse_text = parser.get_verse(book_name, chapter, verse)

    # Create a border around the verse
    verse_reference = f"{book_name} {chapter}:{verse}"
    max_line_width = max(len(verse_reference), len(verse_text))
    border_width = min(max_line_width + 4, 80)

    # Center the verse box
    terminal_width = 220 # ← CHANGE THIS FOR VERSE DISPLAY
    verse_box = f"\n{WHITE}┌{'─' * border_width}┐{RESET}\n"
    verse_box += f"{WHITE}│{' ' * border_width}│{RESET}\n"

    # Center the reference
    ref_padding = (border_width - len(verse_reference)) // 2
    verse_box += f"{WHITE}│{' ' * ref_padding}{GREEN}{verse_reference}{' ' * (border_width - len(verse_reference) - ref_padding)}{WHITE}│{RESET}\n"
    verse_box += f"{WHITE}│{' ' * border_width}│{RESET}\n"

    # Wrap long verse text
    words = verse_text.split()
    lines = []
    current_line = []

    for word in words:
        if len(' '.join(current_line + [word])) <= border_width - 4:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))

    # Print each line of verse text
    for line in lines:
        line_padding = (border_width - len(line)) // 2
        verse_box += f"{WHITE}│{' ' * line_padding}{CREAM}{line}{' ' * (border_width - len(line) - line_padding)}{WHITE}│{RESET}\n"

    verse_box += f"{WHITE}│{' ' * border_width}│{RESET}\n"
    verse_box += f"{WHITE}└{'─' * border_width}┘{RESET}"

    # Center the entire verse box
    verse_lines = verse_box.split('\n')
    for line in verse_lines:
        print(center_content(line, terminal_width))

    # Bookmark question - aligned with verse display
    terminal_width = 220
    while True:
        print(center_content(f"\n{YELLOW}Bookmark this verse? (y/n/back): {RESET}", terminal_width), end='')
        sys.stdout.flush()
        bookmark_choice = input().strip().lower()
        if bookmark_choice == 'back':
            return browse_bible(bible, parser)
        elif bookmark_choice == 'exit':
            return True
        elif bookmark_choice == 'y':
            add_bookmark(book_name, f"{chapter}:{verse}", verse_text)
            print(center_content(f"{GREEN}✅ Verse bookmarked!{RESET}", terminal_width))
            break
        elif bookmark_choice == 'n':
            break
        else:
            print(center_content(f"{YELLOW}❌ Invalid choice. Please enter 'y', 'n', or 'back'.{RESET}", terminal_width))
            continue

    # Browse another question - aligned with verse display
    prompt_width = 220
    while True:
        print(center_content(f"\n{YELLOW}Browse another verse? (y/n): {RESET}", prompt_width), end='')
        sys.stdout.flush()
        another_choice = input().strip().lower()
        if another_choice == 'y':
            return browse_bible(bible, parser)
        elif another_choice == 'n':
            return True
        else:
            print(center_content(f"{YELLOW}❌ Invalid choice. Please enter 'y' or 'n'.{RESET}", prompt_width))
            continue