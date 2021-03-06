# encoding=utf-8
import scrapy
import logging
import time
import re
import codecs
from scrapy.shell import inspect_response


logging.basicConfig(level=logging.INFO)


class DoubanMovieSpider(scrapy.Spider):
    name = "DoubanMovie2"

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
             "redir": "https://movie.douban.com/subject/2131940/comments?start=0&limit=20&sort=new_score",
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
    
        time.sleep(2)

        start, limit = re.search("start=(\d+)&limit=(\d+)",
                                 response.url).groups()
        with codecs.open("%s_%s.html" % (start, limit), "w",
                         encoding="utf-8") as o:
            o.write(response.text)

        for i in response.css("#paginator .next").xpath("@href").extract():
            full_url = response.urljoin(i)
            yield scrapy.Request(
                full_url,
                headers=self.headers,
            )

