import requests
import sys

from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

class Downloader(object):

    def __init__(self, url):
        if not url.startswith('http'):
            url = 'http://' + url
        self.url = url

    def download(self):
        ua = UserAgent()
        headers = {
            'User-Agent': str(ua.chrome)
        }
        html = requests.get(self.url, headers=headers)
        html = html.content
        return html


class Parser(object):

    def __init__(self, html):
        self.html = html
        self.bs = bs(html, "lxml")
        self.pre_process()

    def pre_process(self):
        '''
        Removing unnecessary tags from the html content
        '''
        REMOVABLE_TAGS = ['script']
        for tag in REMOVABLE_TAGS:
            [s.extract() for s in self.bs(tag)]
        text = self.bs.text
        text = text.split('\n')
        new_text = []
        for i in text:
            k = i.strip()
            if len(k)>0:
                new_text.append(i)
        self.text = new_text

    def parse(self):
        from string import ascii_letters
        english = ascii_letters + '0123456789.?@!,\'/;"'
        total, translated, non_translated = 0, 0, ''
        for i in self.text:
            nt = False
            for j in i:
                total += 1
                if j not in english:
                    translated += 1
                else:
                    non_translated += j
                    nt = True
            if nt:
                non_translated += ' '
        self.stats(total, translated, non_translated)

    def stats(self, total, translated, non_translated):
        percentage = float(translated)/total * 100
        print "Translated percentage is", percentage
        print "Non translated strings are "
        print non_translated

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Pass url as argument")
    else:
        url = sys.argv[1]
        downloader = Downloader(url)
        html = downloader.download()
        parser = Parser(html)
        parser.parse()
