# coding: utf-8
# 专门用于访问GUET教务系统
import json
import sys
import time
import os
import requests
import logging
from requests.adapters import HTTPAdapter

# APIs 教务系统API 系列
GUET_URL = 'http://bkjw.guet.edu.cn'  # 教务系统域名
VALIDATE_CODE = '/login/GetValidateCode'  # GET 验证码获取
SUBMIT_LOGIN = '/Login/SubmitLogin'  # POST 教务登录
OVERALL_INFO = '/Student/GetPerson'  # POST 学生个人信息
STU_INFO = '/student/StuInfo'  # POST 学生当前学期状态信息
CURRENT_TERM = '/Comm/CurTerm'  # POST 当前学期
SELECTED_COURSES = '/student/GetSctCourse'  # GET 已选课程
SELECT_COURSE = '/student/SctSave'  # POST 提交课程
AVAILABLE_COURSES = '/student/GetPlan'  # GET 可选课程
DROP_COURSE = '/student/UnSct'  # POST 退课
MAJORS = '/Comm/GetSpno'  # 所有专业
DEPARTMENTS = '/Comm/GetDepart'  # 所有专业

# 通用headers
GENERAL_HEADERS: dict[str, str] = {
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
    类, 维持了一个Session连接池
    仅用于访问 {GUET_URL}
    """

    def __init__(self):
        self.isLogin = False
        self.s = requests.Session()

        # init logger
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout
                            , format='%(asctime)s, 进程ID: %(process)s - %(levelname)s: %(message)s, 线程ID: %('
                                     'thread)d')
        logging.getLogger("requests").setLevel(logging.DEBUG)

        # 设定最多24连接, 可增加, 只会重新尝试一次, 且阻塞, 等待可用连接
        self.s.mount('http://', HTTPAdapter(pool_connections=1, pool_maxsize=24, max_retries=1, pool_block=True))

        # 设置项具体 - 未完成功能
        self.settings = {
            'timeout': 5
        }

    # 设置总体超时时间
    def setTimeout(self, val: int):
        self.settings['timeout'] = val

    def getValidationCode(self) -> bytes:
        """
        获取验证码, 返回bytes格式的内容
        :return: binary stream of validate code image
        """
        url = GUET_URL + VALIDATE_CODE
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
        url = GUET_URL + OVERALL_INFO
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

    def getStuInfo(self):
        """
        获得学生当前状态信息
        :return: 状态信息字典
        """
        url = GUET_URL + STU_INFO
        r = self.s.post(url, headers=GENERAL_HEADERS)
        resp: dict = json.loads(r.text)
        return resp

    def getAvailableCourses(self, term: str, grade: str, dptNo: str, majorNo: str, sType: str):
        url = GUET_URL + AVAILABLE_COURSES
        params = {
            '_dc': str(round(time.time() * 1e3)),
            'term': term,
            'grade': grade,
            'dptno': dptNo,
            'spno': majorNo,
            'stype': sType,
            'start': 0,
            'limit': 25,
            'page': 1
        }
        r = self.s.get(url, headers=GENERAL_HEADERS, params=params)
        resp: dict = json.loads(r.text)
        return resp

    def getMajors(self):
        """
        可以获取所有专业, 数据未被归类
        get all majors (uncategorized)
        :return: 数据
        """
        url = GUET_URL + MAJORS
        params = {
            '_dc': str(round(time.time() * 1e3)),
            'page': 1,
            'start': 0,
            'limit': 25,
            'sort': '[{"property":"dptno","direction":"ASC"},{"property":"spno","direction":"ASC"}]'
        }
        r = self.s.get(url, headers=GENERAL_HEADERS, params=params)
        resp: dict = json.loads(r.text)
        return resp

    def getDepartments(self) -> dict:
        url = GUET_URL + DEPARTMENTS
        params = {
            '_dc': self.get_Dc(),
            'page': 1,
            'start': 0,
            'limit': 25
        }
        r = self.s.get(url, headers=GENERAL_HEADERS, params=params)
        resp: dict = json.loads(r.text)
        return resp

    @staticmethod
    def get_Dc() -> str:
        return str(round(time.time() * 1e3))

    def getCookies(self):
        return self.s.cookies

    def closeSession(self):
        """关闭所有会话"""
        self.s.close()


if __name__ == '__main__':
    print(str(round(time.time() * 1e3)))
