# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from . import newsparser
import re

class Mamaclub(newsparser.NewsParser):
    def __init__(self, domain=None):
        super().__init__(domain)

    def parse(self, text):
        soup = BeautifulSoup(text)
        author_span = soup.find('span', class_='vcard author')
        self.author = author_span.text
        pattern = re.compile(u"((?<=發表於\s)(((19|20)?[0-9]{2}[- \/\.](0?[1-9]|1[012])[- \/\.](0?[1-9]|[12][0-9]|3[01]))*))")
        div_author_meta = soup.find('div', class_='meta-author')
        author_meta = div_author_meta.text.strip()
        match = pattern.search(author_meta)
        if match:
            self.publish = match.group(0)
        else:
            self.publish = ''
