"""
进入好友空间
登录
爬数据
翻页
爬数据

https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=1686507126&ftype=0&sort=0&pos=0&num=20&replynum=100&g_tk=1021576395&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1&qzonetoken=0585a382f127abd96120e77e4dca1f673f0dd6c3173967890ddd640b7915c2f441666e862055e7b3eb4c&g_tk=1021576395

"""
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import re
import requests
from concurrent import futures


"""
qq空间好友说说爬取

"""
global flags
flags = True



def get_g_tk(cookie):
    hashes = 5381
    for letter in cookie['p_skey']:
        hashes += (hashes << 5) + ord(letter)  # ord()是用来返回字符的ascii码
    return hashes & 0x7fffffff


def login(driver, qq):#登录需要电脑版qq
    driver.get('https://user.qzone.qq.com/{}/311'.format(qq))
    time.sleep(2)
    try:
        driver.find_element_by_id('login_div')
        login_div_exit = True
    except:
        login_div_exit = False
    if login_div_exit:
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('').click()
    time.sleep(3)


def getOneQq(driver, qq):
    html = driver.page_source
    html_data = BeautifulSoup(html, 'lxml')
    cookie = {}  # 初始化cookie字典
    for elem in driver.get_cookies():  # 取cookies
        cookie[elem['name']] = elem['value']
    g_tk = get_g_tk(cookie)
    g_qzonetoken = ''
    for ib in range(4000):
        n=ib*20
        param = {
            'uin': qq,
            'ftype': '0',
            'sort': '0',
            'pos': n,
            'num': '20',
            'replynum': '100',
            'g_tk': [g_tk, g_tk],
            'callback': '_preloadCallback',
            'code_version': '1',
            'format': 'jsonp',
            'need_private_comment': '1',
            'qzonetoken': g_qzonetoken
        }
        url = 'htps://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={}&ftype=0&sort=0&pos=0&num=20&replynum=100&g_tk={}&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1&qzonetoken={}&g_tk={}'.format(
            qq, g_tk, g_qzonetoken, g_tk)
        try:
            res = requests.get('https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6'
                               , params=param, cookies=cookie)
            r = re.sub("_preloadCallback", "", res.text)
            test = r[1:-2]
            Data = json.loads(test)
            if Data['message'] == '对不起,主人设置了保密,您没有权限查看':
                print('{}没有权限'.format(qq))
                break
            else:
                if not re.search('lbs', test):
                    print('%s说说下载完成' % qq)
                    break
                else:
                    with open('qq/{}.json'.format(qq), 'a+') as f:
                        f.write(json.dumps(Data))
                        f.write('\n')
                        print('{}第{}个，完成'.format(qq,ib))
        except Exception as e:
            print(e)


def main():
    driver = webdriver.Chrome()
    qq = open('qq_number.txt').readlines()#读取qq联系人文件

    ex = futures.ThreadPoolExecutor(50)
    for i in qq:
        d=i.replace('\n','')
        login(driver, d)
        ex.submit(getOneQq, driver, d)


main()
