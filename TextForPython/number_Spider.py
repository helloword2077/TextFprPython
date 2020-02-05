from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import sys

num = 1
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(chrome_options=chrome_options)

driver=webdriver.PhantomJS()

def get_number(page=1):
    numbers = {}
    k = 1
    url = "https://www.materialtools.com/?page=%d" % (page)
    driver.get(url)
    for i in range(14):
        try:
            flag = driver.find_element_by_xpath('/html/body/article/section/div[1]/div[{}]/div[2]/div/small/em'.format(i))
            # /html/body/article/section/div[1]/div[2]/div[2]/div/small/em
            # /html/body/article/section/div[1]/div[5]
            if flag.text == '+86':
                number = flag.find_element_by_xpath("../../h3").text
                data = {
                    number: k + (page - 1) * 10
                }
                numbers.update(data)
        except:
            pass

        finally:
            k+=1


    return numbers


def get_Message(flag):
    print("[*]正在获取信息中")
    url = "https://www.materialtools.com/SMSContent/{}".format(flag)
    driver.get(url)
    while True:
        print("[+]获取成功")
        print("[+]这是你查看#{}下的内容".format(flag))
        print("==================================")
        msgs = driver.find_elements_by_xpath("/html/body/article/section[2]/div/div[2]/table/tbody/tr")
        for msg in msgs:
            print(msg.text)
            print("================")
        print("==================================")
        print("[*]没有找到？输入>>refresh 来刷新页面")
        print("[*]如果找到输入>>exit 退出")
        com = input(">>")
        if com == 'refresh':
            driver.refresh()
        elif com == 'exit':
            return 0


def main():
    global num
    while True:
        print("[*]正在获取第{}页的手机号...".format(num))
        numbers = get_number(num)

        print("[+]获取成功")
        print("===================")

        for i in numbers:
            print("{}-{}".format(numbers[i], i))
        print("===================")
        print("[*]请输入选择的号码的编号")
        print("[*]输入>>next获取下一页")
        print("[*]输入>>exit退出")
        flag = input(">>")
        if flag == 'next':
            num += 1
            if num == 14:
                print("这是最后一页")
            continue
        elif flag == 'exit':
            print('[+]谢谢使用')
            sys.exit(0)
        fg = get_Message(flag)
        if fg == 0:
            continue


main()
