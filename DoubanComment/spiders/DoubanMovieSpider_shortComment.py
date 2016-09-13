# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 14:04:59 2016

@author: lenovo
"""

# encoding=utf-8
import scrapy
import logging
import time
import codecs
from scrapy.shell import inspect_response


logging.basicConfig(level=logging.INFO)


class DoubanMovieSpider(scrapy.Spider):
    name = "DoubanMovie_shortComment"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
    }

    captcha_solution = ""

    def start_requests(self):

        yield scrapy.Request(
            "https://accounts.douban.com/login",
            headers=self.headers,
            callback=self.login
        )

    def login(self, response):
        formdata={
             "redir": "https://movie.douban.com/subject/26776092/comments?start=0&limit=20&sort=new_score",
             "form_email": "ravna@qq.com",
             "form_password": "huapanda2013",
             "login": u"登录",
         }

        # 这段用于手动输入验证码
        captcha_img = response.css(".item-captcha img").xpath("@src").extract()
        if captcha_img:
            captcha_img_src = captcha_img[0]
            print(captcha_img_src)
            formdata["captcha-id"] = captcha_img_src.split("&")[0].split("=")[1]
            formdata["captcha-solution"] = raw_input("input captcha solution: ")

        yield scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            headers=self.headers,
        )

    def parse(self, response):
        # assert response.css(".nav-user-account").extract(), "not login"
#        inspect_response(response, self)
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

        for i in response.css("#paginator .next").xpath("@href").extract():
            full_url = response.urljoin(i)
            yield scrapy.Request(full_url, headers=self.headers, callback=self.parse)
