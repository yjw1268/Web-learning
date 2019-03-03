#!/usr/bin/python3

import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import time
import sys, re
import os

se = requests.Session()  # 模拟登陆
requests.adapters.DEFAULT_RETRIES = 15
se.mount('http://', HTTPAdapter(max_retries=3))  # 重联
se.mount('https://', HTTPAdapter(max_retries=3))


class Pixiv(object):

    def __init__(self):
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.modebase = {
            '1': 'daily',
            '2': 'weekly',
            '3': 'monthly',
            'R1': 'daily_r18',
            'R2': 'weekly_r18',
            'RG': 'r18g',
        }
        self.target_url_1 = 'https://www.pixiv.net/ranking.php?mode='
        self.main_url = 'https://www.pixiv.net'
        self.headers = {
            # 'Host': 'accounts.pixiv.net',
            # 'Origin': 'https://accounts.pixiv.net',
            'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            # 'X-Requested-With': 'XMLHttpRequest'
            # 'Connection': 'close',
        }
        # self.proxies = {
        #     'https': 'https://127.0.0.1:1080',
        #     'http': 'http://127.0.0.1:1080'
        # }
        self.pixiv_id = '835437423@qq.com',  # 2664504212@qq.com
        self.password = 'yjw3616807',  # knxy0616
        self.post_key = []
        self.return_to = 'https://www.pixiv.net/'
        self.load_path = './rank_pic/'  # 存放图片路径

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

    def choosemode(self):
        #print("请选择看图模式:")
        text = str(sys.argv[1])
        mode = self.modebase[text]
        print(mode)
        return mode

    def getnum(self, mode):
        # print(mode)
        if mode == 'daily_r18' or mode == 'weekly_r18':
            print("?")
            getnumber = str(sys.argv[2])
            if (getnumber.isdigit()):
                if int(getnumber) > 5 or int(getnumber) < 1:
                    print("-1")
                    sys.exit()
            elif (getnumber == ''):
                getnumber = 3
            else:
                print("-1")
                sys.exit()
        elif mode == 'r18g':
            print("!")
            getnumber = 1
        else:
            #print("你要看几张图？默认5份（输入1~8）")
            getnumber = str(sys.argv[2])
            if (getnumber.isdigit()):
                if int(getnumber) > 5 or int(getnumber) < 1:
                    print("-1")
                    sys.exit()
            elif (getnumber == ''):
                getnumber = 5
            else:
                print("-1")
                sys.exit()
        return int(getnumber)

    # def secontect(self, target_url):
    #     s = se.get(self.target_url_1 + str(target_url))  # https://www.pixiv.net/setting_user.php
    #     print("s")
    #     print(s.text)
    #     with open(self.load_path + 'Re.html', 'w', encoding='utf-8') as f:
    #         f.write(s.text)
    #         print("sc")

    def validateTitle(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

    def beautifulsoup(self, get_number,target_url):
        s = se.get(self.target_url_1 + str(target_url))
        soup = BeautifulSoup(s.text, features="html.parser")  # 初始化
        # with open(self.load_path + 'Re_soup.html', 'w', encoding='utf-8') as f:
        #     f.write(soup.prettify())  # 保存soup以便check
        title = soup.find_all("a", class_="title", limit=get_number)  # 寻找每周前get_number
        src_headers = self.headers
        for i in title:
            temp_url = self.main_url + '/' + i['href']
            # print(temp_url)  # 详细页的url
            temp_clear = se.get(temp_url, headers=src_headers)
            clear_soup = BeautifulSoup(temp_clear.text, features="html.parser")
            name = self.validateTitle(i.string).decode("utf-8")
            op = clear_soup.prettify().find('"original":"')
            ed = clear_soup.prettify().find('},"tags')
            original_url = clear_soup.prettify()[op + 12:ed - 1]
            adapt_url = original_url.replace('\/', '/')
            print(adapt_url)
            img = se.get(adapt_url, headers=src_headers)
            with open(self.load_path + name + '.jpg', 'wb') as f:  # 图片要用b,对text要合法化处理
                f.write(img.content)  # 保存图片
            print("Finish")
            time.sleep(1)
        # 拉取缩略图
        # pic_dl = soup.find_all("img", class_="_thumbnail ui-scroll-view", limit=get_number)
        # i = 0  # 命名需要
        # for j in pic_dl:
        #     pic_dl_url = j["data-src"]
        #     print(pic_dl_url)  # 缩略图的url
        #     img = requests.get(pic_dl_url, headers=self.headers)  # 下载图片
        #     with open(self.load_path + '1' + '.jpg', 'wb') as f:  # 图片要用b,对text要合法化处理
        #         f.write(img.content)  # 保存图片
        #     i += 1
        # print("Read.")


if __name__ == '__main__':
    pixiv = Pixiv()
    print("Checking permissions...")
    pixiv.login()
    # print("Loggin")
    print("Welcome!")
    # print(" '1':'每日Top'", "'2':'每周Top'",  "'3':'每月Top',", "'R1':'每日色图Top'", "'R2':'每周色图Top'","'RG':'r18g',")
    mode = pixiv.choosemode()
    print("Linking to the sever...")
    # pixiv.secontect(mode)
    print("Getting page contents...")
    pixiv.beautifulsoup(pixiv.getnum(mode),mode)
    print("System Exit")
