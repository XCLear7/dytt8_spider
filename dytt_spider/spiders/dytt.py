import re

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class DyttSpider(scrapy.Spider):
    name = 'dytt'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['https://www.ygdy8.net/html/gndy/dyzz/']

    rules = (
        # 电影详情页链接
        Rule(LinkExtractor(restrict_xpaths='//a[@class="ulink"]'), callback='movie_detail'),
        # 下一页的链接
        Rule(LinkExtractor(allow=r'list_23_([0-9]+).html'), follow=True),
    )

    def movie_detail(self, response):
        '''
        在电影详情页提取电影信息'
        :param response:
        :return:
        '''
        item = {}
        item["name"] = response.xpath('//div[@class="title_all"]/h1/font/text()').extract_first()
        """
        ◎译 名 无依之地/浪迹天地(港)/游牧之地/游牧人生(台) ◎片 名 Nomadland ◎年 代 2020 ◎产 地 美国,德国 ◎类 别 剧情 ◎语 言 英语 ◎字 幕 中英双字 ◎上映日期 2020-09-11(威尼斯电影节) / 2021-01-29(美国) / 2021-02-19(美国网络) ◎IMDb评分7.5/10 from 56101
        """
        # 下面是使用正则匹配（这个网站的网页太不规范了）
        response_str = response.text
        # 片名
        origin_name = re.findall(r'<br />◎片　　名　(.*?)<br />', response_str)
        # 产地
        place = re.findall(r'<br />◎产　　地　(.*?)<br />', response_str)
        item["产地"] = place[0] if len(place) > 0 else None
        # 年代
        time = re.findall(r'<br />◎年　　代　(.*?)<br />', response_str)
        item["年代"] = time[0] if len(time) > 0 else None
        # 简介
        brief = re.findall(r'<br />◎简　　介 <br /><br />　　(.*?)<br />', response_str)
        item["简介"] = brief[0] if len(brief) > 0 else None

        # url
        item["url"] = response.url
        yield item
