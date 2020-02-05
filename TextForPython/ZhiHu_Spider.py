from selenium import webdriver
from time import sleep
import re
import requests
from concurrent import futures
import os

driver = webdriver.Chrome()
"""
爬取知乎图片，并配合1.9.1的百度api给妹子颜值打分

"""

def getImgUrl(driver):
    print('[*]==打开网页中==')
    url = 'https://www.zhihu.com/question/30210517'
    driver.get(url)
    print('[+]==打开成功==')
    sleep(1)
    for i in range(100):
        print('[*]正在获取所有值..')
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight-100)")
    print('[+]获取完毕，正在获取url')
    f1 = driver.find_elements_by_xpath(
        '//*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div/div[*]/div/div[2]/div[1]/span/figure[*]')
    for i in f1:
        html = i.get_attribute('innerHTML')
        img_url = re.search('https://(.*?).jpg', html).group()
        print('[*]成功获取url:{}'.format(img_url))
        yield img_url


def downloadImg(url, k):
    res = requests.get(url)
    print('[*]正在下载{}'.format(k))
    with open('imgForZhiHu/img/{}.jpg'.format(k), 'w+b') as f:
        f.write(res.content)
    print('[+]下载成功{}'.format(k))


def main(driver):
    ex = futures.ThreadPoolExecutor(max_workers=50)

    k = 0
    for i in getImgUrl(driver):
        ex.submit(downloadImg, i, k)
        k += 1
    driver.close()


main(driver)
