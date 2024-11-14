## About CrawlerDetect

This is a Python wrapper for [CrawlerDetect](https://github.com/JayBizzle/Crawler-Detect) - the web crawler detection library
It helps to detect bots/crawlers/spiders via the user agent and other HTTP-headers. Currently able to detect > 1,000's of bots/spiders/crawlers.

### Installation
Run `pip install crawlerdetect`

### Usage

#### Variant 1
```Python
from crawlerdetect import CrawlerDetect
crawler_detect = CrawlerDetect()
crawler_detect.isCrawler('Mozilla/5.0 (compatible; Sosospider/2.0; +http://help.soso.com/webspider.htm)')
# true if crawler user agent detected
```

#### Variant 2
```Python
from crawlerdetect import CrawlerDetect
crawler_detect = CrawlerDetect(user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit (KHTML, like Gecko) Mobile (compatible; Yahoo Ad monitoring; https://help.yahoo.com/kb/yahoo-ad-monitoring-SLN24857.html)')
crawler_detect.isCrawler()
# true if crawler user agent detected
```

#### Variant 3
```Python
from crawlerdetect import CrawlerDetect
crawler_detect = CrawlerDetect(headers={'DOCUMENT_ROOT': '/home/test/public_html', 'GATEWAY_INTERFACE': 'CGI/1.1', 'HTTP_ACCEPT': '*/*', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate', 'HTTP_CACHE_CONTROL': 'no-cache', 'HTTP_CONNECTION': 'Keep-Alive', 'HTTP_FROM': 'googlebot(at)googlebot.com', 'HTTP_HOST': 'www.test.com', 'HTTP_PRAGMA': 'no-cache', 'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36', 'PATH': '/bin:/usr/bin', 'QUERY_STRING': 'order=closingDate', 'REDIRECT_STATUS': '200', 'REMOTE_ADDR': '127.0.0.1', 'REMOTE_PORT': '3360', 'REQUEST_METHOD': 'GET', 'REQUEST_URI': '/?test=testing', 'SCRIPT_FILENAME': '/home/test/public_html/index.php', 'SCRIPT_NAME': '/index.php', 'SERVER_ADDR': '127.0.0.1', 'SERVER_ADMIN': 'webmaster@test.com', 'SERVER_NAME': 'www.test.com', 'SERVER_PORT': '80', 'SERVER_PROTOCOL': 'HTTP/1.1', 'SERVER_SIGNATURE': '', 'SERVER_SOFTWARE': 'Apache', 'UNIQUE_ID': 'Vx6MENRxerBUSDEQgFLAAAAAS', 'PHP_SELF': '/index.php', 'REQUEST_TIME_FLOAT': 1461619728.0705, 'REQUEST_TIME': 1461619728})
crawler_detect.isCrawler()
# true if crawler user agent detected
```
#### Output the name of the bot that matched (if any)
```Python
from crawlerdetect import CrawlerDetect
crawler_detect = CrawlerDetect()
crawler_detect.isCrawler('Mozilla/5.0 (compatible; Sosospider/2.0; +http://help.soso.com/webspider.htm)')
# true if crawler user agent detected
crawler_detect.getMatches()
# Sosospider
```

#### Get version of the library
```Python
from crawlerdetect import CrawlerDetect
crawler_detect = CrawlerDetect()
crawler_detect.version
```

### Contributing
If you find a bot/spider/crawler user agent that CrawlerDetect fails to detect, please submit a pull request with the regex pattern added to the array in `providers/crawlers.py` and add the failing user agent to `tests/crawlers.txt`.

Failing that, just create an issue with the user agent you have found, and we'll take it from there :)

### ES6 Library
To use this library with NodeJS or any ES6 application based, check out [es6-crawler-detect](https://github.com/JefferyHus/es6-crawler-detect).

### .NET Library
To use this library in a .net standard (including .net core) based project, check out [NetCrawlerDetect](https://github.com/gplumb/NetCrawlerDetect).

### Nette Extension
To use this library with the Nette framework, checkout [NetteCrawlerDetect](https://github.com/JanGalek/Crawler-Detect).

### Ruby Gem

To use this library with Ruby on Rails or any Ruby-based application, check out [crawler_detect](https://github.com/loadkpi/crawler_detect) gem.

_Parts of this class are based on the brilliant [MobileDetect](https://github.com/serbanghita/Mobile-Detect)_

[![Analytics](https://ga-beacon.appspot.com/UA-72430465-1/Crawler-Detect/readme?pixel)](https://github.com/JayBizzle/Crawler-Detect)
