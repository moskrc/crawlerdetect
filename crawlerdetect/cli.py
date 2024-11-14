import sys

from crawlerdetect import __version__

if __name__ == "__main__":
    print("HERE")
    if "--version" in sys.argv:
        print(__version__)
