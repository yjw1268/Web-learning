#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import sys
import pymysql

se = requests.Session()  # 模拟登陆
requests.adapters.DEFAULT_RETRIES = 15
se.mount('http://', HTTPAdapter(max_retries=3))  # 重联
se.mount('https://', HTTPAdapter(max_retries=3))

class Pixiv(object):

    def __init__(self):
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.search_url = 'https://www.pixiv.net/search.php'
        self.main_url = 'https://www.pixiv.net'
        self.target_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='
        self.headers = {
            'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        }
        self.pixiv_id = '835437423@qq.com',  # 2664504212@qq.com
        self.password = 'yjw3616807',  # knxy0616
        self.post_key = []
        self.return_to = 'https://www.pixiv.net/'
        self.load_path = './search_pic/'  # 存放图片路径


    def login(self):
        post_key_xml = se.get(self.base_url, headers=self.headers).text
        post_key_soup = BeautifulSoup(post_key_xml, 'lxml')
        self.post_key = post_key_soup.find('input')['value']
        # 构造请求体
        data = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'post_key': self.post_key,
            'return_to': self.return_to
        }
        se.post(self.login_url, data=data, headers=self.headers)

    def download(self):
        pixiv_id=sys.argv[1]
        db = pymysql.connect("localhost", "root", "PlanetarAntimony", "Study")
        cursor = db.cursor()
        sql = "SELECT pixiv_id,original_url FROM pixiv_search WHERE pixiv_id = '%s' " % (pixiv_id)
        cursor.execute(sql)
        results = cursor.fetchall()
        if(results):
            original_url=results[0][1]
        else:
            sql = "SELECT pixiv_id,original_url FROM pixiv_rank WHERE pixiv_id = '%s' " % (pixiv_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            original_url=results[0][1]
        print(original_url)
        img = se.get(original_url, headers=self.headers)
        with open(self.load_path + pixiv_id + '.jpg', 'wb') as f:  # 图片要用b,对text要合法化处理
            f.write(img.content)  # 保存图片
        # olocal_url='http://study.imoe.club/Try/search_pic/'+ pixiv_id + '.jpg'
        # sql = "INSERT INTO pixiv_search(olocal_url) VALUES ('%s')" % (olocal_url)


if __name__ == '__main__':
    pixiv = Pixiv()
    pixiv.login()
    pixiv.download()
    print("System Exit")
