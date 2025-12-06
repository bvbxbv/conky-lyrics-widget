import lyricsgenius
from config import secrets, settings


def init_genius():
    return lyricsgenius.Genius(
        secrets["GENIUS_API_KEY"],
        verbose=False,
    )
