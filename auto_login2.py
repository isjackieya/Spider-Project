import os.path
import time
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


def chromedriver():
    """
    获得驱动器来自动启动浏览器
    需要将chromedriver.exe放在当前文件所在的目录下
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome('./' + os.sep + 'chromedriver.exe', options=options)
    return browser


def ping(Domain):
    if os.system("ping -n 1 -w 1 %s" % Domain):
        return False
    else:
        return True


def login(username, passwd, option, driver):
    driver.get("http://10.255.255.34/authentication/login")
    driver.implicitly_wait(5)
    uname = driver.find_element_by_css_selector(
        "#login-pc > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > input:nth-child(2)")
    ActionChains(driver).click(uname).send_keys(username).perform()
    password = driver.find_element_by_css_selector("input.ant-input:nth-child(1)")
    ActionChains(driver).click(password).send_keys(passwd).perform()
    time.sleep(1)
    log = driver.find_element_by_css_selector("button.ant-btn:nth-child(5)")
    ActionChains(driver).click(log).perform()
    driver.implicitly_wait(3)
    operator = driver.find_element_by_css_selector("button.col:nth-child(%d)" % option)
    ActionChains(driver).click(operator).perform()
    time.sleep(4)
    if driver.current_url == "http://10.255.255.34/authentication/detail":
        return True
    else:
        return False


if __name__ == '__main__':
    """
    双引号中分别填入自己的用户名和密码
    """
    username = ""
    passwd = ""
    option_dict = {
        "中国移动": 1,
        "中国电信": 2,
        "中国联通": 3
    }
    driver = chromedriver()
    try:
        """
           选择运营商:
           可以根据自己的情况，修改option_dict[""]中括号中的值，
           仅这三个值：中国联通，中国电信，中国移动
        """
        if login(username, passwd, option_dict[""], driver):
            if ping("www.baidu.com"):
                print("成功连接网络")
                ip_addr = driver.find_element_by_css_selector(
                    "div.p:nth-child(3) > div:nth-child(1) > span:nth-child(2)").text
                print("您的IP地址是%s" % ip_addr)
            else:
                print("无法接入网络")
    except:
        print("连接时出现错误!!")
    finally:
        driver.close()
