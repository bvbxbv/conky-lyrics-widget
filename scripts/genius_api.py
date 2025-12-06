import lyricsgenius
from config import secrets, settings


def init_genius():
    instance = lyricsgenius.Genius(secrets["GENIUS_API_KEY"])
    instance.verbose = settings["verbose"]
    instance.skip_non_songs = settings["skip_non_songs"]
    instance.excluded_terms = settings["excluded_terms"]
    return instance
