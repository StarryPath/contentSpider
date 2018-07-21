# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5

import MySQLdb
import MySQLdb.cursors


class ContentspiderPipeline(object):

    def __init__(self):
        try:
            self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host='localhost',
                                            db='test',
                                            user='root',
                                            passwd='',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=True
                                            )
            print "Connect to db successfully!"

        except:
            print "Fail to connect to db!"

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_into_table, item)
        return item

    def insert_into_table(self, conn, item):

        sql = "insert into data(title,head,body,real_url,get_url) values(%s,%s,%s,%s,%s)"
        param = ([item['title'], item['head'], item['body'], item['real_url'],item['get_url']])
        conn.execute(sql, param)
        sql2 = "update url_list set flag=%s where url=%s"
        param2 = ("1",item['get_url'])
        conn.execute(sql2, param2)
#a='UPDATE grabsite set title='+item['title']+',head='+item['head']+',body='+item['body']+' where siteName ='+item['Url']
        #conn.execute(a)
