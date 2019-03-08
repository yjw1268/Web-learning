#!/usr/bin/python3

import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from urllib import parse
import time
import json
import sys
import re
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
        self.get_number = 10
        self.searchword = ''
        self.mark = 0
        self.pages = '&order=date_d&p='
        self.page = 1
        self.temp_number = 0

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

    def search(self):
        self.searchword = sys.argv[1]  # 搜索关键词
        self.mark = sys.argv[2]  # 赞数设置
        # if (self.mark.isdigit()):
        #     if int(self.mark) > 20000 or int(self.mark) < 1:
        #         print("输入数字不合法,程序自动结束")
        #         sys.exit()
        # elif (self.mark == ''):
        #     self.mark = 1000
        # else:
        #     print("输入格式不合法,程序自动结束")
        #     sys.exit()
        self.get_number = sys.argv[3]  # 获取图片数
        # if (self.get_number.isdigit()):
        #     if int(self.get_number) > 10 or int(self.get_number) < 1:
        #         print("输入数字不合法,程序自动结束")
        #         sys.exit()
        # elif (self.get_number == ''):
        #     self.get_number = 3
        # else:
        #     print("输入格式不合法,程序自动结束")
        #     sys.exit()
        self.page = sys.argv[4]
        # if (self.page.isdigit()):
        #     if int(self.page) > 100 or int(self.page) < 1:
        #         print("输入数字不合法,程序自动结束")
        #         sys.exit()
        # elif (self.page == ''):
        #     self.page = 1
        # else:
        #     print("输入格式不合法,程序自动结束")
        #     sys.exit()
        self.page = int(self.page)

    def validateTitle(self,title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

    def sbeautifulsoup(self):
        # print(parse.quote(self.searchword))
        payload = {'s_mode': 's_tag', 'word': self.searchword,'order':'date_d','p':self.page}
        # data = urllib.parse.urlencode(payload).encode(encoding="UTF8")
        s = se.get(self.search_url,params=payload)
        self.page += 1
        soup = BeautifulSoup(s.text, features="html.parser")  # 初始化
        # 数据库操作
        db = pymysql.connect("localhost", "root", "PlanetarAntimony", "Study")
        cursor = db.cursor()
        # with open(self.load_path + 'Re_soup.html', 'w', encoding='utf-8') as f:
        #     f.write(soup.prettify())  # 保存soup以便check
        texts = soup.find_all("input", attrs={'data-items': True})
        text = texts[0]['data-items']
        # print(text)
        list = json.loads(text)
        src_headers = self.headers
        for i in list:
            if self.temp_number >= int(self.get_number):
                break
            if (i['bookmarkCount'] >= int(self.mark)):
                pic_dl_url= i['url']  # 缩略图地址
                pic_id = i['illustId']  # 图片id
                temp_url = self.target_url + pic_id
                sql = "SELECT pixiv_id,searchword FROM pixiv_search WHERE pixiv_id = '%s' AND searchword = '%s'" % (pic_id,self.searchword)
                cursor.execute(sql)
                results = cursor.fetchall()
                if results:
                    #print("1")
                    self.temp_number += 1
                    continue
                #print(pic_dl_url)
                temp_clear = se.get(temp_url, headers=src_headers)
                clear_soup = BeautifulSoup(temp_clear.text, features="html.parser")
                title = self.validateTitle(i['illustTitle'])
                op = clear_soup.prettify().find('"original":"')
                ed = clear_soup.prettify().find('},"tags')
                original_url = clear_soup.prettify()[op + 12:ed - 1]
                adapt_url = original_url.replace('\/', '/')
                # 命名格式：mark_date_number.jpg
                dlname = 'mark'+str(i['bookmarkCount']) + '_page' + str(self.page) + '_' +time.strftime("%Y-%m-%d", time.localtime()) + '_' + str(self.temp_number) + '.jpg'
                local_url='http://study.imoe.club/Try/search_pic/' + dlname
                # img = se.get(adapt_url, headers=src_headers)
                # with open(self.load_path + title + '.jpg', 'wb') as f:  # 图片要用b,对text要合法化处理
                #     f.write(img.content)  # 保存图片
                # 保存缩略图
                img = requests.get(pic_dl_url, headers=src_headers)  # 下载图片
                with open(self.load_path + dlname, 'wb') as f:  # 图片要用b,对text要合法化处理
                    f.write(img.content)  # 保存图片
                # print("Downloaded")
                sql = "INSERT INTO pixiv_search(searchword,number,marks,raw_url, pixiv_id,original_url,local_url,title, page) VALUES ('%s','%s','%s','%s', '%s','%s','%s','%s', '%s')" % \
                  (str(self.searchword),str(self.temp_number),str(i['bookmarkCount']),str(pic_dl_url), str(pic_id), str(adapt_url), str(local_url), str(title), str(self.page))
                # 执行sql语句
                cursor.execute(sql)
                db.commit()
                self.temp_number += 1
            #     time.sleep(2)
            # time.sleep(1)


if __name__ == '__main__':
    pixiv = Pixiv()
    pixiv.login()
    pixiv.search()
    while pixiv.temp_number < int(pixiv.get_number):
        # print("Getting content of page " + str(pixiv.page))
        pixiv.sbeautifulsoup()
        if (pixiv.page >= 100):
            break
    print("System Exit")
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import time
import json
import sys
import re
import pymysql

se = requests.Session()  # 模拟登陆
requests.adapters.DEFAULT_RETRIES = 15
se.mount('http://', HTTPAdapter(max_retries=3))  # 重联
se.mount('https://', HTTPAdapter(max_retries=3))


class Pixiv(object):

    def __init__(self):
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.search_url = 'https://www.pixiv.net/search.php?s_mode=s_tag&word='
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
        self.get_number = 10
        self.searchword = ''
        self.mark = 0
        self.pages = '&order=date_d&p='
        self.page = 1
        self.temp_number = 0

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

    def search(self):
        self.searchword = str(sys.argv[1])  # 搜索关键词
        self.mark = str(sys.argv[2])  # 赞数设置
        if (self.mark.isdigit()):
            if int(self.mark) > 20000 or int(self.mark) < 1:
                print("输入数字不合法,程序自动结束")
                sys.exit()
        elif (self.mark == ''):
            self.mark = 1000
        else:
            print("输入格式不合法,程序自动结束")
            sys.exit()
        self.get_number = str(sys.argv[3])  # 获取图片数
        if (self.get_number.isdigit()):
            if int(self.get_number) > 10 or int(self.get_number) < 1:
                print("输入数字不合法,程序自动结束")
                sys.exit()
        elif (self.get_number == ''):
            self.get_number = 3
        else:
            print("输入格式不合法,程序自动结束")
            sys.exit()
        self.page = input("Start with page:(0~100)")
        if (self.page.isdigit()):
            if int(self.page) > 100 or int(self.page) < 1:
                print("输入数字不合法,程序自动结束")
                sys.exit()
        elif (self.page == ''):
            self.page = 1
        else:
            print("输入格式不合法,程序自动结束")
            sys.exit()
        self.page = int(self.page)

    def validateTitle(self,title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

    def sbeautifulsoup(self):
        s = se.get(self.search_url + self.searchword + self.pages + str(self.page))
        self.page += 1
        soup = BeautifulSoup(s.text, features="html.parser")  # 初始化
        # 数据库操作
        db = pymysql.connect("localhost", "root", "PlanetarAntimony", "Study")
        cursor = db.cursor()
        # with open(self.load_path + 'Re_soup.html', 'w', encoding='utf-8') as f:
        #     f.write(soup.prettify())  # 保存soup以便check
        texts = soup.find_all("input", attrs={'data-items': True})
        text = texts[0]['data-items']
        # print(text)
        list = json.loads(text)
        src_headers = self.headers
        for i in list:
            if self.temp_number >= int(self.get_number):
                break
            # print(i['url'])  # 缩略图地址
            # print(i['bookmarkCount'])
            if (i['bookmarkCount'] >= int(self.mark)):
                #print(i['bookmarkCount'])
                pic_id = j["data-id"]  # 图片id
                temp_url = self.target_url + i['illustId']
                # print(temp_url)  # 详细页的url
                temp_clear = se.get(temp_url, headers=src_headers)
                clear_soup = BeautifulSoup(temp_clear.text, features="html.parser")
                title = self.validateTitle(i['illustTitle'])
                # with open(self.load_path + title + '.html', 'w', encoding='utf-8') as f:
                #     f.write(clear_soup.prettify())
                op = clear_soup.prettify().find('"original":"')
                ed = clear_soup.prettify().find('},"tags')
                # print(op)
                # print(ed)
                original_url = clear_soup.prettify()[op + 12:ed - 1]
                # print(original_url)
                adapt_url = original_url.replace('\/', '/')
                # print(adapt_url)  # 高清图地址
                img = se.get(adapt_url, headers=src_headers)
                # 命名格式：mark_date_number.jpg
                dlname = i['bookmarkCount'] + '_page' + str(self.page) +time.strftime("%Y-%m-%d", time.localtime()) + '_' + str(self.temp_number) + '.jpg'
                local_url='http://study.imoe.club/Try/search_pic/' + dlname
                with open(self.load_path + title + '.jpg', 'wb') as f:  # 图片要用b,对text要合法化处理
                    f.write(img.content)  # 保存图片
                print("Downloaded")
                sql = "INSERT INTO pixiv_search(searchword,number,raw_url, pixiv_id,original_url,local_url,title, page) VALUES ('%s','%s','%s', '%s','%s','%s','%s', '%s')" % \
                  (str(self.searchword),str(self.temp_number),str(pic_dl_url), pic_id, str(adapt_url), str(local_url), name, str(self.page))
                # 执行sql语句
                cursor.execute(sql)
                db.commit()
                self.temp_number += 1
                time.sleep(2)
            time.sleep(1)

            # 获取缩略图
            # i = 0  # 命名需要
            # for i in list:
            #     if temp_number >= self.get_number:
            #         break
            #     img = requests.get(i['url'], headers=src_headers)  # 下载图片
            #     with open(self.load_path + i['illustTitle'] + '.jpg', 'wb') as f:  # 图片要用b,对text要合法化处理
            #         f.write(img.content)  # 保存图片
            #     i += 1
            # print("Read.")


if __name__ == '__main__':
    pixiv = Pixiv()
    print("Checking permissions...")
    pixiv.login()
    # print("Loggin")
    print("Welcome!")
    pixiv.search()
    print("Linking to the sever...")
    while pixiv.temp_number < int(pixiv.get_number):
        print("Getting content of page " + str(pixiv.page))
        pixiv.secontect()
        pixiv.sbeautifulsoup()
        if (pixiv.page >= 100):
            break
    print("System Exit")
