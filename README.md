# Conky Lyrics Widget

## About project

This is a conky config that displays the title, artist, and lyrics (from [genius.com](https://genius.com/)) of a track, as well as some system data.

# Installation

1. First of all you need conky.

```bash
# with apt
sudo apt update
sudo apt install conky-all

# with pacman
sudo pacman -Syu conky

# with dnf
sudo dnf install conky
```

2. Clone repository

```bash
# i want it to clone in .config directory
# but git will create subdirectory in there
git clone https://github.com/bvbxbv/conky-lyrics-widget.git ~/.config/conky/

# if your directory is empty you may do this
cd ~/.config/conky
git clone https://github.com/bvbxbv/conky-lyrics-widget.git .

# or this (it works anyway)

git clone https://github.com/bvbxbv/conky-lyrics-widget.git /tmp/tmprepo
mv /tmp/tmprepo/* /tmp/tmprepo/.* ~/.config/conky/
rm -rf /tmp/tmprepo
```

3. Install python requirements

```bash
cd ~/.config/conky
pip install -r requirements.txt
```

Pip will install:

-   [LyricsGenius](https://github.com/johnwmillr/LyricsGenius) - nice python api wrapper for getting lyrics (not only lyrics) from [genius](https://genius.com).
-   [tomli](https://github.com/hukkin/tomli) (or not if you have python greater than 3.11)

4. Genius api settings
    1. First of all you need an api key.<br>
       Go to [here](https://genius.com/developers) and click on "Create API CLIENT". 1. Enter app name (whatever) 2. Icon url is not required 3. App website url - i wrote `http://localhost` and it's works 4. Redirect url is not required
    2. Put api key into config file.
        1. Find `~/config/conky/configs/secret.toml.copy` (or where you clone this repo).
        2. Remove `.copy` (`secret.toml.copy` -> `secret.toml`).
        3. Paste your api key instead of `YOUR GENIUS API KEY`.

## Usage

### Running

To run conky you just need run conky and specify path to config:

```bash
conky -c ~/.config/conky/conky.conf
```

If you want set conky as startup app:

-   GUI - just find in your system something like "Startup Applications" (in Pop!\_OS)
    1.  Click "Add"
    2.  Write name of your task (any)
    3.  In textbox "Command" write something like this:
    ```bash
    # i'm not sure if this works with relative paths
    # if you don't want delay before launching script, then remove "sleep 5;"
    bash -c "sleep 5; conky -c /home/$USER/.config/conky/conky.conf > /home/$USER/.config/conky/conky.log 2>&1"
    ```
-   Systemd service

    1.  Create unit file with this content

    ```bash
    # creating
    sudo nano /etc/systemd/system/conky-music.service
    ```

    > NOTE: replace $USER with your username. Systemd hate your path environment variables.

    ```properties
    # content
    [Unit]
    Description=Conky Music + Lyrics Widget
    After=graphical.target

    [Service]
    Type=simple
    User=$USER

    # if you on xorg
    Environment=DISPLAY=:0

    # if you on wayland of xwayland
    # Environment=DISPLAY=%XDG_DISPLAY%
    ExecStart=/usr/bin/conky -c /home/$USER/.config/conky/conky.conf
    Restart=on-failure
    WorkingDirectory=/home/$USER/.config/conky

    [Install]
    WantedBy=default.target
    ```

    2.  Reboot systemd and enable your service

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl --enable --now conky-music.service
    ```

    3.  Check status (Optional)

    ```bash
    systemctl status conky-music.service
    journalctl -u conky-music.service -f
    ```

## Customisation

Everything you need in `config/settings.toml`. If you want to remove something or add, then look at `generate_conky.py`. It's script which needed to make conky and toml configs best friends.

If you need more info about conky features and customisation tricks then look at:

-   [Official conky Github](https://github.com/brndnmtthws/conky)
-   [Official conky site](https://conky.cc/)

### Scripts settings

-   `fill_lines` - number of lines which returns python script.
-   `lyrics_area_height` - number of lines of track lyrics. `38` works perfectly on 1920x1080
-   `skip_if_contains` - lyrics may have line `contributors` or links. If it is, then remove that line.

#### LyricsGenius

-   `verbose` - better set `false`, because [lyricsgenius](https://github.com/johnwmillr/LyricsGenius) write `starting downloading` and things like that.
-   `skip_non_songs` - better set `false`, because [lyricsgenius](https://github.com/johnwmillr/LyricsGenius) may return not only track (e.g. track list)
-   `excluded terms` - exclude songs with these words in their title.
-   `remove_section_header` - remove headers like [CHORUS], [VERSE] and so on

#### text

-   `append_before` - character for indentation (by default it's whitespace).
-   `padding_left` - number of characters to indent from left.

#### intervals

-   `title_update_interval` - interval to update track title
-   `time_update_interval` - interval to update track time (current and length)
-   `lyrics_update_interval` - interval to call python script. There's no caching yet. That's a problem.

#### display

-   `empty_filler` - character after indentation. `~` is pretty good.
-   `lyrics_not_found` - script returns it when page lyrics status is 404.
-   `player_idle` - if playerctl doesnt returns player, then conky prints it.
-   `timer_delimiter` - delimiter between current time and track length (`00:00/2:28` - `timer_delimiter` is `/`).

### Conky settings

#### window

These configs can be found on [conky website](https://conky.cc/)

#### music

-   `title_max_length` - max number of track title characters. If length of track title greater than `title_max_length` then conky prints `"..."`

#### sections

-   `music_section_title` - title of music info block
-   `system_section_title` - title of system info block
-   `memory_section_title` - title of memory info sub block
-   `cpu_section_title` - title of cpu info sub block

## How it works?

-   Conky config file get from `playerctl` all data about track (title, artist, position).
-   Loads from [genius](https://genius.com) with [lyricsgenius](https://github.com/johnwmillr/LyricsGenius) api wrapper lyrics. If script didnt found lyrics its prints `lyrics_not_found` (you can customise it in `configs/settings.toml`)
-   Displays system info with conky stuffs (RAM/Swap usage, uptime, CPU cores load, and simple graph)

## Features

-   customisable with `configs/settings.toml`.

## Requirements

-   Linux with playerctl
-   Python `3.10.12` (just because i used them)
-   Python packages (i hope you already installed them with pip (it you're not then [install](#installation)))
    -   [LyricsGenius](https://github.com/johnwmillr/LyricsGenius)
    -   [tomli](https://github.com/hukkin/tomli) (if you have python greater than `3.11` then you good)

## License

MIT. Do whatever you want.

## Credits

It was useful for me:

-   Conky GitHub - https://github.com/brndnmtthws/conky
-   Conky Website - https://conky.cc/
-   Lyrics Genius python package - https://github.com/johnwmillr/LyricsGenius
-   Genius - https://genius.com/
-   Genius API - https://docs.genius.com/
-   Linux playerctl github - https://github.com/altdesktop/playerctl
-   Linux systemd github - https://github.com/systemd/systemd
-   Linux systemd website - https://systemd.io/
