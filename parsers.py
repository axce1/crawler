# -*- coding utf8 -*-

import lxml.html
from urlparse import urlsplit, urljoin

def links_iterator(response, link_filter=None):
    if not link_filter:
        link_filter = lambda x: True

    base = response.geturl()
    doc = lxml.html.fromstring(response.read())

    for u in doc.xpath('//a/@href'): # select the url in href for all a tags(links)
        if urlsplit(u).hostname != None:
            pass
        else:
            u = urljoin(base, u)
        if link_filter(u):
            yield u
