import requests
import re
import time
import random
if __name__ == "__main__":
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
        'Connection': 'keep-alive',
        'Host': 'www.kuaidaili.com'
    }
    # pro = {'http': 'http://222.33.192.238:8118'}
    # response = requests.get('http://www.google.com.hk', headers=HEADER, proxies=pro)
    # print(response.status_code)
    response = requests.get('https://www.kuaidaili.com/free/inha/1/', headers=HEADER)
    li = re.search(r'<div id="listnav">([\s\S]*?)</div>', response.text)
    string = re.findall(r'<a(.*?)</a>', li.group(1))
    max_page = string[-1].split('>')[-1]
    for i in range(1, int(max_page)):
        url = r'https://www.kuaidaili.com/free/inha/%c/' % str(i)
        response = requests.get(url, headers=HEADER)
        flag = 1
        while response.status_code != 200:
            response = requests.get(url, headers=HEADER)
            time.sleep(random.randint(0, 5))
            flag += 1
            if flag > 3:
                break
        if response.status_code == 200:
            tbody = re.search(r'<tbody>([\s\S]*?)</tbody>', response.text).group()
            IPS = re.findall(r'<td data-title="IP">(.*?)</td>', tbody)
            PORTS = re.findall(r'<td data-title="PORT">(.*?)</td>', tbody)
            for j in range(len(IPS)):
                pro = {'http': 'http://' + str(IPS[j]) + ':' + str(PORTS[j])}
                try:
                    req = requests.get('http://www.163.com', proxies=pro, headers=HEADER, timeout=2)
                    if req.status_code == 200:
                        print(pro['http'])
                except Exception:
                    continue