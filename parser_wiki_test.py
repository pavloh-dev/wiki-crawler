import csv
import os
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import pandas as pd


def parser(url, depth, destination):

    if depth == 0:
        return None
    match = re.compile(r'(/wiki/)+()+')
    html = urlopen(url, timeout=50)
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find("div", {"id": "bodyContent"}).find_all("a", href=match)

    print("Level ", depth, url)

    try:

        for link in links:

            try:

                if ':' not in link['href']:
                    names = link['title']

                    f.writerow([depth, names, 'URL Location: ' + f'{wiki}' + link['href']])

                    # url = link.get('href').strip()
                    if link['href'] == destination or url.startswith('/wiki/') == destination:
                        print(f'You are looking for {destination[6:]}')
                        print(f'found shortest way to url {wiki + link["href"]} \nSteps made: {len(link["href"])}')

                        def filter_data():
                            df = pd.read_csv(files)
                            df.drop_duplicates(inplace=True)
                            df.sort_index(axis=0)
                            df.to_csv('sorted_data.csv', index=True, index_label='#')
                            if os.path.isfile('sample_data.csv') or os.path.exists('sample_data.csv'):
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


def interface():

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
                destination = "".join(["/wiki/", input("Enter keywords:")])
                print(destination)
                regex = re.compile(r'/^https:\/\/en\.wikipedia\.org(\/(wiki)\/?(\?.*)?)?$/')
                if url == regex:
                    parser(url, steps, destination)
                else:
                    # wiki_start = 'https://en.wikipedia.org/wiki/'.join(url)
                    parser(url, steps, destination)
                break
            if choose_case == 2:
                return SystemExit
        except ValueError or KeyboardInterrupt:
            print("Invalid Data... try again")
            return SystemExit


# initialize function using call from interface -> parser
if __name__ == '__main__':

    try:
        wiki = "https://en.wikipedia.org"
        # https://en.wikipedia.org/wiki/Node.js look for example COBOL
        # print output to .csv in row as raw data (could be some out of bounds in indexing rows numbers)
        file = 'sample_data.csv'
        files = './sample_data.csv'
        f = csv.writer(open(file, 'w'))
        f.writerow(['level', 'title', 'link'])
        interface()

    except KeyboardInterrupt or ValueError or IOError:
        assert SystemExit
