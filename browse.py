# browse.py
from bookmarks import add_bookmark
from ascii_art import BROWSE_ART

def browse_bible(bible, parser):
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    
    print(CYAN + BROWSE_ART + RESET)
    print(f"{CYAN}📖 Browse the Bible 📖{RESET}")
    print(f"{YELLOW}Type 'back' to go back or 'exit' to return to menu{RESET}")
    
    # Define Old and New Testament books
    old_testament = [
        'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
        'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings',
        '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job',
        'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah',
        'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
        'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah',
        'Haggai', 'Zechariah', 'Malachi'
    ]
    
    new_testament = [
        'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians',
        '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians',
        '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus',
        'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John',
        '3 John', 'Jude', 'Revelation'
    ]
    
    # Show all books count automatically
    print(f"\n{YELLOW}Bible Statistics:{RESET}")
    print(f"{GREEN}• Old Testament: {len(old_testament)} books{RESET}")
    print(f"{GREEN}• New Testament: {len(new_testament)} books{RESET}")
    print(f"{CYAN}• All Books: {len(bible)} books total{RESET}")
    
    # Choose Testament - Only Old/New Testament choices
    print(f"\n{YELLOW}Choose Testament:{RESET}")
    print(f"{GREEN}[1]{RESET} Old Testament ({len(old_testament)} books)")
    print(f"{GREEN}[2]{RESET} New Testament ({len(new_testament)} books)")
    
    testament_choice = input(f"\n{YELLOW}Enter choice (1-2) or 'back': {RESET}").strip()
    
    if testament_choice.lower() == 'back':
        return
    elif testament_choice.lower() == 'exit':
        return True
    
    if testament_choice == "1":
        available_books = [book for book in bible.keys() if book in old_testament]
        testament_name = "Old Testament"
    elif testament_choice == "2":
        available_books = [book for book in bible.keys() if book in new_testament]
        testament_name = "New Testament"
    else:
        print("❌ Invalid choice. Please enter 1 or 2.")
        return
    
    print(f"\n{CYAN}╔══════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║         {testament_name:^20}         ║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════╝{RESET}")
    
    # Step 1: Choose Book - GRID VIEW (3 columns)
    print(f"\n{YELLOW}Books:{RESET}")
    print(f"{CYAN}╔════════════════════════════════════════════════════════════════╗{RESET}")
    
    # Calculate how many rows needed for 3-column layout
    total_books = len(available_books)
    columns = 3
    rows_needed = (total_books + columns - 1) // columns  # Round up
    
    for row in range(rows_needed):
        line = f"{CYAN}║{RESET}"
        
        # Three columns
        for col in range(columns):
            book_index = row + (col * rows_needed)
            if book_index < total_books:
                book_name = available_books[book_index]
                line += f" {GREEN}[{book_index + 1:2d}]{RESET} {book_name:<15}"
            else:
                line += " " * 22  # Space for empty column
                
        line += f" {CYAN}║{RESET}"
        print(line)
    
    print(f"{CYAN}╚════════════════════════════════════════════════════════════════╝{RESET}")
    
    book_choice = input(f"\n{YELLOW}Choose a book number (1-{len(available_books)}) or 'back': {RESET}").strip()
    
    if book_choice.lower() == 'back':
        return browse_bible(bible, parser)
    elif book_choice.lower() == 'exit':
        return True
    
    try:
        book_index = int(book_choice)
        if not (1 <= book_index <= len(available_books)):
            print("❌ Invalid book number.")
            return
    except ValueError:
        print("❌ Invalid input.")
        return

    book_name = available_books[book_index - 1]
    chapters = list(bible[book_name].keys())

    # Step 2: Choose Chapter - SINGLE ROW (original format)
    print(f"\n{CYAN}╔══════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║          Chapters in {book_name:<12}    ║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════╝{RESET}")
    
    print(f"\n{YELLOW}Chapters:{RESET}")
    for i, ch in enumerate(chapters, 1):
        if i % 10 == 0 or i == len(chapters):
            print(f"{GREEN}{ch}{RESET}")
        else:
            print(f"{GREEN}{ch}{RESET}", end=" ")
    print()
    
    chapter_choice = input(f"\n{YELLOW}Enter chapter number or 'back': {RESET}").strip()
    
    if chapter_choice.lower() == 'back':
        return browse_bible(bible, parser)
    elif chapter_choice.lower() == 'exit':
        return True
    
    chapter = chapter_choice
    if chapter not in bible[book_name]:
        print("❌ Invalid chapter.")
        return

    verses = bible[book_name][chapter]

    # Step 3: Choose Verse - GRID VIEW (3 columns)
    title = f"Verses in {book_name} {chapter}"
    border_length = len(title) + 16 # +4 for padding

    print(f"\n{CYAN}╔{'═' * border_length}╗{RESET}")
    print(f"{CYAN}║        {title}        ║{RESET}")
    print(f"{CYAN}╚{'═' * border_length}╝{RESET}")
    print(f"\n{YELLOW}Available Verses:{RESET}")
    verse_nums = list(verses.keys())
    print(f"{CYAN}╔═══════════════════════════════════════════════════════════╗{RESET}")
    
    total_verses = len(verse_nums)
    columns = 4
    rows_needed = (total_verses + columns - 1) // columns
    
    for row in range(rows_needed):
        line = f"{CYAN}║{RESET}"
        
        # Three columns
        for col in range(columns):
            verse_index = row + (col * rows_needed)
            if verse_index < total_verses:
                verse_num = verse_nums[verse_index]
                line += f" {GREEN}{verse_num:>4}{RESET}"
            else:
                line += " " * 5# Space for empty column
                
        line += " " * 38+ f" {CYAN}║{RESET}"
        print(line)
    
    print(f"{CYAN}╚═══════════════════════════════════════════════════════════╝{RESET}")
    
    verse_choice = input(f"\n{YELLOW}Enter verse number or 'back': {RESET}").strip()
    
    if verse_choice.lower() == 'back':
        return browse_bible(bible, parser)
    elif verse_choice.lower() == 'exit':
        return True
    
    verse = verse_choice
    if verse not in verses:
        print("❌ Invalid verse.")
        return

    # Step 4: Display Verse Text
    verse_text = parser.get_verse(book_name, chapter, verse)
    print(f"\n{CYAN}╔══════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║              📜 VERSE 📜             ║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════╝{RESET}")
    print(f"\n{GREEN}{book_name} {chapter}:{verse}{RESET}")
    print(f"{YELLOW}{verse_text}{RESET}")

    # Step 5: Ask to Bookmark
    bookmark_choice = input(f"\n{YELLOW}Bookmark this verse? (y/n/back): {RESET}").strip().lower()
    if bookmark_choice == 'back':
        return browse_bible(bible, parser)
    elif bookmark_choice == 'exit':
        return True
    elif bookmark_choice == 'y':
        add_bookmark(book_name, f"{chapter}:{verse}", verse_text)
        print(f"{GREEN}✅ Verse bookmarked!{RESET}")
    
    # After viewing verse, ask if user wants to browse another
    another_choice = input(f"\n{YELLOW}Browse another verse? (y/n): {RESET}").strip().lower()
    if another_choice == 'y':
        return browse_bible(bible, parser)
    else:
        return True
