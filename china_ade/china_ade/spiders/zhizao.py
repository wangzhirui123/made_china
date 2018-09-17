# -*- coding: utf-8 -*-
import scrapy
import sys
from china_ade.items import ChinaAdeItem
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')

class ZhizaoSpider(scrapy.Spider):
    name = 'zhizao'
    allowed_domains = ['http://cn.made-in-china.com/Construction-Decoration-Catalog/Slate-Culture-Stone.html']
    start_urls = ['http://cn.made-in-china.com/Construction-Decoration-Catalog/Slate-Culture-Stone.html']

    def parse(self, response):
        urls = response.xpath('//div[@class="sl-vam pic-mid img-min-js"]/div[@class="sl-vam-outer"]/div[@class="sl-vam-inner"]/a/@href')
        for url in urls:
            yield scrapy.Request('http://cn.made-in-china.com/'+url.extract(),callback=self.ParsePage,dont_filter=True)

        next_page = response.xpath('//a[@class="page-next"]/@href')[0].extract()
        yield scrapy.Request('http://cn.made-in-china.com/'+next_page,callback=self.parse,dont_filter=True)

    def ParsePage(self,response):
        items = ChinaAdeItem()
        items['title'] = response.xpath('//h1/text()|//h1/@title')[0].extract().replace('\r\n','')
        # print title
        dict_data = {}
        keys = response.xpath('//table[@id="prodetails_data"]/tbody/tr/th/text()')
        values = response.xpath('//table[@id="prodetails_data"]/tbody/tr/td/text()')
        items['item_class'] = '板岩、文化石'
        for num in range(len(keys)):
            dict_data[keys[num].extract()] = values[num].extract().replace('\r\n','').replace(' ','').replace('\t','')
        items['item_img'] = response.xpath('//div[@class="mImgs"]/table/tr/td/img/@src|//div[@class="big-pic"]/a/@data-url|//img[@class="imgborderdetails"]/@src')

        # with open('e:/ceshi.txt','a+')as f:
        #     f.write(response.url+str(len(item_img))+'                     \n')
        tag = response.xpath('//div[@class="de-table-bd clear"]/table/tr/td/text()')
        a = ''
        for num in range(len(tag)):
            if num %2 ==0:
                a += '\n'
            a+=tag[num].extract()
        for i in a.split('\n'):
            try:
                dict_data[i.split('：')[0]] = i.split('：')[1]
            except:
                continue
        items['dict_data'] = dict_data
        items['content'] = str(BeautifulSoup(response.body).find_all('div',class_="description")[0])
        url_dict = {}
        urls = response.xpath('//ul/li[@class="nav-item"]/a/@href')
        names = response.xpath('//ul/li[@class="nav-item"]/a/span/text()')
        for num in range(len(urls)):
            url_dict[names[num].extract()] = urls[num].extract()
        yield scrapy.Request(url_dict[u'公司信息'],meta={'items':items},callback=self.ParseCom,dont_filter=True)


    def ParseCom(self,response):
        items = response.meta['items']
        items['com_jieshao'] = response.xpath('//p[@class="companyInf js-companyInf"]')[0].xpath('string(.)')[0].extract()
        items['contact_man'] = response.xpath('//ul[@class="contactInfo"]/li[1]')[0].xpath('string(.)')[0].extract().replace('\r\n','').replace(' ','').replace('\t','')
        items['contact_zuoji'] = response.xpath('//ul[@class="contactInfo"]/li/strong[@class="contact-bd org"]/text()')[0].extract()
        try:
            items['contact_phone'] = response.xpath('//ul[@class="contactInfo"]/li/strong[@class="contact-bd org"]/text()')[1].extract()
        except:
            items['contact_phone'] = ''

        items['contact_address'] = response.xpath('//span[@class="contact-bd"]')[-1].xpath('text()')[0].extract().replace('\r\n','').replace(' ','').replace('\t','')

        tmp_list = response.xpath('//table[@class="memb-lst"]/tr/td[1]/label/@title')
        com_file_dict = {}
        a = ''
        for i in tmp_list:
            a +=i.extract()+','
        com_file_dict['主营产品'] = a
        com_file_dict['业务范围'] = response.xpath('//table[@class="memb-lst"]/tr[2]/td/text()')[0].extract()
        com_file_dict['经营模式'] = response.xpath('//table[@class="memb-lst"]/tr[3]/td/text()')[0].extract().replace('\r\n','').replace('\t','')
        items['com_file_dict'] = com_file_dict
        items['com_name'] = response.xpath('//div[@class="company-hd yyy clear"]/h1/text()|//h2[@class="only-tit js-comname4seo"]/text()|div[@class="company-hd clear"]/h2/text()') [0].extract().replace('\r\n','').replace('\t','')

        return items

