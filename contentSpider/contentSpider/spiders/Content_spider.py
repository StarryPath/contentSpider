import scrapy
import MySQLdb.cursors
from contentSpider.items import ContentspiderItem
from scrapy import Request

class contentSpider(scrapy.Spider):
    name = "contentSpider"

    def __init__(self, **kwargs):

        super(contentSpider, self).__init__(**kwargs)
        try:
            self.con = MySQLdb.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='',
                db='test'
            )
            print
            "connect db successfully!"
        except:
            print
            "connect db failed!"


        self.urls = []

        self.cur = self.con.cursor()

        self.cur.execute("select url from biao4 where flag=0 " )

        rows = self.cur.fetchall()

        for row in rows:
            url = str(row)[2:-3]
            self.urls.append(url)
        self.urls=list(set(self.urls))
        self.start_urls = self.urls[:]
        print self.start_urls

    def parse(self, response):

        for get_url in self.start_urls:
            item = ContentspiderItem()
            item['get_url'] = get_url
            url=get_url

            yield Request(url,meta={'key':item},callback=self.parse_page1)

    def parse_page1(self, response):

        item = response.meta['key']

        item['title'] = response.xpath('/html/head/title').re(u'[\u4e00-\u9fa5]')
        item['head'] = response.xpath('/html/head').re(u'[\u4e00-\u9fa5]')
        item['body'] = response.xpath('/html/body').re(u'[\u4e00-\u9fa5]')
        item['body'] = ''.join(item['body'])
        item['head'] = ''.join(item['head'])
        item['title'] = ''.join(item['title'])
        item['real_url'] = response.url

        yield item
