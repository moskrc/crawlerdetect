"""
CrawlerDetect is Python class for detecting bots/crawlers/spiders via the user agent.
"""
from .src.crawlerdetect import CrawlerDetect
from .src import providers

__all__ = (
    'CrawlerDetect',
    'providers'
)
