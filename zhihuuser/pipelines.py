# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class ZhihuUserPipeline(object):
    def process_item(self, item, spider):
        #写入文件中
        with open('result.txt', 'a', encoding='utf-8') as f:
            f.write(item['name'] + '\t' + item['headline'] + '\n')
        return item
