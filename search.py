import re
import os
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from bible_parser_json import JSONBibleParser
from ascii_art import SEARCH_ART
from history import SearchHistory

PAGE_SIZE = 10

# ====================================================
#                 KMP ALGORITHM
# ====================================================

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    """Return True if pattern exists inside text."""
    if not pattern:
        return False
    if len(pattern) > len(text):
        return False

    text = text.lower()
    pattern = pattern.lower()

    lps = compute_lps(pattern)
    i = j = 0

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == len(pattern):
            return True  # found match

        elif i < len(text) and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return False

# ====================================================
#           HISTORY + UI HELPERS
# ====================================================

def add_to_search_history(query):
    history = SearchHistory()
    history.add(query)

def strip_colors(text):
    """Strip ANSI color codes for length calculations."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def center_content(content, terminal_width):
    """Center content given terminal width."""
    clean_content = strip_colors(content)
    padding = (terminal_width - len(clean_content)) // 2
    return " " * max(0, padding) + content

YELLOW = "\033[93m"
GREEN  = "\033[92m"
RED    = "\033[91m"
RESET  = "\033[0m"
CYAN   = "\033[96m"

style = Style.from_dict({'placeholder': '#888888 italic'})

def highlight_all(text, words):
    for word in words:
        if word.strip():
            text = re.sub(fr"(?i)\b({re.escape(word)})\b", f"{GREEN}\\1{RESET}", text)
    return text

def is_valid_reference(query):
    return bool(re.fullmatch(r"[A-Za-z0-9 ':]+", query.strip()))

# ====================================================
#            SEARCH FUNCTION (UPDATED)
# ====================================================

def search_bible(bible, query):
    try:
        if not query.strip():
            print(f"{RED}❌ Search query cannot be empty.{RESET}")
            return []

        results = []
        words = query.lower().strip().split()

        # -------------------------------
        #  Case 1: Exact verse search
        # -------------------------------
        if len(words) >= 2 and ":" in words[1]:
            try:
                book_query = words[0]
                chap, verse = words[1].split(":")
                if chap.isdigit() and verse.isdigit():
                    for book, chapters in bible.items():
                        if book.lower().startswith(book_query) and chap in chapters and verse in chapters[chap]:
                            text = chapters[chap][verse]
                            return [(book, chap, verse, text, True)]
                else:
                    print(f"{RED}❌ Invalid format! Use Genesis 2:2{RESET}")
                    return []
            except:
                print(f"{RED}❌ Invalid reference format.{RESET}")
                return []

        # ====================================================
        #  Case 2: Keyword search with RELEVANCE scoring
        # ====================================================
        ranked_results = []

        for book, chapters in bible.items():
            # relevance from book name matches
            book_match_count = sum(1 for w in words if kmp_search(book.lower(), w))

            for chapter, verses in chapters.items():
                for verse, text in verses.items():
                    text_match_count = sum(1 for w in words if kmp_search(text.lower(), w))

                    # total relevance = how many keywords matched
                    relevance = book_match_count + text_match_count

                    if relevance > 0:
                        ranked_results.append({
                            "book": book,
                            "chapter": chapter,
                            "verse": verse,
                            "text": text,
                            "book_match": book_match_count > 0,
                            "relevance": relevance
                        })

        # Sort by:
        # 1. relevance DESC
        # 2. book
        # 3. chapter numeric
        ranked_results.sort(
            key=lambda r: (-r["relevance"], r["book"], int(r["chapter"]), int(r["verse"]))
        )

        # convert back to your usual tuple format
        return [
            (r["book"], r["chapter"], r["verse"], r["text"], r["book_match"])
            for r in ranked_results
        ]

    except Exception as e:
        print(f"{RED}❌ Unexpected error: {e}{RESET}")
        return []

# ====================================================
#            PAGINATED DISPLAY FUNCTIONS
# ====================================================


def show_paginated_results_with_bookmarking(found, words):
    total = len(found)
    index = 0

    while index < total:
        end = min(index + PAGE_SIZE, total)

        # Center page header
        terminal_width_header = 200  # ← CHANGE THIS FOR PAGE HEADER
        print(" ")
        page_header = f"{CYAN}──────────────────────────────────────────────────────────────────────────────────────────────────── {GREEN}● PAGE {(index // PAGE_SIZE) + 1} ●{CYAN} ────────────────────────────────────────────────────────────────────────────────────────────────────────────{RESET}"
        print(" ")
        print(center_content(f"{page_header}", terminal_width_header))

        # Center verse references
        terminal_width_verses = 10 # ← CHANGE THIS FOR VERSE REFERENCES
        # Center verse text  
        terminal_width_text = 40# ← CHANGE THIS FOR VERSE TEXT

        for i, (book, chap, verse, text, book_match) in enumerate(found[index:end], index + 1):
            display_book = highlight_all(book, words) if book_match else book
            display_chap = highlight_all(str(chap), words)
            display_verse = highlight_all(str(verse), words)
            display_text = highlight_all(text, words)

            CREAM = "\033[38;5;223m"
            verse_ref = f"{i}. {CREAM}{display_book} {display_chap}:{display_verse}{RESET}"
            print(center_content(verse_ref, terminal_width_verses))
            print(center_content(display_text, terminal_width_text) + "\n") 
        
        terminal_width_options = 200  # ← CHANGE THIS FOR OPTIONS MENU

        # Create Unicode box around options
        options_box = f"{CYAN}──────────────────────────────────────────────────────────────────────────────┌────────────────────{YELLOW} OPTIONS{RESET}{CYAN} ──────────────────┐────────────────────────────────────────────────────────────────────────────────────────────{RESET}\n"
        options_box += f"{CYAN}     │{RESET}                                               {CYAN}│{RESET}\n"
        options_box += f"{CYAN}     │{RESET}   {GREEN}[1] ➤{RESET}{CREAM} Next Page{RESET}                             {CYAN}│{RESET}\n"
        options_box += f"{CYAN}     │{RESET}   {GREEN}[2] ➤{RESET}{CREAM} Previous Page{RESET}                         {CYAN}│{RESET}\n"
        options_box += f"{CYAN}     │{RESET}   {YELLOW}[3] ➤{RESET}{CREAM} Bookmark{RESET}                              {CYAN}│{RESET}\n"
        options_box += f"{CYAN}     │{RESET}   {YELLOW}[4] ➤{RESET}{CREAM} Search Again{RESET}                          {CYAN}│{RESET}\n"
        options_box += f"{CYAN}     │{RESET}   {RED}[5] ➤{RESET}{CREAM} Exit to Menu{RESET}                          {CYAN}│{RESET}\n"
        options_box += f"{CYAN}     │{RESET}                                               {CYAN}│{RESET}\n"
        options_box += f"{CYAN}     └───────────────────────────────────────────────┘{RESET}"

        # Center and print the entire options box
        options_lines = options_box.split('\n')
        for line in options_lines:
            print(center_content(line, terminal_width_options))
    
        # Center input prompt
        terminal_width_input = 176  # ← CHANGE THIS FOR INPUT PROMPT
        action = input(center_content("Select an option: ", terminal_width_input)).lower()
        if action == '4':
            return "search_again"
        elif action == '5':
            return True
        elif action == '3':
            try:
                sel_prompt = "Enter number to bookmark: "
                sel = int(input(center_content(sel_prompt, terminal_width_input)))
                if index + 1 <= sel <= end:
                    book, chap, verse, text, _ = found[sel - 1]
                    from bookmarks import add_bookmark
                    add_bookmark(book, f"{chap}:{verse}", text)
                    print(center_content("✅ Bookmark added!", terminal_width_input))
                else:
                    print(center_content("❌ Invalid range.", terminal_width_input))
            except:
                print(center_content("❌ Invalid number.", terminal_width_input))
            continue

        # ============================
        # PREVIOUS PAGE
        # ============================
        elif action == '2':
            if index == 0:
                print(center_content("⚠️ Already on the first page.", terminal_width_input))
                continue
            index -= PAGE_SIZE
            continue

        # ============================
        # NEXT PAGE
        # ============================
        elif action == '1':
            if index + PAGE_SIZE >= total:
                print(center_content("⚠️ Already on the last page.", terminal_width_input))
                continue
            index += PAGE_SIZE
            continue

        # ============================
        # EXIT
        # ============================
        else:
            terminal_width_NAH= 190
            print(center_content("❌ Invalid option.", terminal_width_NAH))
            continue

    print(center_content(f"{GREEN}End of results.{RESET}", terminal_width_header))
    return False

# ====================================================
#                  MAIN INTERFACE
# ====================================================
def search_interface(bible):
    YELLOW = "\033[93m"
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    RESET  = "\033[0m"
    CREAM = "\033[38;5;223m"
    # Center ASCII art
    terminal_width = 218 # ← CHANGE THIS FOR ASCII ART
    lines = SEARCH_ART.split('\n')
    for line in lines:
        clean_line = strip_colors(line)
        padding = (terminal_width - len(clean_line)) // 2
        print(" " * padding + f"{CYAN}{line}{RESET}")
    
    # Center titles and menu
    terminal_width = 210  # ← CHANGE THIS FOR MAIN INTERFACE
    terminal_width2 = 211
    terminal_width3 = 188 
    terminal_wide = 208  
   
    print(" ")
    print(center_content(f"{GREEN}Bible Search — KJV Edition{RESET}", terminal_width))
    print(" ")
    print(center_content(f"{CREAM}Search keywords, book names, or exact references.{RESET}", terminal_wide))
    print(" ")
    print(" ")
    print(" ")
    print(center_content(f"{GREEN}Search [1]{RESET}", terminal_width))
    print(" ")
    print(center_content(f"{RED}Back  [2]{RESET}", terminal_width2))
    print(" ")

    while True:   # OUTER MENU LOOP
        choice = input(center_content(f"{YELLOW}SELECT OPTION  {CYAN}➤   {RESET}{RESET}", terminal_width3))

        if choice == '2':
            print(center_content(f"{RED}Exiting search. Goodbye!", terminal_width3))
            return False

        if choice != '1':
            print(center_content("❌ Invalid option. Please enter 1 or 2.", terminal_width3))
            continue

        # =============================
        # INNER SEARCH-SESSION LOOP
        # Runs the search prompt and shows results; if user selects
        # "search again" we loop back to the search prompt directly.
        # =============================
        while True:
            # Center search prompt
            terminal_width_prompt = 200 # ← CHANGE THIS FOR SEARCH PROMPT
            terminal_width_messages = 172  # ← CHANGE THIS FOR MESSAGES
            terminal_width_ARROW = 147  # ← CHANGE THIS FOR MESSAGES
            
            # Box lines
            box_top = f"{GREEN}┌─SEARCH 🔍──────────────────────────────────────────────┐{RESET}"
            box_bottom = f"{GREEN} └────────────────────────────────────────────────────────┘{RESET}"

            # Center each line individually
            print(center_content(box_top, terminal_width_prompt))

            # Your existing prompt
            query = prompt(
                center_content('➤ ', terminal_width_ARROW),
                placeholder='Type your search...',
                style=style
            ).strip()

            print(center_content(box_bottom, terminal_width_prompt))

            if not is_valid_reference(query):
                print(center_content("❌ Invalid input.\n", terminal_width_messages))
                continue

            add_to_search_history(query)
            results = search_bible(bible, query)

            if not results:
                print(center_content("❌ No results found. Try again.\n", terminal_width_messages))
                continue  # stay in the inner search loop

            # =============================
            # SHOW RESULTS
            # =============================
            words = query.lower().split()
            result_flag = show_paginated_results_with_bookmarking(results, words)

            if result_flag == "search_again":
                # loop back to the inner search prompt immediately
                continue
            elif result_flag:
                # exit the search interface and return to main menu
                return True
            else:
                # any other falsey result → exit the search interface
                return False

# ====================================================
#             STANDALONE TEST MODE
# ====================================================

if __name__ == "__main__":
    print("Loading Bible...")
    json_path = os.path.join(os.path.dirname(__file__), "kjv.json")
    parser = JSONBibleParser(json_path)
    bible = parser.load()
    print(f"✅ Loaded {len(bible)} books.")
    print(" ")
    search_interface(bible)
