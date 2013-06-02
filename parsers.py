# -*- coding utf8 -*-

import urllib2
import lxml.html

def links_iterator(response, link_filter=None):
    if not link_filter:
        link_filter = lambda x: True

    doc = lxml.html.fromstring(response.read())

    for u in doc.xpath('//a/@href'): # select the url in href for all a tags(links)
        if link_filter(u):
            yield u
