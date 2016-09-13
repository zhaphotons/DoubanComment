# encoding=utf-8
import scrapy
import logging
import time
import re
import codecs
from scrapy.shell import inspect_response


logging.basicConfig(level=logging.INFO)


class DoubanMovieSpider(scrapy.Spider):
    name = "DoubanMovie_longComment"

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
             "redir": "https://movie.douban.com/subject/26322792/reviews?start=0&sort=time",
             "form_email": "zhaphotons@gmail.com",
             "form_password": "900319lgr",
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
    
        time.sleep(0.5)
        
        urls = response.xpath('//div[@class="middle"]//h3/a/@href').extract()

        for url in urls:
            item = {}

#            time.sleep(0.5)
            
            request = scrapy.Request(url, headers=self.headers, callback=self.parse_Content)
            request.meta['item'] = item
            
            yield request
       
        for href in response.xpath('//div[@class="paginator"]/span[@class="next"]/link/@href').extract():
            full_url = response.urljoin(href)
            yield scrapy.Request(full_url, headers=self.headers, callback=self.parse)
        
        
    def parse_Content(self, response):
        
#        time.sleep(1.0)
#        inspect_response(response, self)
        
        item = response.meta['item']
        
        try:
            item['rating'] = response.xpath('//header[@class="main-hd"]/span[1]/@class').extract()[0][7]        
        except:
            item['rating'] = 'None'
        
        pars = response.xpath('//div[@class="main-bd"]//div[@class="clearfix"]//text()').extract()
        item['comment'] = reduce(lambda x,y: x+y, pars).strip()
        
        yield item