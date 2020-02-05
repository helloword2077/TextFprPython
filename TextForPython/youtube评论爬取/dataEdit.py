import pymongo
from aip import AipNlp
from matplotlib import pyplot
from time import sleep


APP_ID = 
API_KEY = 
SELECT_KEY = 

client = pymongo.MongoClient(host='localhost')
db = client['python']
collection = db['youtube']

client = AipNlp(APP_ID, API_KEY, SELECT_KEY)
POS_NUM = 0  # 积极的计数
NEG_NUM = 0  # 消极的计数
for i in collection.find():
    with open('a.txt','a+') as f:
        try:
            f.write(i['comment'])
        except:
            pass


