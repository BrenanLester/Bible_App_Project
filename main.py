"""Terminal-Based Bible App using JSON Bible data."""
import os
import time
import sys
from bible_parser_json import JSONBibleParser
from browse import browse_bible
from bookmarks import add_bookmark, view_bookmarks, remove_bookmark
from verse_of_the_day import verse_of_the_day
from ascii_art import HEADER_ART

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
    print(f"║      {title:^16}       ║")
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
    typewriter(f"📖 {votd}", delay=0.0)
  

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
            RED    = "\033[91m"
            show_section_header("BOOKMARKS")
            view_bookmarks()
            if input(f"{RED}\nRemove a bookmark? (y/n):{RESET}").strip().lower() == "y":
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

if __name__ == "__main__":
    main()
