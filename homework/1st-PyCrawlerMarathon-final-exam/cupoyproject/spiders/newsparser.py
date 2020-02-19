# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

class NewsParser:
    def __init__(self, domain=None):
        self.domain = domain
        self.__setClassName()
        self.author = ''
        self.publish = ''
        self.content = ''
        self.implement = {
            'Mamaclub': Mamaclub
        }

    def __setClassName(self):
        domain_arr = self.domain.split('.')
        self.__class_name = domain_arr[0].capitalize()
        if len(domain_arr) > 2:
            self.__class_name += domain_arr[1].capitalize()

    def parse(self, text):
        if self.__class_name in self.implement:
            real_obj = self.implement[self.__class_name](self.domain)
            real_obj.parse(text)
            return real_obj
        else:
            return self




class Mamaclub(NewsParser):
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

        article = soup.find('div', class_="entry-content")
        paragraph = article.find_all('p')

        filtered = []
        for p in paragraph:
            v = p.text
            # 假如字串是收藏文章
            if v == '收藏文章':
                continue
            # 假如字串開頭不是作者
            if len(v) >= 2 and v[:2]=='作者':
                continue

            if v != '':
                filtered.append(v)

        # 定義一些特殊符號與全形符號的過濾器
        expr = re.compile(u'[^一-龥。；，：“”（）、？《》\s\w:/-_.?~%()]')
        for i in range(len(filtered)):
            filtered[i] = re.sub(expr, '', filtered[i])

        # 移除空白字串, 組合過濾後的文字即為文章本文 (content)
        filtered = [i for i in filtered if i]
        content = ' '.join(filtered)
        self.content = content
