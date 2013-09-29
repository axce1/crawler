# -*- coding utf8 -*-

import sys
import os
import unittest
from urllib.parse import urlsplit

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
            #'http://nashgorod.ru/forum/',
            #'http://python.org/',
            #'http://lxml.de/index.html',
            #'http://gajim.org/',
            #'http://tv.yandex.ru',
            'http://example.com',
            #'http://r-bis.com/id/',
            )

    def test_alllinks(self):
        links = []
        for page_url in self.urls:
            fileobj = self.user_agent.open(page_url)
            links.extend([ u for u in links_iterator(fileobj)])
        self.assertTrue(links, 'No links from %d pages' % len(self.urls))

    def test_inbound_links(self):
        inbound = []
        for page_url in self.urls:
            hostname = urlsplit(page_url).hostname
            fileobj = self.user_agent.open(page_url)

            def is_inbound(u):
                h = urlsplit(u)[1]
                return h == hostname

            links = [ u for u in links_iterator(fileobj, is_inbound)]
            inbound.extend(
                [ u for u in links if urlsplit(u).hostname != hostname])
            for link in links:
                print (link)

        self.assertFalse(inbound, 'Unexpected outbound links: %s' % inbound)

    def test_outbound_links(self):

        outbound = []
        for page_url in self.urls:
            hostname = urlsplit(page_url).hostname
            fileobj = self.user_agent.open(page_url)

            def is_outbound(u):
                h = urlsplit(u).hostname
                return h != hostname

            links = [ u for u in links_iterator(fileobj, is_outbound) ]
            outbound.extend(
                [ u for u in links if urlsplit(u).hostname == hostname])
            for link in links:
                print (link)

        self.assertFalse(outbound, 'Unexpected inbound links: %s' % outbound)

    def test_traverse(self):

        #page_url = 'http://pi-code.blogspot.com'
        page_url = 'http://example.com'
        hostname = urlsplit(page_url).hostname

        def is_valid_link(u):
            url_parts = urlsplit(u)
            return False if url_parts.hostname == hostname \
                    else False if url_parts[0] != 'http' \
                    else True

        passed = []
        errors = []

        def on_success(url, response):
            passed.append(url)

        def on_failure(url, error):
            errors.append(url)

        self.user_agent.traverse(
            page_url,
            links_filter=is_valid_link,
            on_success=on_success,
            on_failure=on_failure)

        self.assertTrue(len(passed) > 1 , 'No nodes were passed')

    def test_blogspot(self):
        page_url = 'http://krushinsky.blogspot.com/'
        fileobj = self.user_agent.open(page_url)
        test_link = 'http://krushinsky.blogspot.com/2007_12_01_archive.html'
        links = [ u for u in links_iterator(fileobj, lambda u: u == test_link) ]
        print (links)
        self.assertTrue(len(links), "Link '%s' is absent" % test_link)


if __name__ == '__main__':
    module = __import__(__name__)
    suite = unittest.TestLoader().loadTestsFromModule(module)
    unittest.TextTestRunner(verbosity=2).run(suite)
