# splashpaper

Turn Unsplash to a desktop wallpaper.    
Works on Windows, most Linux DEs and macOS

# Installation

To use this script, you need Python 3.x and `requests` module.    
If `pip` is installed (It is installed with Python by default on Windows and some Linux distributions), you can use

`python -m pip install requests`

to get `requests`

Then just download the script and jump to the next section

# Usage

## Basic

Basic usage is simple:

`python wallpaper.py`

But that would set a random picture! Not really cool...

## Resolution

First of all, the script currently doesn't know your screen resolution.    
Provide it with `-r`/`--resolution` option to fetch smaller picture, e.g:

`python wallpaper.py --resolution 1920x1080`

## Sources

Then you'd probably want some specific images.    
Splashdesktop got your back here!    

You can provide four types of sources (and combine them), each with as many sources as you want:

Search terms with `-s`/`--search` option:

`python wallpaper.py --search sea ocean water`

Collections with `-c`/`--collections` option (that's my dark wallpapers collection, by the way):

`python wallpaper.py --collections 22546183```

User photos with `-u`/`--users` option:

`python wallpaper.py --users erondu aditya1702`

User likes with `-l`/`--likes` option:

`python wallpaper.py --likes qevitta erondu`

## Modifiers

There are three modifiers:

- `--featured`: Use photos picked by Unsplash editors.
- `--daily`: Use photo of the day. 
- `--weekly`: Use photo of the week (overrides `--daily`).

These can be used with any combination of sources.

## Slideshow

If you want to change wallpaper once in a while, you can set interval in seconds with `-i`/`--interval`:

`python wallpaper.py --interval 600`

## Autostart

If this wasn't obvious, you need to add this script to autostart if you want it to work continiously.

# Examples

Photos from [my collection](https://unsplash.com/collections/9943257/wallpapers) of wallpapers, changing every minute
`python wallpaper.py --resolution 1920x1080 --collections 9943257 --interval 60`

Photo of the day from [my collection](https://unsplash.com/collections/9943257/wallpapers) of wallpapers
`python wallpaper.py --resolution 1920x1080 --collections 9943257 --daily`

Water photos, changing every 10 minutes
`python wallpaper.py --resolution 1920x1080 --search water ocean sea --interval 600`

Featured photo of the day
`python wallpaper.py --resolution 1920x1080 --featured --daily`

# Using as a module

You can use script as a module, using dictionary of options as `args`:

```python
from wallpaper import main_action
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
