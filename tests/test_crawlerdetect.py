import json
import os
import re

from crawlerdetect import CrawlerDetect
from crawlerdetect import __main__ as main
from crawlerdetect import providers

from .base_case import CrawlerDetectTestCase


class CrawlerDetectTests(CrawlerDetectTestCase):
    def test_get_crawlerdetect_version(self):
        version = main.get_crawlerdetect_version()
        version_parts = version.split(".")
        self.assertEqual(len(version_parts), 3)
        self.assertTrue(version_parts[0].isdigit())
        self.assertTrue(version_parts[1].isdigit())

    def test_is_crawler(self):
        res = self.cd.isCrawler(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit (KHTML, like Gecko) Mobile (compatible; Yahoo Ad monitoring; https://help.yahoo.com/kb/yahoo-ad-monitoring-SLN24857.html)"
        )
        self.assertTrue(res)

    def test_user_agents_are_bots(self):
        with open(
            os.path.join(os.path.dirname(__file__), "fixtures/crawlers.txt"), "r"
        ) as f:
            for line in f:
                test = self.cd.isCrawler(line)
                self.assertTrue(test, line)

    def test_user_agents_are_devices(self):
        with open(
            os.path.join(os.path.dirname(__file__), "fixtures/devices.txt"), "r"
        ) as f:
            for line in f:
                test = self.cd.isCrawler(line)
                self.assertFalse(test, line)

    def test_it_returns_correct_matched_bot_name(self):
        self.cd.isCrawler(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit (KHTML, like Gecko) Mobile (compatible; Yahoo Ad monitoring; https://help.yahoo.com/kb/yahoo-ad-monitoring-SLN24857.html)"
        )
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
        headers = json.loads(
            '{"DOCUMENT_ROOT":"\/home\/test\/public_html","GATEWAY_INTERFACE":"CGI\/1.1","HTTP_ACCEPT":"*\/*","HTTP_ACCEPT_ENCODING":"gzip, deflate","HTTP_CACHE_CONTROL":"no-cache","HTTP_CONNECTION":"Keep-Alive","HTTP_FROM":"bingbot(at)microsoft.com","HTTP_HOST":"www.test.com","HTTP_PRAGMA":"no-cache","HTTP_USER_AGENT":"Mozilla\/5.0 (compatible; bingbot\/2.0; +http:\/\/www.bing.com\/bingbot.htm)","PATH":"\/bin:\/usr\/bin","QUERY_STRING":"order=closingDate","REDIRECT_STATUS":"200","REMOTE_ADDR":"127.0.0.1","REMOTE_PORT":"3360","REQUEST_METHOD":"GET","REQUEST_URI":"\/?test=testing","SCRIPT_FILENAME":"\/home\/test\/public_html\/index.php","SCRIPT_NAME":"\/index.php","SERVER_ADDR":"127.0.0.1","SERVER_ADMIN":"webmaster@test.com","SERVER_NAME":"www.test.com","SERVER_PORT":"80","SERVER_PROTOCOL":"HTTP\/1.1","SERVER_SIGNATURE":"","SERVER_SOFTWARE":"Apache","UNIQUE_ID":"Vx6MENRxerBUSDEQgFLAAAAAS","PHP_SELF":"\/index.php","REQUEST_TIME_FLOAT":1461619728.0705,"REQUEST_TIME":1461619728}'
        )
        cd = CrawlerDetect(headers=headers)
        self.assertTrue(cd.isCrawler())

    def test_user_agent_passed_via_contructor(self):
        cd = CrawlerDetect(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit (KHTML, like Gecko) Mobile (compatible; Yahoo Ad monitoring; https://help.yahoo.com/kb/yahoo-ad-monitoring-SLN24857.html)"
        )
        self.assertTrue(cd.isCrawler())

    def test_http_from_header(self):
        headers = json.loads(
            '{"DOCUMENT_ROOT":"\/home\/test\/public_html","GATEWAY_INTERFACE":"CGI\/1.1","HTTP_ACCEPT":"*\/*","HTTP_ACCEPT_ENCODING":"gzip, deflate","HTTP_CACHE_CONTROL":"no-cache","HTTP_CONNECTION":"Keep-Alive","HTTP_FROM":"googlebot(at)googlebot.com","HTTP_HOST":"www.test.com","HTTP_PRAGMA":"no-cache","HTTP_USER_AGENT":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/28.0.1500.71 Safari\/537.36","PATH":"\/bin:\/usr\/bin","QUERY_STRING":"order=closingDate","REDIRECT_STATUS":"200","REMOTE_ADDR":"127.0.0.1","REMOTE_PORT":"3360","REQUEST_METHOD":"GET","REQUEST_URI":"\/?test=testing","SCRIPT_FILENAME":"\/home\/test\/public_html\/index.php","SCRIPT_NAME":"\/index.php","SERVER_ADDR":"127.0.0.1","SERVER_ADMIN":"webmaster@test.com","SERVER_NAME":"www.test.com","SERVER_PORT":"80","SERVER_PROTOCOL":"HTTP\/1.1","SERVER_SIGNATURE":"","SERVER_SOFTWARE":"Apache","UNIQUE_ID":"Vx6MENRxerBUSDEQgFLAAAAAS","PHP_SELF":"\/index.php","REQUEST_TIME_FLOAT":1461619728.0705,"REQUEST_TIME":1461619728}'
        )
        print(headers)
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
