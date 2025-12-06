import re
from config import settings


def format_output(to_display):
    after = settings["text"]["append_after"] * settings["text"]["padding_left"]
    print(after + to_display)


# lines - number of lines to fill custom value.
# It's neede to place system info block to bottom
# append - append value in bottom
def print_fill(lines=None, append=""):
    lines = lines or range(settings["fill_lines"])
    for _ in lines:
        format_output(settings["display"]["empty_filler"])
    if append:
        format_output(append)


# line - result string from playerctl of format band - title
# transform this string to genius lyric url
def make_genius_url(line):
    parts = re.split(r"\s*-\s*", line, maxsplit=1)
    artist = parts[0]
    title = parts[1] if len(parts) > 1 else ""

    combined = f"{artist} {title}".strip()
    combined = re.sub(r"[^A-Za-z0-9 ]+", "", combined)
    slug = "-".join(combined.lower().split())

    return f"https://genius.com/{slug}-lyrics"


# lines - genius_api result
# filter result by your filters (settings.toml -> skip_if_contains)
def filter_lyrics(lines):
    result = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if any(term.lower() in line.lower() for term in settings["skip_if_contains"]):
            continue
        result.append(line)
    return result
