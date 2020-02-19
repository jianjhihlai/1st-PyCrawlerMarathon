# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import CupoyNewsItem
from . import newsparser
from urllib.parse import urlparse


class CupoynewsSpider(scrapy.Spider):
    name = 'cupoynews'
    # allowed_domains = ['www.cupoy.com']
    # start_urls = 'https://www.cupoy.com/MixNewsMongoAction.do?op=getTopMixNewsByBucketGroup&groupid=life_tw&len=30'

    def __init__(self, group_id = 'life_tw'):
        self.group_id = group_id;
        self.start_urls = 'https://www.cupoy.com/MixNewsMongoAction.do?op=getTopMixNewsByBucketGroup&groupid={}&len=500'.format(self.group_id)
        super().__init__()

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse)

    def parse(self, response):
        total_data = json.loads(response.text)
        assert "items" in total_data, 'got improper data:%s' % total_data
        news_collection = total_data['items']
        for news in news_collection:
            data = CupoyNewsItem()
            data['itemuid'] = news['itemuid']
            data['newsid'] = news['newsid']
            data['title'] = news['title']
            data['description'] = news['description'] if 'description' in news else ''
            data['linkurl'] = news['linkurl']
            data['bucketgrpids'] = news['bucketgrpids']
            data['content'] = ''
            request = scrapy.Request(url=news['linkurl'],
                                     callback=self.parse_news)
            request.meta['data'] = data
            yield request

    def parse_news(self, response):
        data = response.meta.get('data', None)
        parser = newsparser.NewsParser(self.parse_domain(response.url))
        parsed = parser.parse(response.text)
        data['author'] = parsed.author
        data['publish'] = parsed.publish
        if parsed.content == '':
            data['content'] = data['description']
        else:
            data['content'] = parsed.content
        yield data


    def parse_domain(self, article_url):
        parsed_uri = urlparse(article_url)
        get_domain = '{uri.netloc}'.format(uri=parsed_uri)
        return get_domain
