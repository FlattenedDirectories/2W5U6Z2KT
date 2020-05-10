#! /usr/bin/env python3
import sys
import os
import glob
import re
import json
import urllib.request

ipstackAccesskey = os.getenv('IPSTACKACCESSKEY')

cache = dict()
cacheFp = open('./data/ip_country_cache.tsv', 'r')
contents = cacheFp.read()
for line in contents.strip().split('\n'):
  split = line.split('\t')
  cache[split[0]] = split[1]
cacheFp.close()
cacheFp = open('./data/ip_country_cache.tsv', 'a')

def writeCache(ip, country_name):
  cacheFp.write('%s\t%s\n' % (ip, country_name))
  cacheFp.flush()

def getCacheIfExists(ip):
  if ip in cache:
    return cache[ip]
  else:
    print('%s not found in cache, querying from ipstack' % ip)
    if not ipstackAccesskey:
      print("ipstack access key not found, quitting.")
      exit()
    contents = urllib.request.urlopen('http://api.ipstack.com/%s?access_key=%s' % (ip, ipstackAccesskey)).read()
    jsonContents = json.loads(contents)
    cache[ip] = jsonContents['country_name']
    writeCache(ip, jsonContents['country_name'])
    return jsonContents['country_name']

ipDict = dict()
countryDict = dict()

for filePath in glob.glob('./*.log'):
  with open(filePath, 'r') as fp:
    line = fp.readline()
    while line:
      strippedLine = line.strip()
      if strippedLine:
        match = re.search('^(?P<ip>.*?) (?P<remote_log_name>.*?) (?P<userid>.*?) \[(?P<time>.*? .*?)\] \"(?P<request_method>.*?) (?P<path>.*?) (?P<request_version>HTTP/.*?)?\" (?P<status>.*?) (?P<length>.*?) \"(?P<referrer>.*?)\" \"(?P<user_agent>.*?)\" \"(?P<origin_ip>.*?)\"$', strippedLine)
        if match:
          ip = match.group('ip')
          if ip in ipDict:
            ipDict[ip] = ipDict[ip] + 1
          else:
            ipDict[ip] = 1

      ####################
      line = fp.readline()

for ip in ipDict:
  country_name = getCacheIfExists(ip)
  if country_name in countryDict:
    countryDict[country_name] = countryDict[country_name] + ipDict[ip]
  else:
    countryDict[country_name] = ipDict[ip]

max = max(countryDict.values())
for country_name in countryDict:
  if countryDict[country_name] == max:
    print('%s: having total of %d requests' % (country_name, max))
