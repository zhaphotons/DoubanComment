import scrapy

from scrapy.shell import inspect_response

import numpy as np
import os

class DoubanMovieSpider(scrapy.Spider):
    name = "DoubanMovie"

    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36 Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    # }
    #
    # def start_requests(self):
    #
    #     for i in range(0,1000,20):
    #         yield scrapy.Request(
    #             'https://movie.douban.com/subject/24860563/comments?start={0}&limit=20&sort=new_score'.format(i), headers=self.headers)

    start_urls = []

    rootPath = 'file://127.0.0.1/Users/zhaphotons/Desktop/Scrapy_Test/DoubanMovie/DoubanMovie/Data/Star_Trek_Beyong/'
    files = os.listdir('.')

    for f in files:
        if f.endswith('.html'):
            start_urls.append(rootPath+f)

    # for i in range(200, 1820, 20):
    #     start_urls.append('file://127.0.0.1/Users/zhaphotons/Desktop/Scrapy_Test/DoubanMovie/DoubanMovie/Data/Star_Trek_Beyong/{0}.htm'.format(i))

    def parse(self, response):

        # inspect_response(response, self)

        print response.url

        sel = scrapy.Selector(response)

        results = sel.xpath('//div[@class="comment-item"]')

        for re in results:
            item = {}

            item['comment'] = re.xpath('./div[@class="comment"]/p/text()').extract()[0]
            try:
                item['rating'] = re.xpath('./div[@class="comment"]/h3/span[2]/span[1]/@class').extract()[0][7]
            except:
                item['rating'] = 'None'

            yield item