#! /usr/bin/env python3
import sys
import glob
import re
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('getTop', type=int)
parser.add_argument('startTime')
parser.add_argument('endTime')
args = parser.parse_args()
startTime = datetime.datetime.strptime(args.startTime, '%Y-%m-%dT%H:%M:%S%z')
endTime = datetime.datetime.strptime(args.endTime, '%Y-%m-%dT%H:%M:%S%z')
getTop = args.getTop

ipDict = dict()

for filePath in glob.glob('./*.log'):
  with open(filePath, 'r') as fp:
    line = fp.readline()
    while line:
      strippedLine = line.strip()
      if strippedLine:
        match = re.search('^(?P<ip>.*?) (?P<remote_log_name>.*?) (?P<userid>.*?) \[(?P<time>.*? .*?)\] \"(?P<request_method>.*?) (?P<path>.*?) (?P<request_version>HTTP/.*?)?\" (?P<status>.*?) (?P<length>.*?) \"(?P<referrer>.*?)\" \"(?P<user_agent>.*?)\" \"(?P<origin_ip>.*?)\"$', strippedLine)
        if match:
          time = datetime.datetime.strptime(match.group('time'), '%d/%b/%Y:%H:%M:%S %z')
          if time > startTime and time < endTime:
            ip = match.group('ip')
            if ip in ipDict:
              ipDict[ip] = ipDict[ip] + 1
            else:
              ipDict[ip] = 1

      ####################
      line = fp.readline()

ordering = list(set(ipDict.values()))
ordering.sort(reverse=True)
enlistedCount = 0
for count in ordering:
  for ip in [key for (key, value) in ipDict.items() if value == count]:
    print('Host IP: %s, have made %d requests' % (ip, count))
    enlistedCount = enlistedCount + 1
  if enlistedCount >= getTop:
    break
