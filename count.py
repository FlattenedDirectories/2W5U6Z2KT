#! /usr/bin/env python3
import sys
import glob
import re

count = 0
for filePath in glob.glob('./*.log'):
  with open(filePath, 'r') as fp:
    line = fp.readline()
    while line:
      strippedLine = line.strip()
      if strippedLine:
        match = re.search('^(?P<ip>.*?) (?P<remote_log_name>.*?) (?P<userid>.*?) \[(?P<time>.*? .*?)\] \"(?P<request_method>.*?) (?P<path>.*?) (?P<request_version>HTTP/.*?)?\" (?P<status>.*?) (?P<length>.*?) \"(?P<referrer>.*?)\" \"(?P<user_agent>.*?)\" \"(?P<origin_ip>.*?)\"$', strippedLine)
        if match:
          count = count + 1

      ####################
      line = fp.readline()

print('Total count: %d' % count)
