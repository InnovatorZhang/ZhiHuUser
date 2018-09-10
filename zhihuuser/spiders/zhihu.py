# -*- coding: utf-8 -*-
import json

import scrapy

from zhihuuser.items import UserItem

#重复的数据可以在插入数据进数据库那一步中去除
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    #用户信息
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    start_user = 'excited-vczh'

    #关注列表
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    #粉丝列表
    followers_url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        #从大V轮子哥开始查询
        yield scrapy.Request(self.user_url.format(user=self.start_user,include=self.user_query), self.parse_user)


    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        #field是item的名称,遍历定义的item
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        #查询用户的关注列表
        user = result.get('url_token')
        yield scrapy.Request(self.follows_url.format(user=user,include=self.follows_query,offset=0,limit=20),self.parse_follows)
        #查询用户的粉丝列表
        yield scrapy.Request(self.followers_url.format(user=user,include=self.followers_query,offset=0,limit=20),self.parse_followers)

    def parse_follows(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),self.parse_user)

        #判断是否有paging标签和是否到了最后一页
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            #获取下一页地址
            next_page = results.get('paging').get('next')
            yield scrapy.Request(next_page, self.parse_follows)

    def parse_followers(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),self.parse_user)

        #判断是否有paging标签和是否到了最后一页
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            #获取下一页地址
            next_page = results.get('paging').get('next')
            yield scrapy.Request(next_page, self.parse_followers)