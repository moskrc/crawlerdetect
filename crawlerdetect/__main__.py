import sys

from crawlerdetect import get_crawlerdetect_version


if __name__ == "__main__":
    if "--version" in sys.argv:
        print(get_crawlerdetect_version())
