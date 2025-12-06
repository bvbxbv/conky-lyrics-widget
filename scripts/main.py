import sys
from genius_api import init_genius
from formatter import format_output, print_fill, filter_lyrics, make_genius_url
from transliterator import transliterate
from config import settings


def run():
    genius = init_genius()
    query = sys.stdin.read().strip()

    if not query:
        print_fill()
        return

    song = genius.search_song(transliterate(query))
    if not song or not song.lyrics:
        format_output(settings["display"]["empty_filler"])
        format_output(settings["display"]["lyrics_not_found"])
        print_fill(range(settings["fill_lines"] - 2))
        return

    lyrics = filter_lyrics(song.lyrics.splitlines())

    for line in lyrics:
        format_output(settings["display"]["empty_filler"] + " " + line)

    free_space = settings["lyrics_area_height"] - len(lyrics)
    print_fill(range(max(0, free_space)), make_genius_url(transliterate(query)))
