# coding: utf-8
# 专门用于访问GUET教务系统的各种工具
import json

import requests

GUET_URL = 'http://bkjw.guet.edu.cn'
VALIDATE_URL = '/login/GetValidateCode'  # GET
SUBMIT_LOGIN = '/Login/SubmitLogin'  # POST
INFO_URL = '/Student/GetPerson'  # POST

GENERAL_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'bkjw.guet.edu.cn',
    'Origin': 'http://bkjw.guet.edu.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://bkjw.guet.edu.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59',
    'X-Requested-With': 'XMLHttpRequest'
}


class GUET:
    """
    类, 维持了一个回话
    """
    def __init__(self):
        self.isLogin = False
        self.s = requests.session()

    def getValidationCode(self) -> bytes:
        """
        :return: binary stream of validate code image
        """
        url = GUET_URL + VALIDATE_URL
        r = self.s.get(url)
        return r.content

    def submitLogin(self, account, password, validationCode) -> dict:
        """
        登录到教务系统
        :param account: 用户名
        :param password: 密码
        :param validationCode: 验证码
        :return: 登录信息, 非必要
        """
        url = GUET_URL + SUBMIT_LOGIN
        r = self.s.post(url, headers=GENERAL_HEADERS, params={
            'us': account,
            'pwd': password,
            'ck': validationCode
        })
        resp: dict = json.loads(r.text)
        if resp['success']:
            self.isLogin = True
        return resp

    def getPersonInfo(self) -> dict:
        """
        会获得用户信息
        :return: 用户数据字典
        """
        url = GUET_URL + INFO_URL
        r = self.s.post(url, headers=GENERAL_HEADERS)
        resp: dict = json.loads(r.text)
        return resp


if __name__ == '__main__':
    g = GUET()
    gr = g.submitLogin('1900301037', '3092599', '7216')
    print(gr)
