import random

def verse_of_the_day(bible):
    books = list(bible.keys())
    if not books:
        return "Bible not loaded."
    book = random.choice(books)
    chapter = random.choice(list(bible[book].keys()))
    verse = random.choice(list(bible[book][chapter].keys()))
    text = bible[book][chapter][verse]
    return f"{book} {chapter}:{verse} — {text}"
