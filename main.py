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
    CYAN = "\033[92m"
    RESET = "\033[0m"
    
    # Set terminal width and center the header
    terminal_width = 340
    header_width = 40  # Width of your header box
    border_padding = (terminal_width - header_width) // 2
    
    print(" " * border_padding + CYAN + f"╔════════════════════════════╗" + RESET)
    print(" " * border_padding + CYAN + f"║         VERSION 0.1        ║" + RESET)
    print(" " * border_padding + CYAN + f"╚════════════════════════════╝" + RESET)

def show_landing_page():
    """Show landing page with intro ASCII art"""
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    BEIGE = "\033[38;5;223m"     # Warm beige

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
                print(CYAN + " " * border_padding + parts[0] + '│' + RESET + BEIGE + parts[1] + RESET + CYAN + '│' + RESET)
            else:
                print(BEIGE + padded_line + RESET)
        else:
            print(BEIGE + padded_line + RESET)

def show_main_menu_header():
    """Show main menu header (different from landing page)"""
    CYAN = "\033[96m"
    CREAM = "\033[38;5;230m"
    RESET = "\033[0m"
    
    lines = MAIN_MENU_ART.split('\n')
    
    # Find the width of the ASCII art
    art_width = max(len(line) for line in lines)
    terminal_width = 220
    border_padding = (terminal_width - art_width) // 2
    
    for line in lines:
        padded_line = " " * border_padding + line
        
        if line.strip() == '':
            print()
        elif '8' in line:
            # Lines with "8" text - make it cream
            print(CREAM + padded_line + RESET)
        else:
            # All other lines (borders) - make it cyan
            print(CYAN + padded_line + RESET)

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
     typewriter(f"{WHITE}{line:^{border_width-2}}{RESET}", delay=0.01)
     print(f" {CYAN}│{RESET}")

    print(f"{' ' * border_padding}{CYAN}│{' ' * border_width}│{RESET}")
    print(f"{' ' * border_padding}{CYAN}└{'─' * border_width}┘{RESET}")

    # Center the Bible loaded message at the BOTTOM
    success_msg = f"✅ Bible loaded successfully! Books: {len(bible)}"
    terminal_width = 200
    padding = (terminal_width - len(success_msg)) // 2
    print(" " * padding + GREEN + success_msg + RESET)

    # Wait and clear screen - CENTERED
    welcome_msg = "WELCOME TO THE BIBLE (TERMINAL EDITION) FOR MAIN MENU CLICK \"ENTER\""
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
        terminal_width = 100
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
        terminal_width = 85
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
                # Center the options section
                terminal_width = 214  # Set your desired width
                
                options = [
                    f"{CYAN}Options:{RESET}",
                    f"{GREEN}[1]{RESET} Remove a specific bookmark",
                    f"{GREEN}[2]{RESET} Clear ALL bookmarks", 
                    f"{GREEN}[3]{RESET} Return to main menu"
                ]
                
                # Find the longest option length (without colors)
                max_length = max(len(strip_colors(option)) for option in options)
                
                # Calculate padding for the entire block
                block_padding = (terminal_width - max_length) // 2
                
                # Print all options with the same padding
                print()  # Add space before options
                for option in options:
                    print(" " * block_padding + option)
                
           # Center the input prompt
                # Center the input prompt
                print()  # blank line
                prompt_text = f"{YELLOW}Choose option (1-3): {RESET}"
                clean_prompt = strip_colors(prompt_text)
                prompt_padding = (terminal_width - len(clean_prompt)) // 2

                # Loop until valid option selected
                while True:
                    sub_choice = input(" " * prompt_padding + prompt_text).strip()
                    if sub_choice == "1":
                        # remove specific bookmark - allow retry until valid or 'back'
                        num_prompt = f"{YELLOW}Enter bookmark number (or 'back' to cancel): {RESET}"
                        clean_num_prompt = strip_colors(num_prompt)
                        num_padding = (terminal_width - len(clean_num_prompt)) // 2
                        while True:
                            num_input = input(" " * num_padding + num_prompt).strip()
                            if num_input.lower() in ('back','b','cancel','c'):
                                break  # back to options menu
                            try:
                                num = int(num_input)
                                # call remove_bookmark; it returns True on success
                                if remove_bookmark(num):
                                    break  # removal ok -> back to options menu
                                else:
                                    # removal failed (out of range etc.) -> reprompt
                                    err = f"{RED}❌ Removal failed. Try again or type 'back'.{RESET}"
                                    print(" " * num_padding + err)
                                    continue
                            except ValueError:
                                err = f"{RED}❌ Invalid input. Enter a number or 'back'.{RESET}"
                                print(" " * num_padding + err)
                                continue
                        # after handling option 1, show options again
                        continue

                    elif sub_choice == "2":
                        # Clear all bookmarks (confirmation handled in function)
                        from bookmarks import clear_all_bookmarks
                        clear_all_bookmarks()
                        # after clearing, return to options (so user can choose again)
                        continue

                    elif sub_choice == "3":
                        # Return to main menu
                        break

                    else:
                        err_msg = f"{RED}❌ Invalid option. Choose 1, 2 or 3.{RESET}"
                        print(" " * prompt_padding + err_msg)
                        continue
            
            except Exception as e:
                print(f"{RED}❌ Error in bookmarks menu: {e}{RESET}")
            input(f"\n{GREEN}Press Enter to return to main menu...{RESET}")
            clear_screen()

        elif choice == "4":
            show_section_header("SEARCH HISTORY")
            from history import SearchHistory
            history = SearchHistory()
            
            # Display history in table format, if there is any
            history_exists = history.display_table()
            
            if history_exists:
                # Only ask about clearing if there was
                terminal_width = 112
                clear_prompt = "Do you want to CLEAR ALL history? (y/n): "
                prompt_padding = (terminal_width - len(clear_prompt)) // 2
                # Loop until valid y/n
                while True:
                    clear_choice = input(f"\n{' ' * prompt_padding}{YELLOW}{clear_prompt}{RESET}").strip().lower()
                    if clear_choice in ("y", "n"):
                        break
                    print(f"\n{' ' * prompt_padding}{YELLOW}Please type 'y' or 'n'.{RESET}")

                if clear_choice == "y":
                    history.clear()
                    # Center success message
                    terminal_width = 218
                    success_msg = "✅ All search history has been cleared!"
                    success_padding = (terminal_width - len(success_msg)) // 2
                    print(f"\n{' ' * success_padding}{GREEN}{success_msg}{RESET}")
                else:
                    # Center "not cleared" message
                    terminal_width = 218
                    not_cleared_msg = "History not cleared."
                    not_cleared_padding = (terminal_width - len(not_cleared_msg)) // 2
                    print(f"\n{' ' * not_cleared_padding}{YELLOW}{not_cleared_msg}{RESET}")

            # Center the "Press Enter" prompt
            terminal_width = 210
            enter_msg = "Press Enter to return to main menu..."
            enter_padding = (terminal_width - len(enter_msg)) // 2
            input(f"\n{' ' * enter_padding}{GREEN}{enter_msg}{RESET}")
            clear_screen()


        elif choice == "5":
            clear_screen()
            show_main_menu_header()
            # Center goodbye message
            terminal_width = 166
            goodbye_msg = "👋 Thank you for using Bible Terminal Edition! Goodbye!"
            goodbye_padding = (terminal_width - len(goodbye_msg)) // 2
            print(f"\n{' ' * goodbye_padding}{GREEN}{goodbye_msg}{RESET}")
            break

        else:
            # Center invalid choice message
            terminal_width = 166
            invalid_msg = "Invalid choice."
            invalid_padding = (terminal_width - len(invalid_msg)) // 2
            print(f"{' ' * invalid_padding}{YELLOW}{invalid_msg}{RESET}")
            time.sleep(1)
            clear_screen()

if __name__ == "__main__":
    main()
