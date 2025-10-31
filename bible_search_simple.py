import json
import re
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

# === Load Bible JSON ===
with open("bible.json", "r", encoding="utf-8") as f:
    bible = json.load(f)

# === Colors (ANSI) ===
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RESET  = "\033[0m"
CYAN   = "\033[96m"


# === Input style for placeholder ===
style = Style.from_dict({'placeholder': '#888888 italic'})

# === Highlight matches (exact word only) ===
def highlight_all(text, words):
    for word in words:
        if word.strip():
            text = re.sub(
                fr"(?i)\b({re.escape(word)})\b",
                f"{GREEN}\\1{RESET}",
                text
            )
    return text

# === Validate input ===
def is_valid_reference(query):
    return bool(re.fullmatch(r"[A-Za-z0-9 ':]+", query.strip()))

# === Search function ===
def search(query):
    results = []
    words = query.lower().strip().split()

    # Case 1: Exact verse search (e.g., Genesis 2:2)
    if len(words) >= 2 and ":" in words[1]:
        book_query = words[0]
        chap_verse = words[1].split(":")
        if len(chap_verse) == 2 and chap_verse[0].isdigit() and chap_verse[1].isdigit():
            chapter_query, verse_query = chap_verse
            for book, chapters in bible.items():
                if book.lower().startswith(book_query) and chapter_query in chapters:
                    if verse_query in chapters[chapter_query]:
                        text = chapters[chapter_query][verse_query]
                        results.append((book, chapter_query, verse_query, text, True))
                        return results
        else:
            print("❌ Invalid format! Use: Genesis 2:2 (book chapter:verse).")
            return []

    # Case 2: Normal keyword or book search (exact words only)
    for book, chapters in bible.items():
        book_match = any(re.search(fr"\b{re.escape(w)}\b", book.lower()) for w in words)
        for chapter, verses in chapters.items():
            for verse, text in verses.items():
                text_match = any(re.search(fr"\b{re.escape(w)}\b", text.lower()) for w in words)
                if book_match or text_match:
                    results.append((book, chapter, verse, text, book_match))
    return results

# === Show results in pages (20 at a time) ===
def show_paginated_results(found, words):
    PAGE_SIZE = 10
    total = len(found)
    index = 0

    while index < total:
        end = min(index + PAGE_SIZE, total)
        for book, chap, verse, text, book_match in found[index:end]:
            display_book = highlight_all(book, words) if book_match else book
            display_chap = highlight_all(str(chap), words)
            display_verse = highlight_all(str(verse), words)
            display_text = highlight_all(text, words)
            print(f"{CYAN}{display_book} {display_chap}:{display_verse}{RESET}")
            print(display_text + "\n")

        index += PAGE_SIZE
        if index < total:
            remaining = total - index
            cont = input(f"🔽 Press Enter to see next {min(PAGE_SIZE, remaining)} results (or type 'q' to stop): ")
            if cont.lower() == 'q':
                break
        else:
            print(f"✅ End of results. Displayed all {total} matches.\n")

# === Main Program ===
print(f"{CYAN}📖 Bible Search — KJV Edition{RESET}")
print(f"""{CYAN}
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄       ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌     ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░▌      ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░▌░▌     ▐░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌     ▐░▌
▐░▌          ▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌     ▐░▌          ▐░▌       ▐░▌▐░▌▐░▌    ▐░▌▐░▌               ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░▌▐░▌    ▐░▌
▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌          ▐░█▄▄▄▄▄▄▄█░▌     ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌ ▐░▌   ▐░▌▐░▌               ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░▌ ▐░▌   ▐░▌
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌  ▐░▌  ▐░▌▐░▌               ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░▌  ▐░▌  ▐░▌
 ▀▀▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀█░█▀▀ ▐░▌          ▐░█▀▀▀▀▀▀▀█░▌     ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░▌   ▐░▌ ▐░▌▐░▌               ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░▌   ▐░▌ ▐░▌
          ▐░▌▐░▌          ▐░▌       ▐░▌▐░▌     ▐░▌  ▐░▌          ▐░▌       ▐░▌     ▐░▌          ▐░▌       ▐░▌▐░▌    ▐░▌▐░▌▐░▌               ▐░▌          ▐░▌     ▐░▌       ▐░▌▐░▌    ▐░▌▐░▌
 ▄▄▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌     ▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░▌     ▐░▐░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░▌      ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░▌     ▐░▐░▌
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌     ▐░▌          ▐░░░░░░░░░░░▌▐░▌      ▐░░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌      ▐░░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀       ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀       ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀ 
{RESET}""")

print("Search by keyword(s), book name, or exact reference (e.g., Genesis 2:2).")
print("Exact word matching is enabled.\n")

while True:
    # Inline placeholder beside 🔍
    query = prompt(
        'Search🔍:  ',
        placeholder='ex:Genesis 1:1 or love...',
        style=style
    ).strip()

    if query.lower() == "exit":
        print(f"{CYAN}Goodbye 👋{RESET}")
        break

    if not query:
        continue

    if not is_valid_reference(query):
        print("❌ Invalid input! Only letters, numbers, spaces, and ':' are allowed.\n")
        continue

    found = search(query)
    if not found:
        print("❌ No results found.\n")
    else:
        words = query.split()
        show_paginated_results(found, words)
