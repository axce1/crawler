#!/usr/bin/python3.3
from urllib.parse import urlunparse, urlsplit
from crawler import UserAgent
import logging
logging.basicConfig(
level=logging.DEBUG,
format='%(asctime)s %(levelname)-8s %(message)s',
datefmt='%Y-%m-%d %H:%M:%S',
filename='%s.log' % __name__,
filemode='w'
)

# имитируем браузер
AGENT_NAME = "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5"

def is_valid_link(u, hostname):
    """
    Фильтрация ссылок.
    """
    if u != 'javascript:void(0)':
        logging.debug("Validating link: '%s'" % u)
        url_parts = urlsplit(u)
        return False if url_parts.hostname != hostname \
            else False if url_parts[0] != 'http' \
            else True

def main(hostname):
    """
    Обход хоста с целью проверки на наличие мертвых ссылок.
    """
    def on_failure(url, error):
        """Вывод ошибки"""
        print ("%s: %s" % (url, error))

    ua = UserAgent(agentname=AGENT_NAME, ignore_robots=True)
    root = urlunparse(('http', hostname, '', '', '', ''))
    ua.traverse(
    root,
    links_filter=lambda u: is_valid_link(u, hostname),
    on_failure=on_failure)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print ('Usage: python deadlinks.py HOSTNAME')
        sys.exit(1)
    main(sys.argv[1])
