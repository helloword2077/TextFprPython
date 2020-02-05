import requests
from concurrent import futures
from lxml import etree
import threading
import os

"""
爬取视频流ts文件
"""
def getIndexUrl():
    data = {}
    url = 'http://www.tlula600.com/vodlist/5.html'
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    html = etree.HTML(res.text)
    url_data = html.xpath('//*[@id="allright"]/div[9]/div[2]/div/ul/li[*]/a/@href')
    url_name = html.xpath('//*[@id="allright"]/div[9]/div[2]/div/ul/li[*]/a/h3/text()')
    for i in range(len(url_data)):
        data[url_name[i]] = 'http://www.tlula600.com' + url_data[i]
    print('[+]成功获取页面url地址')
    return data


def getUrl(url):
    res = requests.get(url)
    html = etree.HTML(res.text)
    data = html.xpath('//*[@id="dyplayer"]/script[1]/text()')[0].split(',')[6].replace('\\', '').replace(
        "http://sd.52avhd.com:9888/", 'https://hd1.o0omvo0o.com/').replace('\"', '')
    print('[+]成功获取m3u8地址')
    return data


def getM3U8(url_form3u8, name):
    res = requests.get(url_form3u8)

    with open("m3u8/{}.m3u8".format(name), 'w+') as f:
        f.write(res.text)
    print('[+]下载m3u8文件成功：' + name)


def getM3U8_Data(name):
    data = []
    ts = open("m3u8/{}.m3u8".format(name), 'r').readlines()
    for i in ts:
        if i.find('out') >= 0:
            data.append(i.replace('\n', ''))
    return data


def getTs(url, ts,name):
    try:
        os.mkdir('test/'+name)
    except:
        pass
    url = url.replace('playlist.m3u8', '') + ts
    res = requests.get(url)
    with open('test/{}/{}'.format(name,ts), 'w+b') as f:
        f.write(res.content)
    print('{}下载成功'.format(ts))


#
# for i in getM3U8_Data():
#     ex.map(getTs,i)

def m3u8_main():
    ex = futures.ThreadPoolExecutor(max_workers=200)
    urls = getIndexUrl()
    # for name in urls:
    #         url_m3u8=getUrl(urls[name])
    #         # getM3U8(url_m3u8,name[:10])
    #         ex.submit(getM3U8,url_m3u8,name[:-4])
    for name in urls:
        tss = getM3U8_Data(name[:-4])
        url = getUrl(urls[name])
        for ts in tss:
            ex.submit(getTs, url,ts,name)

m3u8_main()
