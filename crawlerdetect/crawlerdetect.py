import re
from typing import Dict, List, Optional

from crawlerdetect.providers.crawlers import data as crawlers_data
from crawlerdetect.providers.exclusions import data as exclusions_data
from crawlerdetect.providers.headers import data as headers_data


class CrawlerDetect:
    _compiled_crawler_regex: Optional[re.Pattern] = None
    _compiled_exclusions_regex: Optional[re.Pattern] = None
    
    def __init__(self, headers: Optional[Dict[str, str]] = None, user_agent: str = "") -> None:
        self.crawlers: List[str] = crawlers_data
        self.exclusions: List[str] = exclusions_data
        self.user_agent_http_headers: List[str] = headers_data

        self.matches: List[str] = []
        self.http_headers: Dict[str, str] = {}
        self.user_agent: str = ""
        
        self._ensure_compiled_regexes()
        self.set_http_headers(headers)
        self.set_user_agent(user_agent)

    def set_http_headers(self, http_headers: Optional[Dict[str, str]]) -> None:
        self.http_headers = {}
        
        if http_headers:
            self.http_headers = {
                k: v for k, v in http_headers.items() 
                if k.startswith("HTTP_")
            }

    def set_user_agent(self, user_agent: Optional[str] = None) -> None:
        if not user_agent:
            ua_parts = [
                self.http_headers[header] 
                for header in self.get_ua_http_headers()
                if header in self.http_headers
            ]
            self.user_agent = " ".join(ua_parts) + (" " if ua_parts else "")
        else:
            self.user_agent = user_agent

    def get_ua_http_headers(self) -> List[str]:
        """
        All possible HTTP headers that represent user agents
        """
        return self.user_agent_http_headers

    @classmethod
    def _ensure_compiled_regexes(cls) -> None:
        """
        Compile regex patterns once and cache them for better performance
        """
        if cls._compiled_crawler_regex is None:
            crawler_pattern = f'({"|".join(crawlers_data)})'
            cls._compiled_crawler_regex = re.compile(crawler_pattern, re.IGNORECASE)

        if cls._compiled_exclusions_regex is None:
            exclusions_pattern = f'({"|".join(exclusions_data)})'
            cls._compiled_exclusions_regex = re.compile(exclusions_pattern, re.IGNORECASE)
    
    def compile_regex(self, patterns: List[str]) -> str:
        """
        Combine regexps (deprecated - kept for backward compatibility)
        """
        return f'({"|".join(patterns)})'

    def is_crawler(self, user_agent: Optional[str] = None) -> bool:
        if not user_agent:
            if self.user_agent:
                user_agent = self.user_agent
            else:
                return False
        
        user_agent = user_agent.strip()
        if not user_agent:
            return False
        
        agent = self._compiled_exclusions_regex.sub("", user_agent)
        
        if not agent:
            return False
        
        result = self._compiled_crawler_regex.search(agent)
        
        self.matches = []
        
        if result:
            self.matches = [x for x in result.groups() if x]
        
        return bool(self.matches)

    def get_matches(self) -> Optional[str]:
        return self.matches[0] if self.matches else None

    # Backward compatibility aliases
    setHttpHeaders = set_http_headers
    setUserAgent = set_user_agent
    getUaHttpHeaders = get_ua_http_headers
    compileRegex = compile_regex
    isCrawler = is_crawler
    getMatches = get_matches
