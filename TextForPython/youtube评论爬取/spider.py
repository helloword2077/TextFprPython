import requests

YOUTUBE_LINK = 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=%E6%AD%A6%E6%B1%89&maxResults=50&&key={key}'
YOUTUBE_IN_LINK = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&nextPageToken={nextPageToken}&q=%E6%AD%A6%E6%B1%89&&key={key}'
#key = 


def index_page():
    res = requests.get(YOUTUBE_LINK.format(key=key))
    res_info = res.json()
    for i in res_info['items']:
        id = i['id']['videoId']
        with open('videoId.txt', 'a+') as f:
            f.write(id)
            f.write('\n')
        print('成功写入---' + id)


index_page()
