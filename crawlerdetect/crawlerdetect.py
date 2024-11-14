import re

from crawlerdetect.providers.crawlers import data as crawlers_data
from crawlerdetect.providers.exclusions import data as exclusions_data
from crawlerdetect.providers.headers import data as headers_data


class CrawlerDetect:
    def __init__(self, headers=None, user_agent=""):
        self.crawlers = crawlers_data
        self.exclusions = exclusions_data
        self.uaHttpHeaders = headers_data

        self.compiledRegex = self.compileRegex(self.crawlers)
        self.compiledExclusions = self.compileRegex(self.exclusions)
        self.matches = []

        self.setHttpHeaders(headers)
        self.setUserAgent(user_agent)

    def setHttpHeaders(self, http_headers):
        self.httpHeaders = {}

        if http_headers:
            for k, v in http_headers.items():
                if k.find("HTTP_") == 0:
                    self.httpHeaders[k] = v

    def setUserAgent(self, user_agent=None):
        if not user_agent:
            ua = ""

            for altHeader in self.getUaHttpHeaders():
                if altHeader in self.httpHeaders:
                    ua += self.httpHeaders[altHeader] + " "

            self.user_agent = ua
        else:
            self.user_agent = user_agent

    def getUaHttpHeaders(self):
        """
        All possible HTTP headers that represent user agents
        """
        return self.uaHttpHeaders

    def compileRegex(self, patterns):
        """
        Combine regexps
        """
        return "({})".format("|".join(patterns))

    def isCrawler(self, user_agent=None):
        if not user_agent:
            if self.user_agent:
                user_agent = self.user_agent
            else:
                return False

        agent = re.sub(self.compiledExclusions, "", user_agent, flags=re.IGNORECASE)

        if not agent:
            return False

        result = re.search(self.compiledRegex, agent, flags=re.IGNORECASE)

        self.matches = []

        if result:
            self.matches = [x for x in result.groups() if x]

        return len(self.matches) > 0

    def getMatches(self):
        return self.matches[0] if self.matches else None
