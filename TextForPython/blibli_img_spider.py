import requests
import json
from concurrent import futures
from tqdm import trange

def main():
    ex=futures.ThreadPoolExecutor(max_workers=50)
    for i in trange(1,152):
        url="https://api.bilibili.com/pgc/season/index/result?season_version=-1&" \
            "area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&" \
            "page={}&" \
            "season_type=1&pagesize=20&type=1".format(i)
        ex.submit(index_page,url)

def index_page(url):
    res=requests.get(url)
    res.encoding=res.apparent_encoding
    next_page(res.text)

def next_page(html):
    data=json.loads(html)
    for i in data['data']['list']:
        img_url=i['cover']
        img_name=i['title']
        # print(img_name)
        get_img(img_url,img_name)

def get_img(img_url,img_name):
    img=requests.get(img_url)
    with open('img/{}.jpg'.format(img_name),'w+b') as f:
        f.write(img.content)
main()