import json
import math
import re
# from scrapy import Spider, Request
from ..items import ZhihuuserItem
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request


class ZhihuUsers(RedisSpider):
    name = 'zhihu_user'
    redis_key = 'ZhihuUsers:start_urls'
    start_user = 'sgai'
    start_urls = ['https://www.zhihu.com/api/v4/members/{}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}'.format(start_user, str(0))]
    user_url = 'https://www.zhihu.com/people/{}/activities'

    def parse(self, response):

        datas = json.loads(response.text)
        total_following = datas['paging']['totals']
        pages = math.ceil(int(total_following)/20)

        for page in range(0, int(pages)):
            following_list = 'https://www.zhihu.com/api/v4/members/{}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}'.format(
                self.start_user, str(20*page))
            yield Request(following_list,callback=self.parse_user)

    def parse_user(self, response):
        datas = json.loads(response.text)
        item = ZhihuuserItem()
        for info in datas['data']:
            item['name'] = info['name']
            dc = re.compile(r'<[^>]+>', re.S)
            item['headline'] = dc.sub('', info['headline'])
            item['answer_count'] = info['answer_count']
            item['articles_count'] = info['articles_count']
            item['followed_count'] = info['follower_count']
            item['url_token'] = info['url_token']
            item['user_url'] = 'https://www.zhihu.com/people/{}'.format(info['url_token'])
            item['user_type'] = info['type']
            yield item
            url =  'https://www.zhihu.com/api/v4/members/{}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}'.format(
                info['url_token'], str(0))
            yield Request(url, meta={'user_token': info['url_token']}, callback=self.second_user)

    def second_user(self, response):
        datas = json.loads(response.text)
        total_following = datas['paging']['totals']
        pages = math.ceil(int(total_following) / 20)

        for page in range(0, int(pages)):
            following_list = 'https://www.zhihu.com/api/v4/members/{}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}'.format(
                response.meta['user_token'], str(20 * page))
            yield Request(following_list, callback=self.parse_user)
