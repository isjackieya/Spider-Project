# !/usr/bin/python
# --*-- coding:utf-8 --*--
import requests
import os
import time
import json


class login():
    def __init__(self, username, passwd, Operators_id, user_ip):
        self.ping_result = self.ping()
        print(self.ping())
        if self.ping_result != 0:
            dic = self.login(username, passwd, Operators_id, user_ip)
            if dic != None:
                for i in list(dic.keys()):
                    if dic[i]:
                        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' ' + i + ":" + str(
                            dic[i]))
        elif self.ping_result == 0:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' info:网络正常！')

    def ping(self):
        domain = 'www.baidu.com'
        flag = os.system('ping -n 1 -w 1 %s' % domain)
        return flag

    def login(self, username, passwd, operater_id, user_ip):
        url = "http://10.255.255.34/api/v1/login"
        headers = {
            "Referer": "http://10.255.255.34/authentication/login",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/100.0.4896.75 Safari/537.36",
        }
        payload1 = {
            "username": username,
            "password": passwd,
            "pagesign": "secondauth",
            "ifautologin": "1",
            "channel": operater_id,
            "usripadd": user_ip}
        # 注意，需要去掉json字符串当中的空格，否则后面状态码会是201
        data = json.dumps(payload1).replace(" ", "")
        print(data)
        try:
            r = requests.post(url, data=data, headers=headers, )
            print(r.status_code)
            r.raise_for_status()
            return r.json()
        except:
            print('网络断开或出现异常！！')


if __name__ == '__main__':
    while 1:
        # 下面输入你的账号、密码以及在nuist校园内网的ip，运营商：{移动用户：CMCC  联通用户：Unicom  电信用户：ChinaNet}，根据自己的情况选择
        Operators_dict = {
            "CMCC": "2",
            "ChinaNet": "3",
            "Unicom": "4"
        }
        username = ""
        passwd = ""
        user_ip = ""
        login(username, passwd, Operators_dict['Unicom'], user_ip)  # 需要用户名
        time.sleep(180)  # 每隔3分钟查看网络连接
