# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter


class DyttSpiderPipeline:
    # TODO(xgs) 存入mysql
    def process_item(self, item, spider):
        # print(item)
        with open('电影.json', "a", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False)
            f.write("\n")
