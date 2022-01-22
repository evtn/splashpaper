import argparse
from time import sleep
from random import choice
from typing import Generator, List, Union, TypedDict
from urllib.parse import quote

try:
    import requests # would fail to import if invoked from setup.py
except ImportError:
    requests = None

from os.path import abspath, dirname
from os import environ
from subprocess import run, DEVNULL, check_output


class About:
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]

    title = "splashpaper"
    description = "Wallpaper manager with unsplash.com integration"
    version = "1.3.3"
    author = "evtn"
    author_email = "g@evtn.ru"
    license = "MIT"
    url = "https://github.com/evtn/splashpaper"


class Args(TypedDict):
    resolution: str
    interval: int
    likes: List[str]
    collections: List[str]
    search: List[str]
    featured: bool
    weekly: bool
    daily: bool
    presets: List[str]


base_url = "https://source.unsplash.com"

presets = {
    "dark": "22546183", 
    "light": "26962183", 
    "wallpapers": "9943257", 
    "abstract": "85975240", 
    "nature": "gQEu_f91tVg", 
    "night": "4PnUeTAlD1s", 
    "city": "vY-yVNran8c",
}

import platform
os_name = platform.system()

if os_name in ["Windows", "nt"]: # apparently Windows Server returns 'nt' instead of 'Windows'
    os_name = "Windows"
    import ctypes


def call(cmd: List[str], **kwargs) -> int:
    return run(cmd, stdout=DEVNULL, stderr=DEVNULL, **kwargs).returncode


def check_de(current_de: str, list_of_de: List[str]) -> bool:
    """Check if any of the strings in ``list_of_de`` is contained in ``current_de``."""
    return any(de in current_de for de in list_of_de)


# I checked gh:markubiak/wallpaper-reddit to get commands for some Linux DE's/WM's (i3, sway)
# But as those are the common commands used in specific environments, I don't really see any reason to mess with license
class Setter: 
    @staticmethod
    def set(path: str) -> None:
        if os_name == "Windows":
            return Setter.set_win(path)
        if os_name == "Darwin":
            return Setter.set_macos(path)
        return Setter.set_linux(path)

    @staticmethod
    def set_win(path: str) -> None:
        ctypes.windll.user32.SystemParametersInfoW(0x14, 0, path, 0x3)

    @staticmethod
    def set_linux(path: str) -> None: 
        de = (environ.get('DESKTOP_SESSION') or '').lower()
        if de:
            if check_de(de, ["xfce", "xubuntu"]):
                # I think that won't create any security problems
                monitors = check_output(
                    "xfconf-query -c xfce4-desktop -l | grep last-image", 
                    shell=True,
                ).decode("utf-8").split("\n")

                for monitor in monitors:
                    call(["xfconf-query", "-c", "xfce4-desktop", "-p", monitor, "-s", path])

            elif check_de(de, ["lubuntu"]):
                call(["pcmanfm", "-w", path])

            elif check_de(de, ["gnome", "unity", "ubuntu", "cinnamon", "pantheon", "budgie-desktop"]):
                ns = "cinnamon" if de == "cinnamon" else "gnome"
                call(["gsettings", "set", "org.%s.desktop.background" % ns, "picture-uri", "file://%s" % path])
            
            elif check_de(de, ["mate"]):
                call(["gsettings", "set", "org.mate.background", "picture-filename", "'%s'" % path])

            elif check_de(de, ["i3", "bspwm", "awesome"]):
                call(["feh", "--bg-center", path])
            
            elif check_de(de, ["sway"]):
                call(["swaymsg", "output * bg %s fill" % path])

        elif not call("command -v termux-wallpaper", shell=True): # detecting termux-wallpaper
            call(["termux-wallpaper", "-f", path])
            call(["termux-wallpaper", "-f", path, "-l"])
            return 
        try:
            call(["feh", "--bg-center", path])
        except FileNotFoundError:
            raise ValueError("DE '%s' is not supported. You could try install feh or use the script as module (writing your own set_wallpaper function)" % de) from None
            

    @staticmethod
    def set_macos(path: str) -> None:
        call(["osascript", "-e", "'tell application \"Finder\" to set desktop picture to POSIX file \"%s\"'" % path])
        call(["killall", "Dock"])

class UQuery:
    
    # sources

    @staticmethod
    def user(username: str) -> str:
        return base_url + "/user/%s" % username

    @staticmethod
    def likes(username: str) -> str:
        return base_url + "/user/%s/likes" % username

    @staticmethod
    def collection(cid: Union[int, str]) -> str:
        return base_url + "/collection/%s" % cid

    # modifiers

    @staticmethod
    def daily(url: str) -> str:
        return url + "/daily"

    @staticmethod
    def weekly(url: str) -> str:
        return url + "/weekly"

    @staticmethod
    def featured(url: str) -> str:
        return url + "/featured"

    @staticmethod
    def resolution(url: str, resolution) -> str:
        return url + "/%s" % resolution

    # search term

    @staticmethod
    def search(url: str, term: str) -> str:
        return url + "?" + quote(term)


def download_file_content(url: str, interval: int = 0) -> Generator[bytes, None, None]:
    if not requests:
        raise requests_error()
    interval_text = f" interval:{args.get('interval')}" if interval else ""
    with requests.get(url, stream=True, headers={"User-Agent": f"evtn:splashpaper/{About.version}{interval_text}"}) as req:
        yield from req.iter_content()


def download_file(url: str, path: str, interval: int = 0) -> str:
    with open(path, 'wb') as file:
        for chunk in download_file_content(url, interval):
            file.write(chunk)
    return path


def build_url(args: Args) -> str:
    sources = {
        "likes": args.get("likes") or [],
        "users": args.get("users") or [],
        "collections": args.get("collections") or [],
        "search": args.get("search") or []
    }
    if args.get("presets"):
        sources["collections"].extend([presets[key] for key in args.get("presets")])

    if not any(sources.values()):
        source_key = ""
        source = ""
    else:
        source_key = choice(
            list(
                filter(
                    sources.get,
                    sources
                )
            )
        )
        source = choice(sources[source_key])
    
    if source_key == "likes":
        url = UQuery.likes(source)
    elif source_key == "users":
        url = UQuery.user(source)
    elif source_key == "collections":
        url = UQuery.collection(source)
    else:
        url = base_url

    if args.get("weekly"):
        url = UQuery.weekly(url)
    elif args.get("daily"):
        url = UQuery.daily(url)
    if args.get("featured"):
        url = UQuery.featured(url)
    if args.get("resolution"):
        url = UQuery.resolution(url, args["resolution"])
    
    if url == base_url:
        url = url + "/random"

    if source_key == "search":
        url = UQuery.search(url, source)

    return url


def set_wallpaper(path: str) -> None:
    return Setter.set(path)


def main_action(args: Args) -> None:
    return set_wallpaper(
        download_file(
            build_url(args), abspath(dirname(__file__)) + "/wallpaper.jpg", args.get("interval", 0)
        )
    )


def main_loop(args: Args) -> None:
    if not requests:
        raise requests_error()
    if not args.get("interval", 0):
        return main_action(args)
    while True:
        try:
            main_action(args)
        except requests.ConnectionError:
            print("connection error, skipping current iteration...")
        sleep(args.get("interval", 0))


def requests_error() -> ImportError:
    return ImportError("Requests module is not imported, it's either a problem with installation or you've deleted it. Reinstall requests to use the module")


parser = argparse.ArgumentParser(description="Set a wallpaper or wallpaper slideshow. Specify as many sources as you want.")

parser.add_argument(
    "-i", "--interval",
    type=int,
    help="Slideshow interval (in seconds). If not specified, script will set wallpaper once and exit.",
    default=0
)
# TODO: get_screen_resolution
parser.add_argument(
    "-r", "--resolution",
    help="Screen resolution (WIDTHxHEIGHT). It's recommended to provide this argument to fetch smaller picture.",
)

sources = parser.add_argument_group("Sources", "If no source is specified, fetches random picture")

sources.add_argument(
    "-l", "--likes",
    nargs="*",
    help="Any number of Unsplash users to choose from their likes, e.g. -l \"qevitta\"",
)

sources.add_argument(
    "-u", "--users", 
    nargs="*",
    help="Any number of Unsplash users to choose from their photos, e.g. -u \"erondu\" \"aditya1702\"",
)

sources.add_argument(
    "-c", "--collections", 
    nargs="*",
    help="Any number of Unsplash collection IDs as source of pictures, e.g. '-c 22546183 26962183'",
)

sources.add_argument(
    "-s", "--search", 
    nargs="*",
    help="Any number of search terms, e.g. '-s nature night'",
)

sources.add_argument(
    "-p", "--presets",
    help="Use images from named collections",
    choices=presets.keys(),
    nargs="*",
)

modifiers = parser.add_argument_group("Modifiers")

modifiers.add_argument(
    "--daily",
    help="Use photo of the day. Overriden by --weekly",
    action="store_true"
)

modifiers.add_argument(
    "--weekly",
    help="Use photo of the week. Overrides --daily",
    action="store_true"
)

modifiers.add_argument(
    "--featured",
    help="Use photos picked by Unsplash editors",
    action="store_true"
)


if __name__ == "__main__":
    args: Args = Args(**vars(parser.parse_args()))
    if not hasattr(args, "help"):
        main_loop(args)






