import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import sys

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
        self.load_path = './id_pic/'  # 存放图片路径


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
        # 获取原图url
        temp_url = self.target_url+pixiv_id
        temp_clear = se.get(temp_url, headers=self.headers)
        clear_soup = BeautifulSoup(temp_clear.text, features="html.parser")
        #name = self.validateTitle(title[i].text)  # 图片名称
        op = clear_soup.prettify().find('"original":"')
        ed = clear_soup.prettify().find('},"tags')
        original_url = clear_soup.prettify()[op + 12:ed - 1]
        adapt_url = original_url.replace('\/', '/')
        img = se.get(adapt_url, headers=self.headers)
        with open(self.load_path + pixiv_id + '.jpg', 'wb') as f:  # 图片要用b,对text要合法化处理
            f.write(img.content)  # 保存图片


if __name__ == '__main__':
    pixiv = Pixiv()
    pixiv.login()
    pixiv.download()
    print("System Exit")
