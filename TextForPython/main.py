from fake_useragent import UserAgent
import requests
from lxml import etree
import youtube_dl
from concurrent import futures
import pymongo

NUM = 0  # 计数


def index_url():
    for page in range(1, 53):
        url = 'https://www.pornhub.com/video/search?search=%E4%BA%9A%E6%B4%B2&page=' + str(page)
        yield url


def get_pageUrl(url):
    ua = UserAgent()
    headers = {
        'UserAgent': ua.random
    }
    try:
        res = requests.get(url, headers=headers)
        html = etree.HTML(res.text)
        hrefs = html.xpath('//li[@class=" js-pop videoblock videoBox"]/div/div[3]/span/a/@href')
        titles = html.xpath('//li[@class=" js-pop videoblock videoBox"]/div/div[3]/span/a/@title')
        for href, title in zip(hrefs, titles):
            data = {}
            result = 'https://www.pornhub.com' + href
            data['title'] = title
            data['url'] = result
            yield data
    except:
        return None


def download(url):
    global NUM
    '''
    path = 'E:/视频/'
    print('[*]正在下载:' + data['title'][:5])
    ydl_opts = {
        'outtmpl': path

    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    ydl.download([data['url']])
    NUM += 1
    print('[+]下载成功:' + data['title'][:5])
    '''
    path = 'E:/视频'
    print('[*]正在下载:' + url)

    ydl = youtube_dl.YoutubeDL()
    ydl.download([url])
    NUM += 1
    print('[+]下载成功:' + url)


def main():
    global NUM
    client = pymongo.MongoClient(host='localhost')
    db = client['python']
    collection = db['pornhub']

    ex = futures.ThreadPoolExecutor(max_workers=50)
    for i in index_url():
        datas = get_pageUrl(i)
        if datas:
            for data in datas:
                ex.submit(download, data)
            if NUM == 50:
                break

ex = futures.ThreadPoolExecutor(max_workers=50)
for i in open('list.txt','r').readlines():
    url = i.replace('\n','')
    ex.submit(download,url)