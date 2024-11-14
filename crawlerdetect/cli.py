import sys

from crawlerdetect import __version__


def main():
    if "--version" in sys.argv:
        print(__version__)


if __name__ == "__main__":
    main()
