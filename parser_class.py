import random
import re
import csv
import threading
import time

import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup
from typing import List, Optional, Union
from urllib.error import HTTPError


class ParserThread(threading.Thread):
    """
    A threading example
    """

    def __init__(self, name):
        """ Init """
        ParserThread.__init__(self)
        super().__init__(name)
        self.name = name

    def run(self):
        """Launch threads"""
        amount = random.randint(3, 15)
        time.sleep(amount)
        msg = "%s is running" % self.name
        print(msg)


def create_threads():
    """
    Creating Threads
    """
    for i in range(5):
        name = "Thread #%s" % (i + 1)
        my_thread = ParserThread(name)
        my_thread.start()


class WiKiLink(ParserThread):
    """Class to represent wiki link with title and level
    """

    def __init__(self, level: int, title: str, link: str) -> None:
        self.level = level
        self.title = title
        self.link = link

    @classmethod
    def from_bs_element(cls, element, level: int) -> WiKiLink:
        title = element["title"]
        link = element["href"]

        return cls(level, title, link)

    @staticmethod
    def from_bs_result_set(links: bs4.element.ResultSet) -> List:
        return list(map(self.from_bs_element, links))

    def __hash__(self):
        hashable_items = (self.level, self.title, self.link)
        return hash(hashable_items)


class WikiParser(ParserThread):
    """
    Class to parse wiki pages with some depth
    """

    WIKI_LINKS_RE = re.compile(r'(/wiki/)+()+')
    HTTP_REQUEST_TIMEOUT = 50
    UNUSEFUL_LINKS_FILTER_FUNCTIONS = [
        lambda link: ':' not in link["href"],
    ]

    def __init__(self, start_url: str, depth: Optional[int] = 3) -> None:
        """Initial state of parser
        """

        self.start_url = start_url
        self.depth = depth

    def get_page_html(self, url: str) -> str:
        """Get HTML (in str) from url
        """
        with urlopen(url, timeout=self.HTTP_REQUEST_TIMEOUT) as response:
            html: str = response.read()

        return html

    def get_wiki_links_from_url(self, url: str) -> bs4.element.ResultSet:
        """Automatically get HTML from URL  and all links for wiki pages
        """
        page_html = self.get_page_html(url)
        soup = BeautifulSoup(page_html, 'html.parser')
        links = soup.find("div", {"id": "bodyContent"}).find_all("a", href=self.WIKI_LINKS_RE)

        return links

    def filter_links(self, links: Union[List, bs4.element.ResultSet]) -> List:
        filtered_links = links

        for filter_function in self.UNUSEFUL_LINKS_FILTER_FUNCTIONS:
            filtered_links = filter(filter_function, filtered_links)

        return list(filtered_links)

    def parse_links(self, url: Optional[str] = None, current_depth: Optional[int] = None):
        if current_depth is None:
            current_depth = self.depth
        elif current_depth <= 0:
            return []

        if url is None:
            url = self.start_url

        all_links = self.get_wiki_links_from_url(url)
        wiki_links = self.filter_links(all_links)

        # ..........................................

        for wiki_link in wiki_links:
            wiki_url = "https://en.wikipedia.org" + wiki_link['href']
            included_wiki_links = self.parse_links(wiki_url, current_depth - 1)
            wiki_links.insert(included_wiki_links)

        return wiki_links


if __name__ == "__main__":
    parser = WikiParser("https://en.wikipedia.org/wiki/Google_Talk")
    create_threads()
    print(parser.parse_links())
