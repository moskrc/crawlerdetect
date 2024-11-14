#!/bin/bash

VERSION="master"

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
datafile "https://raw.githubusercontent.com/JayBizzle/Crawler-Detect/${VERSION}/raw/Crawlers.txt" "crawlerdetect/providers/crawlers.py"

echo "Updating exclusions"
datafile "https://raw.githubusercontent.com/JayBizzle/Crawler-Detect/${VERSION}/raw/Exclusions.txt" "crawlerdetect/providers/exclusions.py"

echo "Updating headers"
datafile "https://raw.githubusercontent.com/JayBizzle/Crawler-Detect/${VERSION}/raw/Headers.txt" "crawlerdetect/providers/headers.py"

echo "Patching files"
#sed -i "" -e 's/`Yandex(?!Search)`/`Yandex`/' crawlerdetect/providers/crawlers.py
sed -i "" -e 's/r""\([^"]*\)""/r"\\\"\1\\\""/' crawlerdetect/providers/exclusions.py

echo "Updating tests/data/user_agent/crawlers.txt"
curl --progress-bar -o tests/fixtures/user_agent/crawlers.txt https://raw.githubusercontent.com/JayBizzle/Crawler-Detect/${VERSION}/tests/data/user_agent/crawlers.txt

echo "Updating tests/data/user_agent/devices.txt"
curl --progress-bar -o tests/fixtures/user_agent/devices.txt https://raw.githubusercontent.com/JayBizzle/Crawler-Detect/${VERSION}/tests/data/user_agent/devices.txt

echo "Updating tests/data/sec_ch_ua/crawlers.txt"
curl --progress-bar -o tests/fixtures/sec_ch_ua/crawlers.txt https://raw.githubusercontent.com/JayBizzle/Crawler-Detect/${VERSION}/tests/data/sec_ch_ua/crawlers.txt

echo "Updating tests/data/sec_ch_ua/devices.txt"
curl --progress-bar -o tests/fixtures/sec_ch_ua/devices.txt https://raw.githubusercontent.com/JayBizzle/Crawler-Detect/${VERSION}/tests/data/sec_ch_ua/devices.txt

echo "Updating completed"
