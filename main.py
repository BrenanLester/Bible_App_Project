"""Terminal-Based Bible App using JSON Bible data."""
import os
import time
import sys
from bible_parser_json import JSONBibleParser
from browse import browse_bible
from bookmarks import add_bookmark, view_bookmarks, remove_bookmark
from verse_of_the_day import verse_of_the_day
from ascii_art import HEADER_ART, MAIN_MENU_ART

# === CORE FUNCTIONS ===
def typewriter(text, delay=1):
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
    show_main_menu_header()
    CYAN = "\033[96m"
    RESET = "\033[0m"
    print(CYAN + f"\n╔════════════════════════════╗")
    print(f"║      {title:^16}       ║")
    print(f"╚════════════════════════════╝" + RESET)

def show_landing_page():
    """Show landing page with intro ASCII art"""
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    
    lines = HEADER_ART.split('\n')
    
    # Find the width of the ASCII art
    art_width = max(len(line) for line in lines)
    terminal_width = 200  # Adjust this as needed
    border_padding = (terminal_width - art_width) // 2
    
    for line in lines:
        padded_line = " " * border_padding + line
        if line.strip() == '':
            print()
        elif '┌' in line or '└' in line or line.strip() == '│' or '─' in line:
            print(CYAN + padded_line + RESET)
        elif '│' in line:
            parts = line.split('│')
            if len(parts) >= 3:
                print(CYAN + " " * border_padding + parts[0] + '│' + RESET + WHITE + parts[1] + RESET + CYAN + '│' + RESET)
            else:
                print(WHITE + padded_line + RESET)
        else:
            print(WHITE + padded_line + RESET)

def show_main_menu_header():
    """Show main menu header (different from landing page)"""
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    
    lines = MAIN_MENU_ART.split('\n')
    
    # Find the width of the ASCII art
    art_width = max(len(line) for line in lines)
    terminal_width = 220  # Adjust this as needed
    border_padding = (terminal_width - art_width) // 2
    
    for line in lines:
        padded_line = " " * border_padding + line
        
        if line.strip() == '':
            print()
        elif '┌' in line or '└' in line or '┐' in line or '┘' in line or '─' in line:
            # Border lines - make it cyan
            print(CYAN + padded_line + RESET)
        elif line.strip().startswith('│') and line.strip().endswith('│'):
            # Lines with border on both sides
            print(CYAN + padded_line + RESET)
        else:
            # All text/content - make it white
            print(WHITE + padded_line + RESET)

# Function to remove ANSI color codes for length calculation
def strip_colors(text):
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

# === MAIN APPLICATION ===
def main():
    # Show LANDING PAGE
    show_landing_page()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_candidate = os.path.join(script_dir, 'kjv.json')

    parser = JSONBibleParser(json_candidate)
    try:
        bible = parser.load()
        
        # Center the Bible loaded message
        GREEN = "\033[92m"
        RESET = "\033[0m"
        success_msg = f" "
        terminal_width = 155
        padding = (terminal_width - len(success_msg)) // 2
        print(" " * padding + GREEN + success_msg + RESET)
        
    except Exception as e:
        print('Failed to load JSON Bible:', e)
        return

    # === VERSE OF THE DAY ===
    GREEN = "\033[92m"
    WHITE= "\033[97m"
    RESET = "\033[0m"
    CYAN = "\033[96m"
    YELLOW= "\033[93m"
    votd = verse_of_the_day(bible)
    verse_text = f"📖 {votd}"

    # Auto-adjust border width based on verse length
    max_width = 80  # Maximum terminal width
    min_width = 60  # Minimum border width

    # Calculate optimal border width
    verse_length = len(verse_text)
    border_width = min(max(verse_length + 4, min_width), max_width)  # +4 for padding

    # Split long verses into multiple lines
    def wrap_text(text, width):
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            if len(' '.join(current_line + [word])) <= width - 4:  # -4 for border padding
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

    wrapped_lines = wrap_text(verse_text, border_width - 2)

    # Center the entire border
    terminal_width = 196
    border_padding = (terminal_width - border_width) // 2

    # Print the border and verse - KEEPING THIS EXACTLY AS YOU HAVE IT
    print(f"{' ' * border_padding}{GREEN}┌{'📖  VERSE OF THE DAY  📖' }┐{RESET}")
    print(f"{' ' * border_padding}{CYAN}┌{'─' * border_width}┐{RESET}")
 
    print(f"{' ' * border_padding}{CYAN}│{' ' * border_width}│{RESET}")

    for line in wrapped_lines:
     print(f"{' ' * border_padding}{CYAN}│{RESET} ", end="")
     typewriter(f"{WHITE}{line:^{border_width-2}}{RESET}", delay=0.02)
     print(f" {CYAN}│{RESET}")

    print(f"{' ' * border_padding}{CYAN}│{' ' * border_width}│{RESET}")
    print(f"{' ' * border_padding}{CYAN}└{'─' * border_width}┘{RESET}")

    # Center the Bible loaded message at the BOTTOM
    success_msg = f"✅ Bible loaded successfully! Books: {len(bible)}"
    terminal_width = 200
    padding = (terminal_width - len(success_msg)) // 2
    print(" " * padding + GREEN + success_msg + RESET)

    # Wait and clear screen - CENTERED
    welcome_msg = "WELCOME TO BIBLE TERMINAL EDITION! FOR MAIN MENU CLICK \"ENTER\""
    terminal_width = 200
    welcome_padding = (terminal_width - len(welcome_msg)) // 2
    input(f"\n\n{' ' * welcome_padding}{YELLOW}{welcome_msg}{RESET}")
    clear_screen()

    
    while True:
        # === MAIN MENU ===
        GREEN = "\033[92m"
        RESET = "\033[0m"
        CYAN = "\033[96m"

        # Show MAIN MENU HEADER (different from landing page)
        show_main_menu_header()

        # Center the MAIN MENU header
        terminal_width = 120
        menu_header_lines = [
            "╔════════════════════════════╗",
            "║        MAIN  MENU          ║", 
            "╚════════════════════════════╝"
        ]
        
        # Calculate padding for the header
        header_length = len(strip_colors(menu_header_lines[0]))
        header_padding = (terminal_width - header_length) // 2
        
        # Print centered header
        for line in menu_header_lines:
            print(" " * header_padding + CYAN + line + RESET)

        # Center the menu block
        menu_items = [
            f"{GREEN}[1]{RESET} Browse",
            f"{GREEN}[2]{RESET} Search Verse", 
            f"{GREEN}[3]{RESET} View / Remove Bookmarks",
            f"{GREEN}[4]{RESET} Search History",
            f"{GREEN}[5]{RESET} Exit"
        ]
        
        # Find the longest menu item length (without colors)
        max_length = max(len(strip_colors(item)) for item in menu_items)
        
        # Calculate padding for the entire block
        block_padding = (terminal_width - max_length) // 2
        
        # Print all menu items with the same padding
        for item in menu_items:
            print(" " * block_padding + item)

        # Center the input prompt
        prompt_text = "Enter choice: "
        terminal_width = 107
        prompt_padding = (terminal_width - len(prompt_text)) // 2
        choice = input('\n' + " " * prompt_padding + prompt_text).strip()

        if choice == "1":
            show_section_header("BROWSE BIBLE")
            browse_bible(bible, parser)
            input(f"\n{GREEN}Press Enter to return to main menu...{RESET}")
            clear_screen()

        elif choice == "2":
            show_section_header("SEARCH VERSE")
            from search import search_interface
            
            # Run the interactive search interface
            search_interface(bible)
            
            # After search interface returns, go back to main menu
            input(f"\n{GREEN}Press Enter to return to main menu...{RESET}")
            clear_screen()

        elif choice == "3":
            RED    = "\033[91m"
            show_section_header("BOOKMARKS")
            view_bookmarks()
            try:
                print(f"\n{CYAN}Options:{RESET}")
                print(f"{GREEN}[1]{RESET} Remove a specific bookmark")
                print(f"{GREEN}[2]{RESET} Clear ALL bookmarks")
                print(f"{GREEN}[3]{RESET} Return to main menu")
                
                sub_choice = input(f"\n{YELLOW}Choose option (1-3): {RESET}").strip()
                
                if sub_choice == "1":
                    try:
                        num = int(input(f"{YELLOW}Enter bookmark number: {RESET}"))
                        remove_bookmark(num)
                    except ValueError:
                        print(f"{RED}❌ Invalid input. Please enter a number.{RESET}")
                    except Exception as e:
                        print(f"{RED}❌ Error removing bookmark: {e}{RESET}")
                
                elif sub_choice == "2":
                    # Clear all bookmarks with confirmation
                    from bookmarks import clear_all_bookmarks
                    clear_all_bookmarks()
                
                elif sub_choice == "3":
                    pass  # Return to main menu
                else:
                    print(f"{RED}❌ Invalid option.{RESET}")
            
            except Exception as e:
                print(f"{RED}❌ Error in bookmarks menu: {e}{RESET}")
            input(f"\n{GREEN}Press Enter to return to main menu...{RESET}")
            clear_screen()

        elif choice == "4":
            show_section_header("SEARCH HISTORY")
            from history import SearchHistory
            history = SearchHistory()
            history_items = history.list_all()

            if history_items:
                print("\nRecent searches:")
                for i, query in enumerate(history_items, 1):
                    print(f"{i}. {query}")

                # === Ask to clear history AFTER listing ===
                clear_choice = input("\nDo you want to CLEAR ALL history? (y/n): ").strip().lower()

                if clear_choice == "y":
                    history.clear()
                    print("\n✅ All search history has been cleared!")
                else:
                    print("\n❎ History not cleared.")
            else:
                print("\nNo search history found.")

            input(f"\n{GREEN}Press Enter to return to main menu...{RESET}")
            clear_screen()

        elif choice == "5":
            clear_screen()
            show_main_menu_header()
            print(f"\n{GREEN}👋 Thank you for using Bible Terminal Edition! Goodbye!{RESET}")
            break

        else:
            print("Invalid choice.")
            time.sleep(1)
            clear_screen()

if __name__ == "__main__":
    main()
