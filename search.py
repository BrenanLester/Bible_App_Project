"""Search utilities using KMP for algorithmic string matching."""

def _compute_lps(pattern: str):
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


def kmp_search(text: str, pattern: str) -> bool:
    if not pattern:
        return False
    t = text.lower()
    p = pattern.lower()
    lps = _compute_lps(p)
    i = j = 0
    while i < len(t):
        if t[i] == p[j]:
            i += 1
            j += 1
            if j == len(p):
                return True
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False


def search_bible(bible, query):
    """Search through nested bible dict {book: {chapter: {verse: text}}}.

    Returns list of tuples (book, chapter:verse, text)
    """
    if not query:
        return []
    results = []
    for book, chapters in bible.items():
        for chapter, verses in chapters.items():
            for verse_num, verse_text in verses.items():
                if kmp_search(verse_text, query):
                    results.append((book, f"{chapter}:{verse_num}", verse_text))
    return results
