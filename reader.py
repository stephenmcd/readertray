#!/usr/bin/env python

import time, urllib
from threading import Thread
from lib import html


class Reader(Thread):
    """threaded rss checker"""

    def __init__(self, **kwargs):

        self.feeds = {}
        self.interval = 120
        self.running = True
        self.__dict__.update(kwargs)
        self.read = []
        self.unread = []
        Thread.__init__(self)
        self.start()

    def run(self):

        strip = lambda x: html.strip(x.string)
        self._last = 0
        while self.running:
            now = time.time()
            if now > self._last + self.interval:
                self._last = now
                for feed in self.feeds:
                    try:
                        data = urllib.urlopen(feed).read()
                        items = html.parse(data)("item")
                        #items = html.parse(items)("entry")
                        title = html.parse(data)("channel")[0]("title")[0]
                    except Exception, err:
                        print err
                    else:
                        for item in items:
                            if item.title.string not in [read["title"] for read in self.read]:
                                self.unread.append({
                                    "feed": strip(title),
                                    "title": strip(item.title),
                                    "url": html.strip(item.link.nextSibling),
                                    "description": strip(item.description)
                                })
            time.sleep(0.1)

    def items(self):

        while self.unread:
            self.read.append(self.unread.pop(0))
            yield self.read[-1]

    def close(self):

        self.running = False
        self.join()

if __name__ == "__main__":
    reader = Reader(interval=30, feeds=["http://rss.slashdot.org/Slashdot/slashdot"])
    while True:
        for item in reader.items():
            print item
        time.sleep(0.1)
    reader.close()

