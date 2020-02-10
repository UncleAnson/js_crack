# -*- coding: utf-8 -*-

from urllib.parse import urlparse

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

from .items import ArticleItem, ZhengcekuItem, ZhengceContentItem, PressItem

settings = get_project_settings()


class ArticlePipeline(object):
    def open_spider(self, spider):
        self.con = pymysql.connect(host=settings['MYSQL_HOST'], port=settings['MYSQL_PORT'],
                                   user=settings['MYSQL_USER'], passwd=settings['MYSQL_PASSWORD'],
                                   db=settings['MYSQL_DATABASE'])
        self.cur = self.con.cursor()
        self.insert_sql = 'insert into article_yiqing (article_id, title, website, url, pub_time, content, source, tag) values ("{}","{}","{}","{}","{}","{}","{}","{}")'
        self.insert_sql_zhengceku = 'insert into zhengceku (source, file_type, cate, pub_dept, write_date, pub_date, content, title, pub_no, tag, website, url, article_id) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'
        self.insert_sql_zhengceContent = 'insert into zhengceContent (index_no, cate, pub_dept, write_date, pub_date, content, title, pub_no, tag, website, url, article_id) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'
        self.insert_sql_attachment = 'insert into attachment (article_id, url ,file_name) values ("{}","{}","{}")'
        self.insert_sql_press = 'insert into press_yiqing (article_id, title, website, url, pub_time, content, state, tag, guest, location, abstract) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'

    def process_item(self, item, spider):
        if type(item) == ArticleItem:
            sql = self.insert_sql.format(
                item["article_id"], item["title"], item["website"], item["url"], item["pub_time"], item["content"],
                item["source"], item["tag"])
            try:
                self.cur.execute(sql)
            except Exception as e:
                print(sql)
                raise e
        elif type(item) == ZhengcekuItem:
            for url, name in item["attachment"]:
                sql = self.insert_sql_attachment.format(item["article_id"], url, name)
                self.cur.execute(sql)
            sql = self.insert_sql_zhengceku.format(item["source"], item["file_type"], item["cate"], item["pub_dept"],
                                                   item["write_date"], item["pub_date"], item["content"], item["title"],
                                                   item["pub_no"], item["tag"], item["website"], item["url"],
                                                   item["article_id"])
            self.cur.execute(sql)
        elif type(item) == ZhengceContentItem:
            sql = self.insert_sql_zhengceContent.format(item["index_no"], item["cate"], item["pub_dept"],
                                                        item["write_date"], item["pub_date"], item["content"],
                                                        item["title"],
                                                        item["pub_no"], item["tag"], item["website"], item["url"],
                                                        item["article_id"])
            self.cur.execute(sql)
        elif type(item) == PressItem:
            sql = self.insert_sql_press.format(item["article_id"], item["title"], item["website"], item["url"],
                                               item["pub_time"], item["content"], item["state"], item["tag"],
                                               item["guest"], item["location"], item["abstract"])
            self.cur.execute(sql)
        self.con.commit()

        return item

    def __del__(self):
        self.con.close()


class ImagePipeline(ImagesPipeline):
    # 重写方法
    def get_media_requests(self, item, info):
        if type(item) in (ArticleItem, PressItem):
            netloc = urlparse(item['url']).netloc
            default_headers = {
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Host': netloc,
                'Referer': item['url'],
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            }
            image_url = item["image_url"]
            if image_url:
                for i, url in enumerate(image_url):
                    # print(url)
                    yield scrapy.Request(url, headers=default_headers,
                                         meta={"image_name": item["article_id"] + '-' + str(i)})

    # # 保存图片时重命名
    # def item_completed(self, results, item, info):
    #     print(results)
    #     print("*"* 30)
    #     # 列表推导式，获取图片的保存路径
    #     # image_url = [x["path"] for ok, x in results if ok]
    #
    #     # 重命名，由于都是jpg文件，所以直接拼上了
    #     os.rename(images_store + image_url[0], images_store + item["article_id"] + ".jpg")

    def file_path(self, request, response=None, info=None):
        image_name = request.meta["image_name"]
        # 重命名(包含后缀名)，若不重写这函数，图片名为哈希
        # pic_path = request.url.split('/')[-1]
        return image_name + ".jpg"
