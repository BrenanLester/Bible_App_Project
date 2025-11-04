# Bible Search - Standalone Version

This is a **standalone** Bible search application with a beautiful UI.

## 📁 Contents

- **search.py** - Standalone search program with ASCII art banner and colored output
- **bible_parser_json.py** - JSON Bible parser (converts raw JSON to hierarchical structure)
- **kjv.json** - King James Version Bible database (raw JSON format)

## 🚀 How to Run

From the Bible Search Standalone folder:
```bash
python search.py
```

Or from the main Concept directory:
```bash
python "Bible Search Standalone/search.py"
```

## ✨ Features

- 🔍 **Keyword Search** - Search for any word or phrase in the Bible
- 📖 **Exact Verse Lookup** - Find specific verses (e.g., "Genesis 1:1")
- 🎨 **Beautiful UI** - ASCII art banner and colored output
- 📄 **Paginated Results** - Shows 10 results at a time
- 🔤 **Exact Word Matching** - Uses regex for precise word boundary matching
- 💬 **Interactive Prompts** - Uses prompt_toolkit for enhanced input

## 📝 Usage Examples

### Search by Keyword:
```
Search🔍: love
```

### Search by Exact Reference:
```
Search🔍: John 3:16
```

### Search by Book Name:
```
Search🔍: Genesis
```

### Exit:
```
Search🔍: exit
```

## 🎨 UI Preview

```
📖 Bible Search — KJV Edition

 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ...
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌ ...
...

Search by keyword(s), book name, or exact reference (e.g., Genesis 2:2).
Exact word matching is enabled.

Search🔍:  ex:Genesis 1:1 or love...
```

## 🔧 Requirements

- Python 3.6+
- prompt_toolkit library

### Install Dependencies:
```bash
pip install prompt-toolkit
```

## 🔧 Technical Details

This standalone version:
- **Includes** its own `bible_parser_json.py` parser (no external dependencies on other folders)
- **Parses** the raw `kjv.json` file into a hierarchical structure: `bible[Book][Chapter][Verse] = "text"`
- **Uses** the same Bible data structure as the main Bible App
- **Runs** completely independently - all files are self-contained in this folder

## 📦 Integration with Main App

This standalone version is already compatible with the main Bible App. The search logic uses the same Bible dictionary structure.

To use in other files:
1. Import the `search()` function from this file
2. Pass the loaded Bible dictionary
3. Use the returned results in your application

## 🎯 Key Functions

- `search(query)` - Main search function that returns results
- `highlight_all(text, words)` - Highlights matching words in results
- `show_paginated_results(found, words)` - Displays results in pages
- `is_valid_reference(query)` - Validates user input

## 🌟 Enjoy Your Bible Search!

This standalone version provides a fast, beautiful way to search the King James Bible from your terminal!

---

**Note:** This is a **completely standalone** version - all necessary files are included in this folder. You can copy this entire folder anywhere and it will work independently!

