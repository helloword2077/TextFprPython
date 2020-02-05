import PIL.ExifTags
from PIL import Image
import argparse

parse = argparse.ArgumentParser()
parse.add_argument('-i', help="图片存放位置")
parse.add_argument('-a', action='store_true', help="输出图片全部信息")
parse.add_argument('-s','--show', action='store_true', help="查看基本信息")
parse.add_argument('-f',help="保存到文件")
args = parse.parse_args()


def getGps(gps):
    deg = float(gps[2][0][0]) / float(gps[2][0][1])
    min = float(gps[2][1][0]) / float(gps[2][1][1]) / 60
    sec = float(gps[2][2][0]) / float(gps[2][2][1]) / 3600

    deg1 = float(gps[4][0][0]) / float(gps[4][0][1])
    min1 = float(gps[4][1][0]) / float(gps[4][1][1]) / 60
    sec1 = float(gps[4][2][0]) / float(gps[4][2][1]) / 3600
    return deg + min + sec, deg1 + min1 + sec1


def get_exif(fn):
    try:
        img = Image.open(fn)
        exif = {PIL.ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
                if k in PIL.ExifTags.TAGS
                }

        for i in exif:
            if type(exif[i]) == bytes:
                try:
                    flag = exif[i].decode("utf-8")
                except:
                    pass
                exif[i] = flag
        # print(exif)

        GPS = exif['GPSInfo']
        GPS = getGps(GPS)
        data = {
            "拍摄日期": exif['DateTime'],
            "拍摄设备": exif['Make'],
            "地址信息": GPS

        }
        if args.show:
            print(data)
        if args.a:
            print(exif)
        if args.f:
            with open(args.f,'w+') as f:
                f.write(str(exif))
    except:
        print("未发现信息，输入-h查看帮助")


get_exif(args.i)
