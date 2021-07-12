import argparse
from time import sleep
from random import choice
from urllib.parse import urlencode
import requests
import shutil
from os.path import abspath, dirname
from os import environ
from subprocess import call as call_, DEVNULL, check_output


class About:
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]

    with open("README.md") as file:
        long_description = file.read()

    title = "splashpaper"
    description = "Wallpaper manager with unsplash.com integration"
    version = "1.0.4"
    author = "evtn"
    author_email = "g@evtn.ru"
    license = "MIT"
    url = "https://github.com/evtn/splashpaper"


base_url = "https://source.unsplash.com"

import platform
os_name = platform.system()

if os_name in ["Windows", "nt"]: # apparently Windows Server returns 'nt' instead of 'Windows'
    os_name = "Windows"
    import ctypes


def call(cmd):
    return call_(cmd, stdout=DEVNULL, stderr=DEVNULL)


def check_de(current_de, list_of_de):
    """Check if any of the strings in ``list_of_de`` is contained in ``current_de``."""
    return any(de in current_de for de in list_of_de)


# I checked gh:markubiak/wallpaper-reddit to get commands for some Linux DE's/WM's (i3, sway)
# But as those are the common commands used in specific environments, I don't really see any reason to mess with license
class Setter: 
    def set(path):
        if os_name in "Windows":
            return Setter.set_win(path)
        if os_name == "Darwin":
            return Setter.set_macos(path)
        return Setter.set_linux(path)

    def set_win(path):
        return ctypes.windll.user32.SystemParametersInfoW(0x14, 0, path, 0x3)

    def set_linux(path): 
        de = environ.get('DESKTOP_SESSION').lower()
        
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

        else:
            raise ValueError("DE '%s' is not supported. You could try use the script as module or modify the file." % de)

    def set_macos(path):
        call(["osascript", "-e" "'tell application \"Finder\" to set desktop picture to POSIX file \"%s\"'" % path])

class UQuery:
    
    #sources

    def user(username):
        return base_url + "/user/%s" % username

    def likes(username):
        return base_url + "/user/%s/likes" % username

    def collection(cid):
        return base_url + "/collection/%s" % cid

    # modifiers

    def daily(url):
        return url + "/daily"

    def weekly(url):
        return url + "/weekly"

    def featured(url):
        return url + "/featured"

    def resolution(url, resolution):
        return url + "/%s" % resolution

    # search term

    def search(url, terms):
        return url + "?" + urlencode(",".join(terms))



def download_file(url, path):
    with requests.get(url, stream=True) as req:
        with open(path, 'wb') as file:
            shutil.copyfileobj(req.raw, file)
    return path


def build_url(args):
    sources = {
        "likes": args.get("likes", []),
        "users": args.get("users", []),
        "collections": args.get("collections", []),
        "search": args.get("search", [])
    }
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


def set_wallpaper(path):
    return Setter.set(path)


def main_action(args):
    return set_wallpaper(
        download_file(
            build_url(args), abspath(dirname(__file__)) + "/wallpaper.jpg"
        )
    )


def main_loop(args):
    if not args.interval:
        return main_action(vars(args))
    while True:
        try:
            main_action(vars(args))
        except requests.ConnectionError:
            print("connection error, skipping current iteration...")
        sleep(args.interval)


if __name__ == "__main__":
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
    args = parser.parse_args()
    if not hasattr(args, "help"):
        main_loop(args)






