from selenium import webdriver
import csv
import time


def chromedriver():
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    options.add_experimental_option('prefs', prefs)  # 不加载图片
    options.add_experimental_option('excludeSwitches',
                                    ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    options.add_argument("--disable-blink-features=AutomationControlled")  # 禁用启用Blink运行时的功能
    browser = webdriver.Chrome(r"F:\pachong\冰墩墩\chromedriver.exe", options=options)
    browser.maximize_window()
    return browser
    pass


# 有iframe的登录框
def login1(driver, username, passwd):
    driver.implicitly_wait(10)
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="J_loginIframe"]'))
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(passwd)
    time.sleep(3)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
    driver.switch_to.default_content()


# 没有iframe的登录框
def login2(driver, username, passwd):
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(passwd)
    driver.implicitly_wait(10)
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()


# 开始获取数据
def get_data(driver):
    dict = {};
    time.sleep(3)
    driver.implicitly_wait(5)
    product_name = driver.find_element_by_xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[1]/h1').text
    dict["产品名称"] = product_name
    product_price = driver.find_element_by_xpath('//dd/span[@class="tm-price"]').text
    dict["产品价格"] = product_price
    product_sales = driver.find_elements_by_xpath('//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]')
    if len(product_sales):
        dict["销量"] = product_sales[0].text
    else:
        dict["销量"] = "Null,该商品已下架"
    product_popularity = driver.find_element_by_xpath('//*[@id="J_CollectCount"]').text
    dict["人气"] = product_popularity
    driver.implicitly_wait(20)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="J_TabBar"]/li[2]/a').click()
    time.sleep(2)
    driver.implicitly_wait(3)
    dict["关键词"] = []
    keyword_list = driver.find_elements_by_xpath(
        '/html/body/div[5]/div/div[4]/div/div[1]/div/div[10]/div[1]/div/div[1]/div[3]/div[2]/div/span/a')

    driver.implicitly_wait(5)
    for keyword in keyword_list:
        if keyword.text:
            dict["关键词"].append(keyword.text)
        else:
            dict["关键词"].append("Null")
            break
    comment_list = driver.find_elements_by_xpath('//*[@id="J_Reviews"]/div/div[6]/table/tbody/tr/td[1]/div[1]/div[1]')
    if len(comment_list):
        f2.write("商品:" + product_name + '   的评论列表：\n')
    else:
        f2.write("商品:" + product_name + "的评论列表为空\n")
        f2.write("------------------------------------------------------------------------\n")
    for comment in comment_list:
        f2.write(comment.text + '\n')
        f2.write("************************************************************************\n")
    f2.write("------------------------------------------------------------------------\n")
    time.sleep(1)
    writer.writerow(dict)


if __name__ == '__main__':
    url = "https://theolympicstore.tmall.com/index.htm?spm=a220o.1000855.w5002-17469162993.2.73a52e89Ylz63C"
    username = input("请输入淘宝用户名")  # 用户名
    passwd = input("请输入淘宝密码")  # 密码
    driver = chromedriver()
    driver.get(url)
    url_list = driver.find_elements_by_xpath('//div[@class="main-wrap J_TRegion"]/div[@class="J_TModule"]//area')
    header = ["产品名称", "产品价格", "销量", "人气", "关键词"]
    with open("bingdundun.csv", "w", encoding="utf-8", newline="") as f1, open("comment.txt", "w",
                                                                               encoding="utf-8") as f2:
        writer = csv.DictWriter(f1, fieldnames=header)
        writer.writeheader()
        f2.write("------------------------------------------------------------------------\n")
        for url in url_list:
            url = url.get_attribute("href")
            print(url)
            js = "window.open('%s')" % (url)
            driver.execute_script(js)
            driver.switch_to.window(driver.window_handles[1])
            frame = driver.find_elements_by_xpath("/html/body/div[10]/div[2]/iframe")
            if u"天猫tmall.com--理想生活上天猫" in driver.title:
                login2(driver, username, passwd)
            elif len(frame):
                login1(driver, username, passwd)
            time.sleep(3)
            get_data(driver)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        driver.quit()
