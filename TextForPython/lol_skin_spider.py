from concurrent import futures
import requests
from bs4 import BeautifulSoup
ex = futures.ThreadPoolExecutor(max_workers=50)

headers="Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"

def main():
    for i in range(1,44):
        url = "http://lol.52pk.com/pifu/hero/hero_{}.shtml".format(i)
        ex.submit(index_page,url)


def index_page(url):
    res = requests.get(url, headers)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text,'lxml')
    res.close()
    for i in range(1,26):
        try:
            data = soup.select("body > div.ListBigContent > div > div > ul > li:nth-child({}) > a".format(i))[0].attrs
            img_page_url = data['href']
            get_img_page(img_page_url)
        except Exception:
            pass

def get_img_page(img_page_url):
    res = requests.get(img_page_url)
    html = BeautifulSoup(res.text,'lxml')
    img_url = html.select('body > div.pifuShowBox > div.pifuIntroPic.pifuIntroPic2 > img')[0].attrs['src']
    res.close()
    img_res = requests.get(img_url)
    img_name = img_url.split('/')[-1]
    with open('img/{}'.format(img_name),'w+b') as f:
        f.write(img_res.content)

main()
