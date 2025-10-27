"""JSON-backed Terminal Bible App.

This is a separate version of the Bible App that reads `kjv.json` and
implements the same features required by the project guidelines.
"""
import os
from bible_parser_json import JSONBibleParser
from search import search_bible
from bookmarks import add_bookmark, view_bookmarks, remove_bookmark
from history import add_to_history, view_history
from verse_of_the_day import verse_of_the_day


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # look for kjv.json
    json_candidate = os.path.join(os.path.dirname(script_dir), 'kjv.json')
    if not os.path.isfile(json_candidate):
        json_candidate = os.path.join(script_dir, 'kjv.json')
    parser = JSONBibleParser(json_candidate)
    try:
        bible = parser.load()
    except Exception as e:
        print('Failed to load JSON Bible:', e)
        return

    while True:
        print('\n=== JSON Bible App ===')
        print('[1] Search Verse')
        print('[2] Add Bookmark (manual)')
        print('[3] View / Remove Bookmarks')
        print('[4] Verse of the Day')
        print('[5] Search History')
        print('[6] Exit')

        choice = input('Enter choice: ').strip()
        if choice == '1':
            query = input('Enter keyword or phrase: ').strip()
            add_to_history(query)
            results = search_bible(bible, query)
            if results:
                for i, (book, ref, text) in enumerate(results, 1):
                    print(f"{i}. {book} {ref} - {text}")
                if input('Bookmark a result? (y/n): ').strip().lower() == 'y':
                    try:
                        idx = int(input('Number to bookmark: '))
                        if 1 <= idx <= len(results):
                            book, ref, text = results[idx-1]
                            add_bookmark(book, ref, text)
                        else:
                            print('Invalid number.')
                    except ValueError:
                        print('Invalid input.')
            else:
                print('No results found.')
        elif choice == '2':
            book = input('Enter Book name: ').strip()
            ref = input('Enter Chapter:Verse (e.g. 3:16): ').strip()
            try:
                ch, v = ref.split(':',1)
                text = parser.get_verse(book, ch, v)
            except Exception:
                text = input('Enter verse text: ').strip()
            add_bookmark(book, ref, text)
        elif choice == '3':
            view_bookmarks()
            if input('Remove a bookmark? (y/n): ').strip().lower() == 'y':
                try:
                    num = int(input('Enter bookmark number: '))
                    remove_bookmark(num)
                except ValueError:
                    print('Invalid input.')
        elif choice == '4':
            verse_of_the_day(bible)
        elif choice == '5':
            view_history()
        elif choice == '6':
            print('Goodbye!')
            break
        else:
            print('Invalid choice.')


if __name__ == '__main__':
    main()
