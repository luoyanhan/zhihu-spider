import requests
import re
import random
import time

class xici_spider(object):
    def __init__(self):
        self.HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
        'Connection': 'keep-alive'
        }
        self.urls = [
            'http://www.xicidaili.com/nt/',
            'http://www.xicidaili.com/nn/',
            'http://www.xicidaili.com/wn/',
            'http://www.xicidaili.com/wt/'
        ]

    def get_proxy(self, url):
        res = requests.get(url, headers=self.HEADER)
        flag = 1
        while res.status_code != 200:
            res = requests.get(url, headers=self.HEADER)
            time.sleep(random.randint(0, 5))
            flag += 1
            if flag > 3:
                break
        if res.status_code == 200:
            tbody = re.search(r'<table id="ip_list">([\s\S]*?)</table>', res.text).group()
            trs = re.findall(r'<tr([\s\S]*?)</tr>', tbody)
            for i in range(1, len(trs)):
                tds = re.findall(r'<td>([\s\S]*?)</td>', trs[i])
                proxy, port, type = tds[0], tds[1], tds[3]
                if type == 'HTTP':
                    pro = {'http': 'http://' + proxy + ':' + port}
                else:
                    pro = {'https': 'https://' + proxy + ':' + port}
                try:
                    req = requests.get('http://www.163.com', proxies=pro, headers=self.HEADER, timeout=1)
                    print(pro)
                    if req.status_code == 200:
                       print(pro)
                except Exception:
                    continue

    def main(self):
        self.get_proxy('http://www.xicidaili.com/nt/')
        for U in self.urls:
            for i in range(1, 2):
                url = U + str(i)
                self.get_proxy(url)


if __name__ == "__main__":
    daili = xici_spider()
    daili.main()


