import re
from typing import Dict, List, Optional, Tuple
from functools import lru_cache

from crawlerdetect.providers.crawlers import data as crawlers_data
from crawlerdetect.providers.exclusions import data as exclusions_data
from crawlerdetect.providers.headers import data as headers_data


@lru_cache(maxsize=1)
def get_compiled_crawler_regex() -> re.Pattern:
    pattern = f'({"|".join(crawlers_data)})'
    return re.compile(pattern, re.IGNORECASE)


@lru_cache(maxsize=1)
def get_compiled_exclusions_regex() -> re.Pattern:
    pattern = f'({"|".join(exclusions_data)})'
    return re.compile(pattern, re.IGNORECASE)


class CrawlerDetect:
    CACHE_SIZE = 1024

    def __init__(
        self,
        headers: Optional[Dict[str, str]] = None,
        user_agent: str = "",
    ) -> None:
        self.matches: List[str] = []
        self.http_headers: Dict[str, str] = {}
        self.user_agent: str = ""

        self.set_http_headers(headers)
        self.set_user_agent(user_agent)

        self._cached_check = lru_cache(maxsize=self.CACHE_SIZE)(self._check_crawler)

    def set_http_headers(self, http_headers: Optional[Dict[str, str]]) -> None:
        self.http_headers = {k: v for k, v in (http_headers or {}).items() if k.startswith("HTTP_")}

    def set_user_agent(self, user_agent: Optional[str] = None) -> None:
        if user_agent:
            self.user_agent = user_agent
        else:
            ua_parts = [
                self.http_headers[header] for header in self.get_ua_http_headers() if header in self.http_headers
            ]
            self.user_agent = " ".join(ua_parts) + (" " if ua_parts else "")

    def get_ua_http_headers(self) -> List[str]:
        return headers_data

    def _check_crawler(self, user_agent: str) -> Tuple[bool, Optional[str]]:
        agent = get_compiled_exclusions_regex().sub("", user_agent)
        if not agent:
            return False, None

        if result := get_compiled_crawler_regex().search(agent):
            for group in result.groups():
                if group:
                    return True, group

        return False, None

    def is_crawler(self, user_agent: Optional[str] = None) -> bool:
        user_agent = (user_agent or self.user_agent).strip()
        if not user_agent:
            return False

        is_bot, matched = self._cached_check(user_agent)
        self.matches = [matched] if matched else []
        return is_bot

    def get_matches(self) -> Optional[str]:
        return self.matches[0] if self.matches else None

    # Backward compatibility aliases
    setHttpHeaders = set_http_headers
    setUserAgent = set_user_agent
    getUaHttpHeaders = get_ua_http_headers
    isCrawler = is_crawler
    getMatches = get_matches
