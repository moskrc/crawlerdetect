#!/bin/bash
set -euo pipefail

REPO="JayBizzle/Crawler-Detect"

# Works with both GNU sed (Linux) and BSD sed (macOS), which disagree on
# how `-i` takes its backup-suffix argument.
sed_inplace() {
	if sed --version >/dev/null 2>&1; then
		sed -i "$@"
	else
		sed -i '' "$@"
	fi
}

VERSION=$(curl -s "https://api.github.com/repos/${REPO}/releases/latest" | grep -m1 '"tag_name"' | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+')
if [ -z "${VERSION}" ]; then
	echo "Failed to determine latest ${REPO} release" >&2
	exit 1
fi
echo "Syncing with ${REPO} release ${VERSION}"

datafile(){
	url="$1"
	name="$2"

curl --progress-bar "$url" | awk -v name="$name" -v url="$url" '
BEGIN{
    printf("data = [\n")
}
{
    printf("    r\"%s\",\n", $0)
}
END{
    printf("]\n")
}' > "${name}"
}
echo "Updating crawlers"
datafile "https://raw.githubusercontent.com/${REPO}/${VERSION}/raw/Crawlers.txt" "crawlerdetect/providers/crawlers.py"

echo "Updating exclusions"
datafile "https://raw.githubusercontent.com/${REPO}/${VERSION}/raw/Exclusions.txt" "crawlerdetect/providers/exclusions.py"

echo "Updating headers"
datafile "https://raw.githubusercontent.com/${REPO}/${VERSION}/raw/Headers.txt" "crawlerdetect/providers/headers.py"

echo "Patching files"
#sed_inplace -e 's/`Yandex(?!Search)`/`Yandex`/' crawlerdetect/providers/crawlers.py
sed_inplace -e 's/r""\([^"]*\)""/r"\\\"\1\\\""/' crawlerdetect/providers/exclusions.py

echo "Updating tests/data/user_agent/crawlers.txt"
curl --progress-bar -o tests/fixtures/user_agent/crawlers.txt "https://raw.githubusercontent.com/${REPO}/${VERSION}/tests/data/user_agent/crawlers.txt"

echo "Updating tests/data/user_agent/devices.txt"
curl --progress-bar -o tests/fixtures/user_agent/devices.txt "https://raw.githubusercontent.com/${REPO}/${VERSION}/tests/data/user_agent/devices.txt"

echo "Updating tests/data/sec_ch_ua/crawlers.txt"
curl --progress-bar -o tests/fixtures/sec_ch_ua/crawlers.txt "https://raw.githubusercontent.com/${REPO}/${VERSION}/tests/data/sec_ch_ua/crawlers.txt"

echo "Updating tests/data/sec_ch_ua/devices.txt"
curl --progress-bar -o tests/fixtures/sec_ch_ua/devices.txt "https://raw.githubusercontent.com/${REPO}/${VERSION}/tests/data/sec_ch_ua/devices.txt"

echo "Updating README upstream version"
PATTERN_COUNT=$(grep -c '^    r"' crawlerdetect/providers/crawlers.py)
sed_inplace -E "s#^> Currently synced with .*#> Currently synced with [${REPO} \`${VERSION}\`](https://github.com/${REPO}/releases/tag/${VERSION}) — ${PATTERN_COUNT} crawler patterns.#" README.md

echo "Updating completed (upstream release ${VERSION})"
