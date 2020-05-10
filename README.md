# Access log analytics

## Assumptions

1. Log files will be named in format `*.log`
2. Log file will sit aside with `*.py`
3. Lines like `185.209.0.12 - - [19/May/2019:13:51:11 +0800] "\x03\x00\x00/*\xE0\x00\x00\x00\x00\x00Cookie: mstshash=Administr" 400 157 "-" "-" "-"` is not considered as valid, which will not be counted
4. Timezone is HKT (GMT +8)
5. Any host count is having same count with the last candidate will still be shown, so there may be more candidate shown compared to given condition.

## Usage
```sh
#Q1
./count.py

#Q2
./hosts.py 10 "2019-06-10T00:00:00+08:00" "2019-06-19T23:59:59+08:00"

#Q3 
./country.py
#Might need API access key if needing new queries on geolocation info outside the cache file, see https://ipstack.com/
IPSTACKACCESSKEY=xxxxxxxxxxxxxxxxxxx ./country.py
```
