# -*- coding: utf-8 -*-

import MySQLdb
import copy
import pymongo
from china_ade import settings
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from twisted.enterprise import adbapi
from MySQLdb import cursors

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ChinaAdePipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client.zhongguozhiziao
        self.table = self.db.zhizao



    def process_item(self,item,spider):
        post_info = dict(item)
        del(post_info)['item_img']
        self.table.insert(post_info)
        return item



class MyImagesPipline(ImagesPipeline):


    def get_media_requests(self,item,info):
        for url in item['item_img']:
            yield Request(url.extract())

    def item_completed(self,results,item,info):
        img_path = [x['path'] for ok, x in results if ok]
        item['image_path'] = str(img_path)

        return item


class MysqlTwistedPipline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
        host = settings['HOST'],
        db = settings['MYSQL_DBNAME'],
        user = settings['MYSQL_USER'],
        passwd = settings['MYSQL_PASSWORD'],
        charset='utf8',
        cursorclass=MySQLdb.cursors.DictCursor,
        use_unicode=True
        )
        dbpool = adbapi.ConnectionPool('MySQLdb',**dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        aitem = copy.deepcopy(item)
        query = self.dbpool.runInteraction(self.do_insert,aitem)
        query.addErrback(self.handle_error)

    def handle_error(self,failure):
        print failure


    def do_insert(self,cursor,item):
        pass

        # with open('e:/ceshi.txt','a+')as f:
        #     f.write(item['dict_data'][u'材质']+'\n')

        # for i in item['dict_data']:
        #     i = i.replace(u'\xa0','').replace(' ','')
        #     print i
        #     sql_sele = 'select standardtype_id from jc_standard_type where name = "%s"'%(i)
        #     cursor.execute(sql_sele)
        #     try:
        #         Id = cursor.fetchone()['standardtype_id']
        #
        #     except Exception as e:
        #         sql_in_standard_type = 'insert into jc_standard_type(name)VALUES ("%s")'%(i)
        #         cursor.execute(sql_in_standard_type)
        #         sql_sele = 'select standardtype_id from jc_standard_type where name = "%s"'%(i)
        #         cursor.execute(sql_sele)
        #         Id = cursor.fetchone()['standardtype_id']






















