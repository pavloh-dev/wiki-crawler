import csv
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError


def parser(url, depth):
    if depth == 0:
        return None

    match = re.compile(r'(/wiki/)+()+')
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find("div", {"id": "bodyContent"}).find_all("a", href=match)

    print("Level ", depth, url)

    try:
        count = 0
        for link in links:
            try:
                if ':' not in link['href']:
                    count += 1
                    names = link['title']
                    parser("https://en.wikipedia.org" + link['href'], depth - 1)
                    f.writerow([count, names, link])

            except HTTPError as exception:
                if exception.code == 404:
                    print('404 Error. Exiting...')
                elif exception.code == 403:
                    print('Access Denied')
                else:
                    raise

    except KeyboardInterrupt:
        print('Exit execution...')
        raise SystemExit


def interface():
    while True:
        try:
            print('''Welcome to Wikipedia URL Crawler, please, choose operation:
                1. Search mode (crawl)
                2. Terminate (exit)
                ''')
            oper = int(input('Enter your choose: '))
            if oper == 1:
                url = input('Enter Wiki URL or string: ')
                steps = int(input('Enter depth of search (default 3): '))
                regex = re.compile(r'/^https:\/\/en\.wikipedia\.org(\/(wiki)\/?(\?.*)?)?$/')
                if url == regex:
                    parser(url, steps)
                else:
                    # wiki_start = 'https://en.wikipedia.org/wiki/'.join(url)
                    parser(url, steps)
                break
            if oper == 2:
                return SystemExit
            assert KeyboardInterrupt
        except ValueError or KeyboardInterrupt:
            print("Invalid Data... try again")
            return SystemExit


# initialize function using call from interface -> parser
if __name__ == '__main__':
    # print output to .csv in row as raw data (could be some out of bounds in indexing rows numbers)
    f = csv.writer(open('../test.csv', 'w'))
    f.writerow(['#', 'Title', 'Link'])
    interface()
