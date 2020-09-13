import csv
import functools
import os
import re
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import pandas as pd


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer()


def parser(url: str, depth: int, destination: str):
    if depth == 0:
        return None
    match = re.compile(r'(/wiki/)+()+')
    html = urlopen(url, timeout=50)
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find("div", {"id": "bodyContent"}).find_all("a", href=match)

    def crawler():
        return print("Level ", depth, url)

    try:
        crawler()
        for link in links:

            try:

                if ':' not in link['href']:
                    names = link['title']

                    f.writerow([depth, names, 'URL Location: ' + f'{wiki}' + link['href']])

                    if link['href'] == destination or url.startswith('/wiki/') == destination:
                        print(f'You are looking for {destination[6:]}')
                        print(f'found shortest way to url {wiki + link["href"]} \nSteps made: {len(link["href"])} \nRecord # in sample_data.csv is {len(links)}')

                        @timer
                        def filter_data():
                            df = pd.read_csv(files)
                            df.drop_duplicates(inplace=True)
                            df.sort_index(axis=0)
                            df.to_csv('sorted_data.csv', index=True, index_label='#')
                            if os.path.isfile('sample_data.csv') | os.path.exists('sample_data.csv'):
                                exit()

                        return filter_data()
                    else:
                        parser(wiki + link['href'], depth - 1, destination)

            except HTTPError as exception:
                if exception.code == 404:
                    print('404 Error. Exiting...')
                else:
                    raise

    except KeyboardInterrupt:
        print('Exit execution...')
        raise SystemExit


def interface() -> None:
    while True:
        try:
            print('''Welcome to Wikipedia URL Crawler, please, choose operation:
                1. Search
                2. Terminate (exit)
                ''')
            choose_case = int(input('Enter your choose: '))
            if choose_case == 1:

                url = input('Enter Wiki URL or string: ')
                steps = int(input('Enter depth of search (default 3): '))
                destination = "".join(["/wiki/", input("Enter keywords: ")])

                regex = re.compile(r'/^https:\/\/en\.wikipedia\.org(\/(wiki)\/?(\?.*)?)?$/')
                if url == regex:
                    parser(url, steps, destination)
                else:
                    parser(url, steps, destination)
                break
            if choose_case == 2:
                assert SystemExit
        except (ValueError, KeyboardInterrupt):
            print("Invalid Data... try again")
            assert SystemExit


if __name__ == '__main__':
    try:
        wiki = "https://en.wikipedia.org"

        '''
        LINK EXAMPLE: https://en.wikipedia.org/wiki/Node.js look for example COBOL
        print output to .csv in row as raw data (could be some out of bounds in indexing rows numbers)
        '''

        file = 'sample_data.csv'
        files = './sample_data.csv'
        subset = open(file, 'w')
        f = csv.writer(subset)
        f.writerow(['level', 'title', 'link'])
        interface()
        subset.close()

    except (KeyboardInterrupt, ValueError, IOError):
        assert SystemExit
