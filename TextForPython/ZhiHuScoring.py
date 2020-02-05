from baidu.api import AipFace
import base64
import os
import shutil
appid=
client_id=
client_secret=
aipface=AipFace(appid,client_id,client_secret)

def rm():
    print('[*]正在清理损坏img')
    imgPaths = os.listdir('imgForZhiHu/img')
    for imgPath in imgPaths:
        path='imgForZhiHu/img/'+imgPath
        size=os.path.getsize(path)
        if size < 1024:
            os.remove(path)
    print('[+]清理完毕')


def getImgPath():
    paths=os.listdir('imgForZhiHu/img')
    for i in paths:
        yield i

def getImgData():
    imgPaths=getImgPath()
    for imgpath in imgPaths:
        path='imgForZhiHu/img/{}'.format(imgpath)
        with open(path, 'rb') as f:

            imgdata=f.read()

        imgBase=base64.encodebytes(imgdata)
        img=str(imgBase,'utf-8')

        options={
            'max_face_num':1,
            'face_field': "age,beauty"
        }
        result=aipface.detect(img,'BASE64',options)
        try:
            if result['result']:
                print('{}的信息'.format(imgpath))
                age = result['result']['face_list'][0]['age']
                beauty = result['result']['face_list'][0]['beauty']
                print('年龄为',age)
                print('颜值:',beauty)
                print('======================')
                if beauty>70:
                    shutil.copyfile(path,'imgForZhiHu/sss/{}.jpg'.format(imgpath+'颜值'+str(beauty)))

            else:
                print('{}'.format(imgpath))
                print('未发现人脸')
                print('**********************')

        except:
            pass



def main():
    rm()
    imgdata=getImgData()

main()