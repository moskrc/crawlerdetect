[![test](https://github.com/moskrc/crawlerdetect/actions/workflows/python-package.yml/badge.svg)](https://github.com/moskrc/crawlerdetect/actions/workflows/python-package.yml)

# About CrawlerDetect

This is a Python wrapper for [CrawlerDetect](https://github.com/JayBizzle/Crawler-Detect) a web crawler detection library. It helps identify
bots, crawlers, and spiders using the user agent and other HTTP headers.

> Currently synced with [JayBizzle/Crawler-Detect `v1.4.1`](https://github.com/JayBizzle/Crawler-Detect/releases/tag/v1.4.1) - 1462 crawler patterns.

# How to install
```bash
$ pip install crawlerdetect
```

# How to use

## Method Reference
| camelCase | snake_case | Description                       |
|-----------|------------|-----------------------------------|
| `isCrawler()` | `is_crawler()` | Check if user agent is a crawler  |
| `getMatches()` | `get_matches()` | Get the name of detected crawlers |

## Variant 1
```Python
from crawlerdetect import CrawlerDetect
crawler_detect = CrawlerDetect()
crawler_detect.isCrawler('Mozilla/5.0 (compatible; Sosospider/2.0; +http://help.soso.com/webspider.htm)')
# true if crawler user agent detected
```

## Variant 2
```Python
from crawlerdetect import CrawlerDetect
crawler_detect = CrawlerDetect(user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit (KHTML, like Gecko) Mobile (compatible; Yahoo Ad monitoring; https://help.yahoo.com/kb/yahoo-ad-monitoring-SLN24857.html)')
crawler_detect.isCrawler()
# true if crawler user agent detected
```

## Variant 3
```Python
from crawlerdetect import CrawlerDetect
crawler_detect = CrawlerDetect(headers={'DOCUMENT_ROOT': '/home/test/public_html', 'GATEWAY_INTERFACE': 'CGI/1.1', 'HTTP_ACCEPT': '*/*', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate', 'HTTP_CACHE_CONTROL': 'no-cache', 'HTTP_CONNECTION': 'Keep-Alive', 'HTTP_FROM': 'googlebot(at)googlebot.com', 'HTTP_HOST': 'www.test.com', 'HTTP_PRAGMA': 'no-cache', 'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36', 'PATH': '/bin:/usr/bin', 'QUERY_STRING': 'order=closingDate', 'REDIRECT_STATUS': '200', 'REMOTE_ADDR': '127.0.0.1', 'REMOTE_PORT': '3360', 'REQUEST_METHOD': 'GET', 'REQUEST_URI': '/?test=testing', 'SCRIPT_FILENAME': '/home/test/public_html/index.php', 'SCRIPT_NAME': '/index.php', 'SERVER_ADDR': '127.0.0.1', 'SERVER_ADMIN': 'webmaster@test.com', 'SERVER_NAME': 'www.test.com', 'SERVER_PORT': '80', 'SERVER_PROTOCOL': 'HTTP/1.1', 'SERVER_SIGNATURE': '', 'SERVER_SOFTWARE': 'Apache', 'UNIQUE_ID': 'Vx6MENRxerBUSDEQgFLAAAAAS', 'PHP_SELF': '/index.php', 'REQUEST_TIME_FLOAT': 1461619728.0705, 'REQUEST_TIME': 1461619728})
crawler_detect.isCrawler()
# true if crawler user agent detected
```
## Output the name of the bot that matched (if any)
```Python
from crawlerdetect import CrawlerDetect
crawler_detect = CrawlerDetect()
crawler_detect.isCrawler('Mozilla/5.0 (compatible; Sosospider/2.0; +http://help.soso.com/webspider.htm)')
# true if crawler user agent detected
crawler_detect.getMatches()
# Sosospider
```

## Get version of the library
```Python
import crawlerdetect
crawlerdetect.__version__
```

# Contributing

The patterns and testcases are synced from the PHP repo. If you find a bot/spider/crawler user agent that crawlerdetect fails to detect, please submit a pull request with the regex pattern and a testcase to the [upstream PHP repo](https://github.com/JayBizzle/Crawler-Detect).

Failing that, just create an issue with the user agent you have found, and we'll take it from there :)

# Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and packaging.

## Setup
```bash
$ uv sync
```

## Running tests
```bash
$ uv run pytest
```

## Update crawlers from upstream PHP repo
```bash
$ ./update_data.sh
```

## Bump version
Bumping updates the version in `pyproject.toml` and `crawlerdetect/__init__.py`, commits the change, and creates a matching `vX.Y.Z` git tag.

Pass the part to increment:
```bash
# 0.4.1 -> 0.4.2
$ uv run bump-my-version bump patch

# 0.4.1 -> 0.5.0
$ uv run bump-my-version bump minor

# 0.4.1 -> 1.0.0
$ uv run bump-my-version bump major
```

Or set an explicit version instead of incrementing a part:
```bash
$ uv run bump-my-version bump --new-version 0.4.1
```

Preview the change first with `--dry-run -v` (nothing is written or committed):
```bash
$ uv run bump-my-version bump --dry-run -v patch
```

`bump-my-version bump` on its own (no part, no `--new-version`) fails with `Unable to get the next version.` - one of the two is required.

You may also see a harmless warning:
```
Specified version (0.3.3) does not match last tagged version (0.3.2)
```
This just means the version in `pyproject.toml` and the latest `vX.Y.Z` git tag are out of sync (e.g. after a manual version edit) - bump-my-version still uses `pyproject.toml` as the source of truth and bumps correctly regardless.

`bump-my-version` doesn't know about `uv.lock` by default, which used to leave the project's own version there stale and break CI's `uv sync --locked`. A `pre_commit_hooks` entry in `pyproject.toml` (`uv lock`, `git add uv.lock`) now refreshes and stages it automatically, so it's included in the same bump commit — no manual step needed.

Once bumped, push the commit and tag, then [publish to PyPI](#how-to-publish-a-new-release-to-pypi):
```bash
$ git push && git push --tags
```

## How to publish a new release to PyPI
```bash
$ uv build
$ uv publish
```
`uv publish` needs a PyPI token, provided via `UV_PUBLISH_TOKEN` (or `--token`):
```bash
$ UV_PUBLISH_TOKEN=pypi-... uv publish
```
