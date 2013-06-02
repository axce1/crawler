# -*- coding utf8 -*-

import sys
import os
import unittest
from urlparse import urlsplit

import crawler
from parsers import links_iterator

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(parent_dir, 'src')
sys.path.append(src_dir)

class TestUserAgent(unittest.TestCase):

    def setUp(self):

        self.crawler = crawler.UserAgent()


    def tearDown(self):
        pass


    def test_default_agentname(self):

        msg = "Default agent name should be '%s', not '%s'" % \
                (crawler.DEFAULT_AGENTNAME, self.crawler.agentname)
        self.assertEqual(self.crawler.agentname, crawler.DEFAULT_AGENTNAME, msg)


    def test_custom_agentname(self):

        name = 'Other Test/2.0'
        c = crawler.UserAgent(agentname=name)
        self.assertEqual(c.agentname, name, \
            "Custom agent name should be '%s', not '%s'" % \
            (name, c.agentname))


    def test_htmlget(self):

        resp = self.crawler.open('http://spintongues.msk.ru/kafka2.html')
        ctype = resp.info().get('Content-Type')
        self.assert_(ctype.find('text/html') != -1, 'Not text/html')


    def test_urlerror(self):

        self.assertRaises(IOError, self.crawler.open, 'http://foo/bar/buz/q231')


    def test_robotrules(self):

        self.assertRaises(RuntimeError, self.crawler.open, 'http://yandex.ru')


class TestLinks(unittest.TestCase):

    def setUp(self):
        self.user_agent = crawler.UserAgent()
        self.urls = (
            'http://www.google.com/',
            'http://python.org/',
            'http://lxml.de/index.html',
            'http://gajim.org/',
            'http://tv.yandex.ru'
            )


    def test_alllinks(self):

        links = []
        for page_url in self.urls:
            fileobj = self.user_agent.open(page_url)
            links.extend([ u for u in links_iterator(fileobj)])
        self.assertTrue(links, 'No links from %d pages' % len(self.urls))


if __name__ == '__main__':
    module = __import__(__name__)
    suite = unittest.TestLoader().loadTestsFromModule(module)
    unittest.TextTestRunner(verbosity=2).run(suite)

