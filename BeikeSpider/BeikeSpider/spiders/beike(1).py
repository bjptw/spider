# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from BeikeSpider.items import BeikespiderItem
from selenium import webdriver
from bs4 import BeautifulSoup as bs4


class BeikeSpider(CrawlSpider):
    name = 'beike'
    allowed_domains = ['wh.fang.ke.com']
    start_urls = ['http://wh.fang.ke.com/loupan/jiangxia-hongshan/#dongxihu']

    rules = (
        Rule(LinkExtractor(allow=r'/pg\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = BeikespiderItem()
        data = response.xpath("//li[@class='resblock-list']")
        for each in data:
            title = each.xpath("./a/@title").extract()[0]
            addr = each.xpath("//div[@class='resblock-location']/span[2]/text()").extract()[0]
            price = each.xpath("//span[@class='number']/text()").extract()[0]
            item["img_name"] = title  + "—" + addr + "—" + price
            item["img_url"] = each.xpath("./a/img/@data-original").extract()[0]
            yield item

        # driver = webdriver.PhantomJS()
        # self.driver.get(response.url)
        # soup = bs4(self.driver.page_source, 'html.parser')
        # data = soup.select('li[class="resblock-list"]')
        # for each in data:
        #     title = each.select("a")[0].attrs['title']
        #     addr = each.select('div[class="resblock-location"] span')[1].get_text()
        #     price = each.select("span[class='number']")[0].get_text()
        #     # if price != "价格待定":
        #     #     price = price + "元/平(均价)"
        #     item["img_name"] = title + "—" + addr + "—" + price
        #     item["img_url"] = each.select("a img")[0].attrs['src']
        #     yield item
