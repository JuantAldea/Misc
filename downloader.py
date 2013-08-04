# Copyright (C) 2013, Juan Antonio Aldea Armenteros
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf8 -*-

#!/usr/bin/python

import threading
import urllib2
import math

def download(url, header, part):
    f = open("part" + str(part), "w")
    print "Range:" + header["Range"]
    request = urllib2.Request(url, headers=header)
    f.write(urllib2.urlopen(request).read())
    print "Part " + str(part) + "finished!"


url = "http://..."
size = 1610612755
threads = []
parts = 20
part = int(math.ceil(size / float(parts)))
start = 0

for i in range(parts):
    start = i * part
    end = min(size, 1 + (i + 1) * part)
    start += 0 if i == 0 else 2
    print start, end, end - start + 1
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": "__utma=163708862.1708841052.1370652629.1370661253.1370663510.4; __utmz=163708862.1370652629.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=163708862; __utmb=163708862.1.10.1370663510",
        "Connection": "keep-alive",
        "Range": "bytes=" + str(start) + "-" + str(end)
    }
    
    threads.append(threading.Thread(target=download, args=(url, header, i)))

for i in range(parts):
    threads[i].start()

for i in range(parts):
    threads[i].join()

