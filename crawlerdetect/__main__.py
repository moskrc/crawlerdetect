import configparser
import os
import sys


def get_crawlerdetect_version():
    config = configparser.ConfigParser()

    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    config_file_path = os.path.join(parent_directory, "setup.cfg")

    config.read(config_file_path)

    return config["crawlerdetect"]["version"]


if __name__ == "__main__":
    if "--version" in sys.argv:
        print(get_crawlerdetect_version())
