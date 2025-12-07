import sys
from genius_api import genius_instance
from formatter import format_output, print_fill, filter_lyrics, make_genius_url
from transliterator import transliterate
from config import settings


def on_not_found():
    format_output(settings["display"]["empty_filler"])
    format_output(
        settings["display"]["empty_filler"]
        + " "
        + settings["display"]["lyrics_not_found"]
    )
    print_fill(range(settings["fill_lines"] - 2))


def run():
    genius = genius_instance()
    query = sys.stdin.read().strip()

    if not query:
        print_fill(range(settings["fill_lines"]))
        return

    song = None
    try:
        song = genius.search_song(transliterate(query))
    except:
        on_not_found()
        sys.exit()

    if not song or not song.lyrics:
        on_not_found()
        sys.exit()

    lyrics = filter_lyrics(song.lyrics.splitlines())

    for line in lyrics:
        format_output(settings["display"]["empty_filler"] + " " + line)

    free_space = settings["lyrics_area_height"] - len(lyrics) - 1
    print_fill(range(max(0, free_space)), make_genius_url(transliterate(query)))
