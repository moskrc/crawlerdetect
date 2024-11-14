"""
CrawlerDetect is Python class for detecting bots/crawlers/spiders via the user agent.
"""

from .src import providers
from .src.crawlerdetect import CrawlerDetect, get_crawlerdetect_version

__all__ = ("CrawlerDetect", "providers", "get_crawlerdetect_version")
