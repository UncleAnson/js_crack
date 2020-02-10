# -*- coding: utf-8 -*-
import hashlib

import redis
import scrapy
from article.items import ArticleItem, ZhengcekuItem, ZhengceContentItem
from article.util import return_tag

m = hashlib.md5()
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
conn = redis.StrictRedis(connection_pool=pool)


class YiqingSpider(scrapy.Spider):
    name = 'gwyspider'

    def start_requests(self):
        # # 国务院
        urls = [
            # ("http://sousuo.gov.cn/column/49127/0.htm", "国务院-政务动态-中央动态"),
            # ("http://sousuo.gov.cn/column/49129/0.htm", "国务院-政务动态-部门动态"),
            # ("http://sousuo.gov.cn/column/49128/0.htm", "国务院-防控动态"),
            ("http://sousuo.gov.cn/column/30469/0.htm", "国务院-最新政策")

        ]
        for url, name in urls:
            yield scrapy.Request(url, meta={"website": name}, callback=self.parse_gwy)
        # 测试
        # wjw_cookie = get_cookie("http://www.nhc.gov.cn/xcs/kpzs/list_gzbd_5.shtml")
        # url= 'http://www.nhc.gov.cn/xcs/fkdt/202001/52998d14ad824bc9bf499d3915b9dbb1.shtml'
        # yield scrapy.Request(url, meta={"website": "test_website", "tag": "test_tag"},
        #                      callback=self.parse_wjw_detail)  # , cookies=wjw_cookie)

    def parse_gwy(self, response):
        website = response.meta["website"]
        tag = response.xpath('//span[@class="tabg"]/text()').extract()[0].strip()
        print("爬取 ", tag)
        articles = response.xpath('//h4')
        current_page = response.xpath('//input[@id="pnum"]/@value').extract()[0]
        print("当前爬取页：", current_page)

        for a_dom in articles:
            title = a_dom.xpath("./a/text()").extract()[0]
            href = a_dom.xpath("./a/@href").extract()[0]
            # 不采集视频文章
            if "cntv" in href:
                print(title, href, "放弃原因：视频")
                continue
            # 判断是否采集完成
            # if conn.hget("bf", tag + '-' + href):
            #     print("采集完成，网站{}的{}板块({}) 最新数据为{}({})".format(website, tag, response.url, title, href))
            #     return
            # else:
            #     conn.hset("bf",  tag + '-' + href, 1)
            print(title, href)

            # 浏览更多政策请点击进入“文件库”>>>
            if " http://www.gov.cn/zhengce/xxgkzl.htm" == href:
                continue

            # 进入详情页
            if "zhengce/zhengceku" in href:
                yield scrapy.Request(url=href, callback=self.parse_zhengce_zhengceku,
                                     meta={"tag": tag, "website": website})
            elif "zhengce/content" in href:
                yield scrapy.Request(url=href, callback=self.parse_zhengce_content,
                                     meta={"tag": tag, "website": website})
            else:
                yield scrapy.Request(url=href, callback=self.parse_content, meta={"tag": tag, "website": website})

        try:
            next_page_url = response.xpath('//a[@class="next"]/@href').extract()[0]
        except:
            print(website, tag, "已到达末页")
        else:
            print("next_page_url", next_page_url)
            # 翻页
            yield scrapy.Request(next_page_url, callback=self.parse_gwy, meta={"website": website})

    def parse_content(self, response):
        tag = response.meta["tag"]
        website = response.meta["website"]
        title = ''.join(
            response.xpath('//div[@class="article oneColumn pub_border"]/h1/text()').extract()).strip().replace('"',
                                                                                                                '\"')
        url = response.url
        pub_time = response.xpath('//div[@class="pages-date"]/text()').extract()[0].strip()
        source = response.xpath('//div[@class="pages-date"]/span[contains(text(),"来源")]/text()').extract()[0].split(' ')
        if len(source) == 1:
            source = ''
        else:
            source = source[-1]
        content = ''.join(response.xpath('//div[@class="pages_content"]/p/text()').extract()).replace('"', '\"')
        images = response.xpath('//div[@class="pages_content"]//p/img/@src').extract()
        base_url = "http://" + "/".join(url.split('/')[2:-1]) + "/"
        images = [base_url + image for image in images]
        article_id = hashlib.md5(url.encode()).hexdigest()
        # print(article_id)
        # print(tag)
        # print(website)
        print(title)
        print(url)
        # print(pub_time)
        # print(source)
        # print(content)

        article = ArticleItem()
        article["article_id"] = article_id
        article["tag"] = return_tag(title, tag, source)
        article["website"] = website
        article["title"] = title
        article["url"] = url
        article["pub_time"] = pub_time
        article["source"] = source
        article["content"] = content
        article["image_url"] = images
        yield article

    def parse_zhengce_zhengceku(self, response):
        tag = response.meta["tag"]
        website = response.meta["website"]
        url = response.url
        article_id = hashlib.md5(url.encode()).hexdigest()

        # 标题
        title = ''.join(response.xpath('//div[@class="policyLibraryOverview_header"]//tr[2]/td[2]/text()').extract())
        # 发文机关
        pub_dept = ''.join(response.xpath('//div[@class="policyLibraryOverview_header"]//tr[2]/td[4]/text()').extract())
        # 发文字号
        pub_no = ''.join(response.xpath('//div[@class="policyLibraryOverview_header"]//tr[3]/td[2]/text()').extract())
        # 来源
        source = ''.join(response.xpath('//div[@class="policyLibraryOverview_header"]//tr[3]/td[4]/text()').extract())
        # 主题分类
        cate = ''.join(
            response.xpath('//div[@class="policyLibraryOverview_header"]//tr[4]/td[2]/text()').extract()).replace('\\',
                                                                                                                  '/')
        # 公文种类
        file_type = ''.join(
            response.xpath('//div[@class="policyLibraryOverview_header"]//tr[4]/td[4]/text()').extract())
        # 成文日期
        write_date = ''.join(
            response.xpath('//div[@class="policyLibraryOverview_header"]//tr[5]/td[2]/text()').extract())
        # 发文日期
        pub_date = ''.join(response.xpath('//div[@class="policyLibraryOverview_header"]//tr[5]/td[4]/text()').extract())
        content = ''.join(response.xpath('//div[@class="pages_content"]//text()').extract())
        # 附件信息
        attach = response.xpath('//div[@class="pages_content"]//p/a')
        attachment = []
        for a in attach:
            file_name = a.xpath('./text()').extract()[0]
            download_url = a.xpath('./@href').extract()[0]
            attachment.append((file_name, download_url))

        item = ZhengcekuItem()
        item["source"] = source
        item["file_type"] = file_type
        item["cate"] = cate
        item["pub_dept"] = pub_dept
        item["write_date"] = write_date
        item["pub_date"] = pub_date
        item["content"] = content
        item["title"] = title
        item["pub_no"] = pub_no
        item["tag"] = tag
        item["website"] = website
        item["url"] = url
        item["article_id"] = article_id
        item["attachment"] = attachment
        yield item

    def parse_zhengce_content(self, response):
        print('~~~~')
        tag = response.meta["tag"]
        website = response.meta["website"]
        url = response.url
        article_id = hashlib.md5(url.encode()).hexdigest()

        # 索引号
        index_no = ''.join(response.xpath('//td/table[@class="bd1"][1]//tr[1]/td[2]/text()').extract())
        # 主题分类
        cate = ''.join(response.xpath('//td/table[@class="bd1"][1]//tr[1]/td[4]/text()').extract()).replace('\\', '/')
        # 发文机关
        pub_dept = ''.join(response.xpath('//td/table[@class="bd1"][1]//tr[2]/td[2]/text()').extract())
        # 成文日期
        write_date = ''.join(response.xpath('//td/table[@class="bd1"][1]//tr[2]/td[4]/text()').extract())
        # 标题
        title = ''.join(response.xpath('//td/table[@class="bd1"][1]//tr[3]/td[2]/text()').extract())
        # 发文字号
        pub_no = ''.join(response.xpath('//td/table[@class="bd1"][1]//tr[4]/td[2]/text()').extract())
        # 发文日期
        pub_date = ''.join(response.xpath('//td/table[@class="bd1"][1]//tr[2]/td[4]/text()').extract())
        content = ''.join(response.xpath('//td[@id="UCAP-CONTENT"]//text()').extract())

        item = ZhengceContentItem()
        item["index_no"] = index_no
        item["cate"] = cate
        item["pub_dept"] = pub_dept
        item["write_date"] = write_date
        item["pub_date"] = pub_date
        item["content"] = content
        item["title"] = title
        item["pub_no"] = pub_no
        item["tag"] = tag
        item["website"] = website
        item["url"] = url
        item["article_id"] = article_id
        yield item
