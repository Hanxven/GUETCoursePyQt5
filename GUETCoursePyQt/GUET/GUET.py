# coding: utf-8
# 专门用于访问GUET教务系统的各种工具
import json
import time

import requests

GUET_URL = 'http://bkjw.guet.edu.cn'  # domain
VALIDATE = '/login/GetValidateCode'  # GET
SUBMIT_LOGIN = '/Login/SubmitLogin'  # POST
INFO = '/Student/GetPerson'  # POST
CURRENT_TERM = '/Comm/CurTerm'  # POST
SELECTED_COURSES = '/student/GetSctCourse'  # GET


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
    类, 维持了一个session
    注意, 不是线程安全的, 注意同一时间仅能由一个线程访问.
    """

    def __init__(self):
        self.isLogin = False
        self.s = requests.session()
        self.settings = {
            'timeout': 5
        }

    def setSettings(self, val: dict):
        self.settings = val

    def getValidationCode(self) -> bytes:
        """
        获取验证码, 返回bytes格式的内容
        :return: binary stream of validate code image
        """
        url = GUET_URL + VALIDATE
        r = self.s.get(url, timeout=self.settings['timeout'])
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
        }, timeout=self.settings['timeout'])
        resp: dict = json.loads(r.text)
        if resp['success']:
            self.isLogin = True
        return resp

    def getPersonInfo(self) -> dict:
        """
        获得学生信息, 需要登录
        :return: 用户数据字典
        """
        url = GUET_URL + INFO
        r = self.s.post(url, headers=GENERAL_HEADERS, timeout=self.settings['timeout'])
        resp: dict = json.loads(r.text)
        return resp

    def getCurrentTerm(self) -> dict:
        """
        获取当前学期
        data: list, 学期
        :return: 当前学期
        """
        url = GUET_URL + CURRENT_TERM
        r = self.s.post(url, headers=GENERAL_HEADERS, timeout=self.settings['timeout'])
        resp = json.loads(r.text)
        # 保证返回值为字典
        if isinstance(resp, list):
            resp = {'data': resp}
        return resp

    def getSelectedCourses(self, term: str) -> dict:
        """
        返回已选课程
        :param term: 指定学期
        :return: 已选课程字典
        """
        url = GUET_URL + SELECTED_COURSES
        params = {
            '_dc': str(round(time.time() * 1e3)),  # 当前毫秒时间戳
            'comm': '1@1',  # 未知
            'term': term,  # 学期, 如果错误, 则无数据
            'page': 1,
            'start': 0,
            'limit': 100
        }
        r = self.s.get(url, headers=GENERAL_HEADERS, params=params, timeout=self.settings['timeout'])
        resp: dict = json.loads(r.text)
        return resp

    def setControlsState(self):
        # 设置各种控件的显示方式, 统一更改
        ...

    def closeSession(self):
        """关闭会话"""
        self.s.close()


if __name__ == '__main__':
    print(str(round(time.time() * 1e3)))
