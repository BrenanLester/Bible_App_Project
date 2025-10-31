import os
import json
import random

# --- Book mapping table (for converting book IDs to names) ---
book_mapping = {
    1: "Genesis", 2: "Exodus", 3: "Leviticus", 4: "Numbers",
    5: "Deuteronomy", 6: "Joshua", 7: "Judges", 8: "Ruth",
    9: "1 Samuel", 10: "2 Samuel", 11: "1 Kings", 12: "2 Kings",
    13: "1 Chronicles", 14: "2 Chronicles", 15: "Ezra", 16: "Nehemiah",
    17: "Esther", 18: "Job", 19: "Psalms", 20: "Proverbs",
    21: "Ecclesiastes", 22: "Song of Solomon", 23: "Isaiah",
    24: "Jeremiah", 25: "Lamentations", 26: "Ezekiel", 27: "Daniel",
    28: "Hosea", 29: "Joel", 30: "Amos", 31: "Obadiah", 32: "Jonah",
    33: "Micah", 34: "Nahum", 35: "Habakkuk", 36: "Zephaniah",
    37: "Haggai", 38: "Zechariah", 39: "Malachi", 40: "Matthew",
    41: "Mark", 42: "Luke", 43: "John", 44: "Acts", 45: "Romans",
    46: "1 Corinthians", 47: "2 Corinthians", 48: "Galatians",
    49: "Ephesians", 50: "Philippians", 51: "Colossians",
    52: "1 Thessalonians", 53: "2 Thessalonians", 54: "1 Timothy",
    55: "2 Timothy", 56: "Titus", 57: "Philemon", 58: "Hebrews",
    59: "James", 60: "1 Peter", 61: "2 Peter", 62: "1 John",
    63: "2 John", 64: "3 John", 65: "Jude", 66: "Revelation"
}

class BibleParserJSON:
    """
    Loads Bible data from a single JSON file (kjv.json) and stores it
    in a hierarchical structure:
        bible[Book][Chapter][Verse] = "text"
    """

    def __init__(self, json_path: str):
        self.json_path = json_path
        self.bible = {}  # nested dictionary: Book → Chapter → Verse

    def load_all_books(self):
        """Loads Bible data from the JSON file and builds the hierarchy."""
        if not os.path.exists(self.json_path):
            print("Error: Bible JSON file not found.")
            return {}

        with open(self.json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # expected format: { "resultset": { "row": [ { "field": [...] } ] } }
        rows = data.get("resultset", {}).get("row", [])

        for row in rows:
            fields = row.get("field", [])
            if len(fields) < 5:
                continue  # skip invalid entries

            book_id = fields[1]
            chapter = str(fields[2])
            verse = str(fields[3])
            text = fields[4]

            # convert book ID to book name using the mapping
            book_name = book_mapping.get(book_id, f"Book_{book_id}")

            # build the hierarchical tree (dict of dicts)
            self.bible.setdefault(book_name, {}).setdefault(chapter, {})[verse] = text

        print(f"✅ Bible loaded successfully! Books: {len(self.bible)}")
        return self.bible

    def get_verse(self, book, chapter, verse):
        """Returns a specific verse (Book → Chapter → Verse)."""
        try:
            return self.bible[book][str(chapter)][str(verse)]
        except KeyError:
            return "Verse not found."

    def get_random_verse(self):
        """Selects and returns a random verse (for Verse of the Day)."""
        if not self.bible:
            return "Bible not loaded."

        book = random.choice(list(self.bible.keys()))
        chapter = random.choice(list(self.bible[book].keys()))
        verse = random.choice(list(self.bible[book][chapter].keys()))
        verse_text = self.bible[book][chapter][verse]

        return f"{book} {chapter}:{verse} — {verse_text}"
    
    def load(self):
        """Compatibility function to match the main.py call."""
        return self.load_all_books()

# Alias for backward compatibility
JSONBibleParser = BibleParserJSON

