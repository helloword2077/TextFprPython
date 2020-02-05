import requests
import pymongo
from concurrent import futures
from time import sleep


YOUTUBE_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&videoId={}&key={}'
YOUTUBE_IN_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&pageToken={nextPageToken}&videoId={videoId}&key={key}'
key = 
client = pymongo.MongoClient(host='localhost')
db = client['python']
collection = db['youtube']

def get_comment(videoId):
    count = 200
    co = 0
    try:
        res = requests.get(YOUTUBE_LINK.format(videoId, key))
        res_info = res.json()

        while 'nextPageToken' in res_info:
            res = requests.get(YOUTUBE_IN_LINK.format(nextPageToken=res_info['nextPageToken'], videoId=videoId, key=key))
            res_info = res.json()
            if res.status_code != 200:
               pass

            for item in res_info['items']:
                text = {}
                data = item['snippet']['topLevelComment']['snippet']
                text['name'] = data['authorDisplayName']
                text['comment'] = data['textOriginal']
                text['likeCount'] = data['likeCount']
                text['time'] = data['publishedAt']
                text['videoId'] = data['videoId']
                co += 1
                if co == count:
                    break
                collection.insert(text)
    except Exception as e:
        print(e)
        with open('log.txt','a+') as f:
            f.write('----')
            f.write(videoId)
            f.write('\n')


def main():
    ex = futures.ThreadPoolExecutor(max_workers=50)
    ids = open('videoId.txt','r').readlines()
    for id in ids:

        id_info = id.replace('\n','')
        ex.submit(get_comment,id)
        print('[*]正在爬取:', id_info)

main()


