import json
import os
import re

from crawlerdetect import CrawlerDetect, get_crawlerdetect_version, providers

from .base_case import CrawlerDetectTestCase


with open(os.path.join(os.path.dirname(__file__), "fixtures/headers.json")) as f:
    test_headers = json.load(f)


class CrawlerDetectTests(CrawlerDetectTestCase):
    def test_get_crawlerdetect_version(self):
        version = get_crawlerdetect_version()
        version_parts = version.split(".")
        self.assertEqual(len(version_parts), 3)
        self.assertTrue(version_parts[0].isdigit())
        self.assertTrue(version_parts[1].isdigit())

    def test_is_crawler(self):
        ua = (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit (KHTML, like Gecko) Mobile "
            "(compatible; Yahoo Ad monitoring; https://help.yahoo.com/kb/yahoo-ad-monitoring-SLN24857.html)"
        )
        res = self.cd.isCrawler(ua)
        self.assertTrue(res)

    def test_user_agents_are_bots(self):
        with open(
            os.path.join(os.path.dirname(__file__), "fixtures/user_agent/crawlers.txt"), "r"
        ) as f:
            for line in f:
                test = self.cd.isCrawler(line)
                self.assertTrue(test, line)

    def test_sec_ch_ua_are_bots(self):
        with open(
            os.path.join(os.path.dirname(__file__), "fixtures/sec_ch_ua/crawlers.txt"), "r"
        ) as f:
            for line in f:
                test = self.cd.isCrawler(line)
                self.assertTrue(test, line)

    def test_user_agents_are_devices(self):
        with open(
            os.path.join(os.path.dirname(__file__), "fixtures/user_agent/devices.txt"), "r"
        ) as f:
            for line in f:
                test = self.cd.isCrawler(line)
                self.assertFalse(test, line)

    def test_sec_ch_ua_are_devices(self):
        with open(
            os.path.join(os.path.dirname(__file__), "fixtures/sec_ch_ua/devices.txt"), "r"
        ) as f:
            for line in f:
                test = self.cd.isCrawler(line)
                self.assertFalse(test, line)

    def test_it_returns_correct_matched_bot_name(self):
        ua = (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit (KHTML, like Gecko) "
            "Mobile (compatible; Yahoo Ad monitoring; https://help.yahoo.com/kb/yahoo-ad-monitoring-SLN24857.html)"
        )
        self.cd.isCrawler(ua)
        matches = self.cd.getMatches()
        self.assertEqual(self.cd.getMatches(), "monitoring", matches)

    def test_it_returns_null_when_no_bot_detected(self):
        self.cd.isCrawler("nothing to see here")
        matches = self.cd.getMatches()
        self.assertEqual(self.cd.getMatches(), None, matches)

    def test_empty_user_agent(self):
        test = self.cd.isCrawler("      ")
        self.assertFalse(test)

    def test_current_visitor(self):
        headers = test_headers["test_current_visitor"]
        cd = CrawlerDetect(headers=headers)
        self.assertTrue(cd.isCrawler())

    def test_user_agent_passed_via_contructor(self):
        ua = (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit (KHTML, like Gecko) Mobile (compatible; "
            "Yahoo Ad monitoring; https://help.yahoo.com/kb/yahoo-ad-monitoring-SLN24857.html)"
        )
        cd = CrawlerDetect(user_agent=ua)
        self.assertTrue(cd.isCrawler())

    def test_http_from_header(self):
        headers = test_headers["test_http_from_header"]
        cd = CrawlerDetect(headers=headers)
        self.assertTrue(cd.isCrawler())

    def test_the_regex_patterns_are_unique(self):
        crawlers = providers.crawlers.Crawlers()
        self.assertEqual(len(crawlers.getAll()), len(set(crawlers.getAll())))

    def test_there_are_no_regex_collisions(self):
        crawlers = providers.crawlers.Crawlers()
        for key1, regex in enumerate(crawlers.getAll()):
            for key2, compare in enumerate(crawlers.getAll()):
                # Dont check this regex against itself
                if key1 != key2:
                    cleaned_compare = (
                        compare.replace("\\n", "\n")
                        .replace("\\r", "\n")
                        .replace("\\", "")
                    )
                    result = re.search(regex, cleaned_compare, flags=re.IGNORECASE)
                    self.assertFalse(result)
