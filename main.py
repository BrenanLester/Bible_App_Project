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

    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_candidate = os.path.join(script_dir, 'kjv.json')

    parser = JSONBibleParser(json_candidate)
    try:
        bible = parser.load()
    except Exception as e:
        print('Failed to load JSON Bible:', e)
        return

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
            from search import search_interface
            
            # Run the interactive search interface
            search_interface(bible)
            
            # After search interface returns, go back to main menu
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
def browse_bible(bible, parser):
    from ascii_art import BROWSE_ART
    
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
    
    # Choose Testament
    print(f"\n{GREEN}Choose Testament:{RESET}")
    print(f"{GREEN}[1]{RESET} Old Testament ({len(old_testament)} books)")
    print(f"{GREEN}[2]{RESET} New Testament ({len(new_testament)} books)")
    print(f"{GREEN}[3]{RESET} All Books ({len(bible)} books)")                                                          
    
    testament_choice = input(f"\n{YELLOW}Enter choice (1-3) or 'back': {RESET}").strip()
    
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
    elif testament_choice == "3":
        available_books = list(bible.keys())
        testament_name = "All Books"
    else:
        print("❌ Invalid choice.")
        return
    
    print(f"\n{CYAN}╔══════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║         {testament_name:^20}         ║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════╝{RESET}")
    
    # Step 1: Choose Book
    print(f"\n{YELLOW}Available Books:{RESET}")
    for i, book in enumerate(available_books, 1):
        print(f"{GREEN}[{i:2d}]{RESET} {book}")
    
    book_choice = input(f"\n{YELLOW}Choose a book number (1-{len(available_books)}) or 'back': {RESET}").strip()
    
    if book_choice.lower() == 'back':
        return browse_bible(bible, parser)  # Restart browse
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

    # Step 2: Choose Chapter
    print(f"\n{CYAN}╔══════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║          Chapters in {book_name:<12}   ║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════╝{RESET}")
    
    print(f"\n{YELLOW}Available Chapters:{RESET}")
    for i, ch in enumerate(chapters, 1):
        if i % 10 == 0 or i == len(chapters):
            print(f"{GREEN}{ch}{RESET}")
        else:
            print(f"{GREEN}{ch}{RESET}", end=" ")
    print()
    
    chapter_choice = input(f"\n{YELLOW}Enter chapter number or 'back': {RESET}").strip()
    
    if chapter_choice.lower() == 'back':
        return browse_bible(bible, parser)  # Restart browse
    elif chapter_choice.lower() == 'exit':
        return True
    
    chapter = chapter_choice
    if chapter not in bible[book_name]:
        print("❌ Invalid chapter.")
        return

    verses = bible[book_name][chapter]

    # Step 3: Choose Verse
    print(f"\n{CYAN}╔══════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║          Verses in {book_name} {chapter:<3}       ║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════╝{RESET}")
    
    print(f"\n{YELLOW}Available Verses:{RESET}")
    verse_nums = list(verses.keys())
    for i, v in enumerate(verse_nums, 1):
        if i % 10 == 0 or i == len(verse_nums):
            print(f"{GREEN}{v}{RESET}")
        else:
            print(f"{GREEN}{v}{RESET}", end=" ")
    print()
    
    verse_choice = input(f"\n{YELLOW}Enter verse number or 'back': {RESET}").strip()
    
    if verse_choice.lower() == 'back':
        return browse_bible(bible, parser)  # Restart browse
    elif verse_choice.lower() == 'exit':
        return True
    
    verse = verse_choice
    if verse not in verses:
        print("❌ Invalid verse.")
        return

    # Step 4: Display Verse Text
    verse_text = parser.get_verse(book_name, chapter, verse)
    print(f"\n{CYAN}╔══════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║              📜 VERSE 📜              ║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════╝{RESET}")
    print(f"\n{GREEN}{book_name} {chapter}:{verse}{RESET}")
    print(f"{YELLOW}{verse_text}{RESET}")

    # Step 5: Ask to Bookmark
    bookmark_choice = input(f"\n{YELLOW}Bookmark this verse? (y/n/back): {RESET}").strip().lower()
    if bookmark_choice == 'back':
        return browse_bible(bible, parser)  # Restart browse
    elif bookmark_choice == 'exit':
        return True
    elif bookmark_choice == 'y':
        add_bookmark(book_name, f"{chapter}:{verse}", verse_text)
        print(f"{GREEN}✅ Verse bookmarked!{RESET}")
    
    # After viewing verse, ask if user wants to browse another
    another_choice = input(f"\n{YELLOW}Browse another verse? (y/n): {RESET}").strip().lower()
    if another_choice == 'y':
        return browse_bible(bible, parser)  # Restart browse
    else:
        return True
if __name__ == "__main__":
    main()