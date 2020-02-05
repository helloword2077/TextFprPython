import requests
import json
from bs4 import BeautifulSoup
from concurrent import futures

"""
网易云歌单爬取
"""
def getcomments(musicid):
    url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=09acec287fc11ba45ea7d2605953e084'.format(musicid)
    payload = {
        'params': '4hmFbT9ZucQPTM8ly/UA60NYH1tpyzhHOx04qzjEh3hU1597xh7pBOjRILfbjNZHqzzGby5ExblBpOdDLJxOAk4hBVy5/XNwobA+JTFPiumSmVYBRFpizkWHgCGO+OWiuaNPVlmr9m8UI7tJv0+NJoLUy0D6jd+DnIgcVJlIQDmkvfHbQr/i9Sy+SNSt6Ltq',
        'encSecKey': 'a2c2e57baee7ca16598c9d027494f40fbd228f0288d48b304feec0c52497511e191f42dfc3e9040b9bb40a9857fa3f963c6a410b8a2a24eea02e66f3133fcb8dbfcb1d9a5d7ff1680c310a32f05db83ec920e64692a7803b2b5d7f99b14abf33cfa7edc3e57b1379648d25b3e4a9cab62c1b3a68a4d015abedcd1bb7e868b676'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        'Referer': 'http://music.163.com/song?id={}'.format(musicid),
        'Host': 'music.163.com',
        'Origin': 'http://music.163.com'
    }

    response = requests.post(url=url, headers=headers, data=payload)
    data = json.loads(response.text)
    hotcomments = []
    for hotcomment in data['hotComments']:
        item = {
            'nickname': hotcomment['user']['nickname'],
            'content': hotcomment['content'],
            'likes' : hotcomment['likedCount']
        }
        hotcomments.append(item)

    # return  hotcomments
    # 返回热门评论
    return [content['content'] for content in hotcomments]



def get_song(url):
    new_url = url.replace('/#', '')

    header = {
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
    }

    res = requests.get(new_url, headers=header).text

    r = BeautifulSoup(res, "html.parser")
    music_dict = {}
    result = r.find('ul', {'class', 'f-hide'}).find_all('a')
    for music in result:
        music_id = music.get('href').strip('/song?id=')
        music_name = music.text
        music_dict[music_id] = music_name
    return music_dict


def comments_write(texts):
    with open('网易云评论.txt','a+') as f:
        for i in texts:
            try:
                f.write(i)
                f.write('\n')
            except:
                continue


if __name__ == '__main__':
    # i=input('请输入网易云歌单地址：')
    i='https://music.163.com/#/playlist?id=49242031'
    a=get_song(i)
    for i in a:
        ac=getcomments(i)
        comments_write(ac)
