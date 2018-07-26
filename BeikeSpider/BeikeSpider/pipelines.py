# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import json
from scrapy.conf import settings

class BeikespiderPipeline(object):
    # def __init__(self):
    #     self.filename = open("beike.json","wb")
    #     self.num = 0
    #
    # def process_item(self, item, spider):
    #     text = json.dumps(dict(item),ensure_ascii=False) + "\n"
    #     self.filename.write(text.encode("utf-8"))
    #     self.num += 1
    #     return item
    #
    # def close_spider(self,spider):
    #     self.filename.close()
    #     print("总共有" + str(self.num) + "个资源")

    #保存图片
    def process_item(self, item, spider):
         if 'img_url' in item:
            dir_path = settings["IMAGES_STORE"]
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            su = "." + item["img_url"].split(".")[-1]
            path = item["img_name"] + su
            new_path = '%s/%s' % (dir_path, path)
            if not os.path.exists(new_path):
                with open(new_path, 'wb') as handle:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "Referer":"https://wh.fang.ke.com/loupan/p_blddhabkcr/.75x75.jpg",
                    }
                    response = requests.get(item["img_url"], stream=True,headers=headers)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
            return item
