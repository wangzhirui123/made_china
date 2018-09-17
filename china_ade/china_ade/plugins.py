# -*- coding: utf-8 -*-
__author__ = 'Px'

import sys
import re
import time
import requests
import pymongo
import MySQLdb
from china_ade import settings
from twisted.enterprise import adbapi
from MySQLdb import cursors
from lxml import etree
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

def in_MySQL():
    connection = pymongo.MongoClient()
    db = connection.zhongguozhiziao
    table = db.zhizao
    for item in table.find({}):
        try:
            print item['dict_data'][u'商标']
        except:
            print ''
if __name__ == '__main__':
    conn = MySQLdb.connect('101.201.70.139','root','Myjr678!@#','spider',charset='utf8')
    cur = conn.cursor()
    in_MySQL()