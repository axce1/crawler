# -*- coding: utf8 -*-

import sys
import urllib.request as urllib2

from copy import copy
from urllib.robotparser import RobotFileParser
from urllib.parse import urlunsplit, urlsplit


# config
TIMEOUT = 5
DEFAULT_HEADERS = {
    'Accept' : 'text/html, text/plain',
    'Accept-Charset' : 'windows-1251, koi8-r, UTF-8, iso-8859-1, US-ASCII',
    'Content-Language' : 'ru,en',
    }
DEFAULT_AGENTNAME = 'Test/1.0'
DEFAULT_EMAIL = 'admin@example.com'

class RobotsHTTPHandler(urllib2.HTTPHandler):

    def __init__(self, agentname, *args, **kwargs):
        urllib2.HTTPHandler.__init__(self, *args, **kwargs)
        self.agentname = agentname

    def http_open(self, request):
        url = request.get_full_url()
        host = urlsplit(url)[1]
        robots_url = urlunsplit(('http', host, '/robots.txt', '', ''))
        rp = RobotFileParser(robots_url)
        rp.read()
        if not rp.can_fetch(self.agentname, url):
            raise RuntimeError('Forbidden by robots.txt')
        return urllib2.HTTPHandler.http_open(self, request)

class UserAgent(object):

    def __init__(self, agentname=DEFAULT_AGENTNAME,
                 email=DEFAULT_EMAIL, new_headers={}):

        self.agentname = agentname
        self.email = email
        self.opener = urllib2.build_opener(
            RobotsHTTPHandler(self.agentname),)
        headers = copy(DEFAULT_HEADERS)
        headers.update(new_headers)
        opener_headers = [ (k,v) for k, v in headers.items() ]
        opener_headers.append(('User-Agent', self.agentname))
        if self.email:
            opener_headers.append(('From', self.email))
        self.opener.addheaders = opener_headers

    def open(self, url):
        return self.opener.open(url, None, TIMEOUT)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("Usage: python crawler.py URL")
        sys.exit(1)

    import socket

    ua = UserAgent()
    try:
        resp = ua.open(sys.argv[1])
    except RuntimeError as e:
        sys.stderr.write('Error: %s\n' % e)
        sys.exit(4)

    except urllib2.HTTPError as e:
        sys.stderr.write('Error: %s\n' % e)
        sys.stderr.write('Server error document:\n')
        sys.stderr.write(e.read())
        sys.exit(2)
    except urllib2.URLError as e:
        sys.stderr.write('Error: %s\n' % e)
        sys.exit(3)

    page = ''
    bytes_read = int()
    while 1:
        try:
            data = resp.read(1024).decode('utf8')
            page = page + data
        except socket.error as e:
            sys.stderr.write('Error reading data: %s' % e)
            sys.exit(5)

        if not len(data):
            break
        bytes_read += len(data)

    content_length = int(resp.info().get('Content-Length', 0))
    if content_length and (bytes_read != content_length):
        print ("Expected %d bytes, but read %d bytes" % \
                (content_length, bytes_read))
        sys.exit(6)

    sys.stdout.write(data)


