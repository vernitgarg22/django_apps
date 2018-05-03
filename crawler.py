#!/usr/bin/env python

from datetime import datetime
import re
import requests
import sys


import pdb


class Urls():

    def __init__(self, domain, content):
        self.domain = domain
        self.content = content

    def __iter__(self):
        return self

    def __next__(self):
        """
        Return next url in the page, if any.
        """

        begin = re.search('href=[\'\"]', self.content)
        if not begin:
            raise StopIteration

        self.content = self.content[begin.end() : ]
        end = re.search('[\'\"]', self.content)
        if not end:
            raise StopIteration

        url = self.content[ : end.start()]
        return 'http://' + self.domain + url if url.startswith('/') else url


class PageCrawler():

    def __init__(self, domain, url):

        self.domain = domain
        self.url = url

    def urls(self):

        response = requests.get(self.url)
        if response.status_code != 200:
            # print("url {} - {}".format(url, response.status_code))
            return []

        return Urls(domain=self.domain, content=response.text)


def ignore_url(url):
    """
    Returns True if we should ignore the url.
    """

    url = url.lower()

    # Verify valid protocol (e.g., avoid "tel:", "mailto:")
    valid_protocols = [
        "http:",
        "https:",
    ]

    protocol_ok = False
    for protocol in valid_protocols:

        if url.startswith(protocol):
            protocol_ok = True

    if not protocol_ok:
        return True

    # Make sure file type (if any) is one we are interested in
    pos = url.find('?')
    if pos > 0:
        url = url[ : pos]

    ignored_endings = [
        ".css",
        "/css",
        ".ico",
        ".png",
        ".jpg",
        "pdf",
    ]

    for ignore in ignored_endings:

        if url.endswith(ignore):
            return True

    # Make sure path is one we are interested in
    ignored_paths = [
        "/search-results?",
        "/calendar-and-events/",
        "/calendar-events/",
        "/cablecastpublicsite/",
        "/dnngo_xblog/",
        "/portals/0/docs/",
        "/bundles/styles/",
        "/news/",
        "codstaging.detroitmi.gov",
        "data.detroitmi.gov",
        "dev.socrata.com",
        "github.com",
        "goo.gl/",
        "govdelivery.com",
        "/home-old/",
    ]

    for ignore in ignored_paths:

        if ignore in url:
            return True

    return False


class PageCrawlerAdmin():

    MAX_LEVELS_DEEP = 250

    def __init__(self):

        self.urls_crawled = set()
        self.levels_deep = 0

    def crawl_page(self, domain, url):

        crawler = PageCrawler(domain=domain, url=url)

        if self.levels_deep == self.MAX_LEVELS_DEEP:
            print("Too many levels deep")
            return

        self.levels_deep = self.levels_deep + 1

        for url in crawler.urls():

            if not ignore_url(url) and url not in self.urls_crawled:

                self.urls_crawled.add(url)

                if len(self.urls_crawled) % 100 == 0:
                    print("crawled {} urls - {}".format(len(self.urls_crawled), datetime.now()))
                    sys.stdout.flush()

                print("level: {} - url: {}".format(self.levels_deep, url), file=sys.stderr)

                # If this on our server then crawl it.
                if domain in url:

                    self.crawl_page(domain=domain, url=url)

        self.levels_deep = self.levels_deep - 1

    def get_urls_crawled(self):

        return self.urls_crawled


if __name__ == '__main__':

    domain = "detroitmi.gov"
    site = "http://" + domain

    admin = PageCrawlerAdmin()

    # Start crawling the site.
    try:
        admin.crawl_page(domain=domain, url=site)
    except RecursionError:
        print("Caught RecursionError")
    except:
        print("Caught Unknown Error")

    urls_crawled = admin.get_urls_crawled()

    for url in sorted(list(urls_crawled)):

        print(url)
