# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuuserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field() #用户名
    headline= scrapy.Field() #一句话描述
    answer_count = scrapy.Field() #回答数
    articles_count = scrapy.Field() #文章数
    following_count = scrapy.Field() #关注的人数
    followed_count = scrapy.Field()  #被关注的人数
    url_token = scrapy.Field() #识别用户的token
    user_url = scrapy.Field() #用户主页url
    user_type = scrapy.Field() #用户类型