# splashpaper

Turn Unsplash to a desktop wallpaper.    
Works on Windows, most Linux DEs and macOS

# Installation

To use this script, you need Python 3.x and `requests` module.    
If `pip` is installed (It is installed with Python by default on Windows and some Linux distributions), you can use

```python -m pip install requests```

to get `requests`

Then just download the script and jump to the next section

# Usage

## Basic

Basic usage is simple:

```python wallpaper.py```

But that would set a random picture! Not really cool...

## Resolution

First of all, the script currently doesn't know your screen resolution.    
Provide it with `-r`/`--resolution` option to fetch smaller picture, e.g:

```python wallpaper.py --resolution 1920x1080```

## Sources

Then you'd probably want some specific images.    
Splashdesktop got your back here!    

You can provide four types of sources (and combine them), each with as many sources as you want:

Search terms with `-s`/`--search` option:
```python wallpaper.py --search sea ocean water```

Collections with `-c`/`--collections` option (that's my dark wallpapers collection, by the way):

```python wallpaper.py --collections 22546183```

User photos with `-u`/`--users` option:

```python wallpaper.py --users erondu aditya1702```

User likes with `-l`/`--likes` option:

```python wallpaper.py --likes qevitta erondu```

## Modifiers

There are three modifiers:

- `--featured`: Use photos picked by Unsplash editors.
- `--daily`: Use photo of the day. 
- `--weekly`: Use photo of the week (overrides `--daily`).

These can be used with any combination of sources.

## Slideshow

If you want to change wallpaper once in a while, you can set interval in seconds with `-i`/`--interval`:

```python wallpaper.py --interval 600```

## Autostart

If this wasn't obvious, you need to add this script to autostart if you want it to work continiously.