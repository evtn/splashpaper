# splashpaper

Turn Unsplash into a desktop wallpaper.    
Works on Windows, most Linux DEs/WMs, macOS and Android (check [compatibility](#compatibility))

# Installation

To use this script, you need Python 3.6+ and pip installed.    
Then, just run:

`python -m pip install splashpaper`

# Getting help

It's as simple as:

`python -m splashpaper --help`    

That would print help (mostly the same information as below, but shorter)    

# Usage

## Basic

Basic usage is simple:

`python -m splashpaper`

But that would set a random picture! Not really cool...

## Resolution

First of all, the script currently doesn't know your screen resolution.    
Provide it with `-r`/`--resolution` option to fetch smaller picture, e.g:

`python -m splashpaper --resolution 1920x1080`

## Sources

Then you'd probably want some specific images.    
Splashdesktop got your back here!    

You can provide four types of sources (and combine them), each with as many sources as you want:

### Search terms

With `-s`/`--search` option:

`python -m splashpaper --search sea ocean water`

### Collections 

With `-c`/`--collections` option (that's my dark wallpapers collection, by the way):

`python -m splashpaper --collections 22546183`

### Presets

If you don't really know where to look:    

`python -m splashpaper --presets dark`

Available options: `dark, light, all-wallpapers, abstract, nature, night, city`

### User photos

With `-u`/`--users` option:

`python -m splashpaper --users erondu aditya1702`

### User likes

With `-l`/`--likes` option:

`python -m splashpaper --likes qevitta erondu`

## Modifiers

There are three modifiers:

- `--featured`: Use photos picked by Unsplash editors.
- `--daily`: Use photo of the day. 
- `--weekly`: Use photo of the week (overrides `--daily`).

These can be used with any combination of sources.

## Slideshow

If you want to change wallpaper once in a while, you can set interval in seconds with `-i`/`--interval`:

`python -m splashpaper --interval 600`

## Autostart

If this wasn't obvious, you need to add this script to autostart if you want it to work continiously.

# Examples

Photos from [my collection](https://unsplash.com/collections/9943257/wallpapers) of wallpapers, changing every minute

`python -m splashpaper --resolution 1920x1080 --collections 9943257 --interval 60`

Photo of the day from [my collection](https://unsplash.com/collections/9943257/wallpapers) of wallpapers

`python -m splashpaper --resolution 1920x1080 --collections 9943257 --daily`

Water photos, changing every 10 minutes

`python -m splashpaper --resolution 1920x1080 --search water ocean sea --interval 600`

Featured photo of the day

`python -m splashpaper --resolution 1920x1080 --featured --daily`

# Using as a module

You can use script as a module, using dictionary of options as `args`:

```python
from splashpaper import main_action
from time import sleep

args = {
    "collections": ["9943257"],
    "resolution": "1920x1080",
}

while True:
    main_action(args)
    sleep(60)

```

## Functions
Script uses a very modular workflow.    
By default, script calls `main_loop(args)`, which in turn calls `main_action(args)` once or with interval.

`main_action(args)` is defined as:

```python
def main_action(args):
    return set_wallpaper(
        download_file(
            build_url(args), 
            abspath(dirname(__file__)) + "/wallpaper.jpg"
        )
    )
```

This snippet shows that:

- To build a URL based on your args, script uses `build_url(args)`
- To download a picture from that URL, script uses `download(url, path)`, which returns path
- To set picture as a wallpaper, script uses `set_wallpaper(path)`


# Compatibility

Splashpaper runs on:

- Windows
- macOS (**Warning: when changing wallpaper, Dock restarts and screen may freeze for half a second.**)
- Linux
    - XFCE
    - LXDE/LXQt
    - Gnome
    - Unity
    - Cinnamon
    - Mate
    - i3
    - bspwm
    - awesome
    - sway
    - ... and also any other de/wm where feh can change wallpaper (used as a fallback)
- Android

## Usage on Android

To use module on Android: 

1. Install Termux.    
2. In Termux, install Python (`pkg install python`) and Termux:API (`pkg install termux-api`) if it's not already installed.
3. Install module in Termux just as on desktop: (`python -m pip install splashpaper`)
4. [Use it!](#usage)