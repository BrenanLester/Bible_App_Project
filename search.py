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

def show_paginated_results(found, words):
    try:
        total = len(found)
        index = 0
        results = []
        current_page = 1

        while index < total:
            end = min(index + PAGE_SIZE, total)
            total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE
            
            print(f"\n{CYAN}📄 Page {current_page} of {total_pages}{RESET}")
            print(f"{CYAN}{'='*50}{RESET}\n")

            for book, chap, verse, text, book_match in found[index:end]:
                display_book = highlight_all(book, words) if book_match else book
                display_chap = highlight_all(str(chap), words)
                display_verse = highlight_all(str(verse), words)
                display_text = highlight_all(text, words)

                print(f"{CYAN}{display_book} {display_chap}:{display_verse}{RESET}")
                print(display_text + "\n")

                results.append((book, f"{chap}:{verse}", text))

            index += PAGE_SIZE
            current_page += 1

            if index < total:
                resp = input("\n🔽 Options \n [1] Next Page \n [2] Previous Page \n [3] Quit").lower()
                try:
                    if resp == '1' and index > PAGE_SIZE:
                        index -= 2 * PAGE_SIZE
                        current_page += 2
                    elif resp == '2' and index > PAGE_SIZE:
                        index -= 2 * PAGE_SIZE
                        current_page -= 2
                    else:
                        print("Are you sure you want to quit? \n [1] Yes \n [2] No: ", end="")
                        confirm = input()
                        if confirm == '2':
                            continue
                        else:
                            break
                except:
                    print(f"{RED}❌ Invalid option. Exiting.{RESET}")
                    break
            else:
                print(f"{GREEN}✅ End of results.{RESET}\n")

        return results

    except Exception as e:
        print(f"{RED}❌ Error displaying results: {e}{RESET}")
        return None


def show_paginated_results_with_bookmarking(found, words):
    total = len(found)
    index = 0

    while index < total:
        end = min(index + PAGE_SIZE, total)
        print(f"\n{GREEN}=== Page {(index // PAGE_SIZE) + 1} ==={RESET}")

        for i, (book, chap, verse, text, book_match) in enumerate(found[index:end], index + 1):
            display_book = highlight_all(book, words) if book_match else book
            display_chap = highlight_all(str(chap), words)
            display_verse = highlight_all(str(verse), words)
            display_text = highlight_all(text, words)

            print(f"{i}. {display_book} {display_chap}:{display_verse}")
            print(display_text + "\n")
        print("\n🔽 Options \n [1] Next Page \n [2] Previous Page \n [3] Bookmark \n [4] Exit to Menu\n")
        action = input("Select an option: ").lower()

        if action == '3':
            try:
                sel = int(input("Enter number to bookmark: "))
                if index + 1 <= sel <= end:
                    book, chap, verse, text, _ = found[sel - 1]
                    from bookmarks import add_bookmark
                    add_bookmark(book, f"{chap}:{verse}", text)
                    print("✅ Bookmark added!")
                else:
                    print("❌ Invalid range.")
            except:
                print("❌ Invalid number.")
            continue

        # ============================
        # PREVIOUS PAGE
        # ============================
        elif action == '2':
            if index == 0:
                print("⚠️ Already on the first page.")
                continue
            index -= PAGE_SIZE
            continue

        # ============================
        # NEXT PAGE
        # ============================
        elif action == '1':
            if index + PAGE_SIZE >= total:
                print("⚠️ Already on the last page.")
                continue
            index += PAGE_SIZE
            continue

        # ============================
        # EXIT
        # ============================
        elif action == '4':
            return True

        else:
            print("❌ Invalid option.")
            continue

    print(f"{GREEN}End of results.{RESET}")
    return False

# ====================================================
#                  MAIN INTERFACE
# ====================================================
def search_interface(bible):
    print(CYAN + SEARCH_ART + RESET)
    print(f"{CYAN}📖 Bible Search — KJV Edition{RESET}")
    print("Search keywords, book names, or exact references.")
    print("\n [1] Search \n [2] Exit\n")

    while True:   # OUTER MENU LOOP
        choice = input("Select an option: ")

        if choice == '2':
            print("Exiting search. Goodbye!")
            return False

        # =============================
        # INNER SEARCH LOOP
        # Keeps asking until results exist
        # =============================
        while True:
            query = prompt(
                'Search🔍: ',
                placeholder='ex: Genesis 1:1 or love faith...',
                style=style
            ).strip()

            if not is_valid_reference(query):
                print("❌ Invalid input.\n")
                continue

            add_to_search_history(query)
            results = search_bible(bible, query)

            if results:
                break  # success → exit search loop
            else:
                print("❌ No results found. Try again.\n")

        # =============================
        # SHOW RESULTS
        # =============================
        words = query.lower().split()
        should_return = show_paginated_results_with_bookmarking(results, words)

        if should_return:
            return True



# ====================================================
#             STANDALONE TEST MODE
# ====================================================

if __name__ == "__main__":
    print("Loading Bible...")
    json_path = os.path.join(os.path.dirname(__file__), "kjv.json")
    parser = JSONBibleParser(json_path)
    bible = parser.load()
    print(f"✅ Loaded {len(bible)} books.\n")
    search_interface(bible)
