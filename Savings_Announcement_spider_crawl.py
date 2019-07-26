import requests
import json
from urllib.parse import urlencode
from requests.exceptions import RequestException
import os
import time
def get_page_index(pageNum):
    post_form = {
        'pageNum': pageNum,
        'pageSize': '30',
        'tabName': 'fulltext',
        'column':' szse',
        'stock': '300056',
        'plate': 'sz',
        'seDate': '2016-10-25 ~ 2019-07-26'
    }
    
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Connection': 'keep-alive',
            'Content-Length': '144',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'JSESSIONID=F3F5E3145F10E145E0999B2DEB1124F4'}

    url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    try:
        response = requests.post(url,data=post_form)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print("请求失败")
        
    
    
def parse_page_index(html):
    url = []
    title = []
    data = json.loads(html)
    m = 0
#     if data and 'announcements' in data.keys():
    for item in data.get('announcements'):
        m+=1
        url = 'http://static.cninfo.com.cn/'+item.get('adjunctUrl')
        title = item.get('announcementTitle')
        save_pdf(url,title)
        print('第'+str(m)+'PDF已下载')
#             time.sleep(2)
#         print(url)
            
def download_list():
    a = []
    n = 0
    for i in range (0,24):
        html = get_page_index(i)
        parse_page_index(html)
        n+=1
        print('-------------------------第'+str(n)+'页已提取-----------------')
#         print(html)
#         for url in parse_page_index(html):
#             for (k,v) in  url.items():
#             print(url)
#             print('完成一页解析下载')
         
#             return a
def save_pdf(url,name):
    url = str(url)
#     name = name+'.pdf'
    r = requests.get(url.strip())

    title = '{0}{1}.{2}'.format(name, md5(r.content).hexdigest(), 'pdf')

#     r = requests.get(url.strip())
    with open(title,'wb')as f:
        f.write(r.content)
        f.close()
        print(name+ '  ' +"文件保存成功")            
    
def main():
    download_list()
   
    
if __name__=='__main__':
    main()
    