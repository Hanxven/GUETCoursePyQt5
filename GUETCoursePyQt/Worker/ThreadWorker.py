from PyQt5.QtCore import *

from GUETCoursePyQt.GUET.GUET import GUET


class HWorker(QObject):
    """
    耗时的IO操作放在额外的线程中执行, 并与主线程进行通信
    HWorker负责任务的调用和与主线程进行通信

    - 主线程创建HWorker实例, 并通过与本实例沟通执行或获得结果(signal&slot)
    - HWorker调用实现了QRunnable的类, 这里为HWorkerTasks
    - HWorker将在新的线程中执行. 线程由线程池自动指定, 由线程池自动回收
    - 另外, 在这个工程里, HWorker还额外记录一个GUET类的引用, 来源于主GUI类, 用于操作GUET教务
    """

    pool = QThreadPool()  # 线程池

    # signals
    # 验证码读取完成
    validationReadFinished = pyqtSignal(dict)

    # 登录完成
    loginFinished = pyqtSignal(dict)

    # 个人信息读取完成
    loadPersonInfoFinished = pyqtSignal(dict)

    # 已选课程查询完成
    loadSelectedCoursesFinished = pyqtSignal(dict)

    # 当前学期加载完成
    loadCurrentTermFinished = pyqtSignal(dict)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.guet: GUET = parent.guet
        self.pool.setMaxThreadCount(6)

    def getValidationCode(self):
        c = HWorkerTasks(self, HWorkerTasks.LOAD_VALIDATION_CODE, GUET=self.guet)
        self.pool.start(c)

    def loginToGUET(self, acc: str, pwd: str, ckCode: str):
        c = HWorkerTasks(self, HWorkerTasks.LOGIN_TO_GUET, GUET=self.guet, account=acc, password=pwd, ckCode=ckCode)
        self.pool.start(c)

    def getPersonInfo(self):
        c = HWorkerTasks(self, HWorkerTasks.GET_PERSON_INFO, GUET=self.guet)
        self.pool.start(c)

    def getSelectedCourse(self, term: str):
        c = HWorkerTasks(self, HWorkerTasks.GET_SELECTED_COURSES, GUET=self.guet, term=term)
        self.pool.start(c)

    def getCurrentTerm(self):
        c = HWorkerTasks(self, HWorkerTasks.GET_CURRENT_TERM, GUET=self.guet)
        self.pool.start(c)


class HWorkerTasks(QRunnable):
    """
    HWorkerTasks类是由HWorker进行执行的任务集

    HWorker(执行者) -> 执行 -> HWorkerTasks(被执行任务)
    """

    # 读取验证码
    LOAD_VALIDATION_CODE = 1

    # 登录到教务
    LOGIN_TO_GUET = 2

    # 读取用户信息
    GET_PERSON_INFO = 4

    # 读取已选课程
    GET_SELECTED_COURSES = 8

    # 读取已选学期
    GET_CURRENT_TERM = 16

    def __init__(self, worker: HWorker, task: int, **kwargs) -> None:
        """
        :param worker: 绑定调用方
        :param task: 确认任务类型
        :param kwargs: 任务的参数 key-value arguments
        """
        super().__init__()
        self.worker = worker
        self.task = task
        self.kwargs = kwargs

    def run(self):
        """
        实际的任务分配, 为QRunnable需要实现的接口
        """
        if self.task == self.LOAD_VALIDATION_CODE:
            self.loadValidationCode()
        elif self.task == self.LOGIN_TO_GUET:
            self.loginToGUET()
        elif self.task == self.GET_PERSON_INFO:
            self.getPersonInfo()
        elif self.task == self.GET_SELECTED_COURSES:
            self.getSelectedCourses()
        elif self.task == self.GET_CURRENT_TERM:
            self.getCurrentTerm()

    def loadValidationCode(self):
        # noinspection PyBroadException
        try:
            guet: GUET = self.kwargs['GUET']
            d = guet.getValidationCode()
            self.worker.validationReadFinished.emit({
                'success': True,
                'data': d
            })
        except Exception as e:
            self.worker.validationReadFinished.emit({
                'success': False,
                'reason': e
            })

    def loginToGUET(self):
        # noinspection PyBroadException
        try:
            guet: GUET = self.kwargs['GUET']
            acc = self.kwargs['account']
            pwd = self.kwargs['password']
            ck = self.kwargs['ckCode']
            r = guet.submitLogin(acc, pwd, ck)
            self.worker.loginFinished.emit(r)
        except Exception as e:
            self.worker.loginFinished.emit({
                'success': False,
                'reason': e
            })

    def getPersonInfo(self):
        # noinspection PyBroadException
        try:
            guet: GUET = self.kwargs['GUET']
            d = guet.getPersonInfo()
            self.worker.loadPersonInfoFinished.emit({
                'success': True,
                'data': d
            })
        except Exception as e:
            self.worker.loadPersonInfoFinished.emit({
                'success': False,
                'reason': e
            })

    def getSelectedCourses(self):
        # noinspection PyBroadException
        try:
            guet: GUET = self.kwargs['GUET']
            d = guet.getSelectedCourses(self.kwargs['term'])
            self.worker.loadSelectedCoursesFinished.emit({
                'success': True,
                'data': d
            })
        except Exception as e:
            self.worker.loadSelectedCoursesFinished.emit({
                'success': False,
                'reason': e
            })

    def getCurrentTerm(self):
        # noinspection PyBroadException
        try:
            guet: GUET = self.kwargs['GUET']
            d = guet.getCurrentTerm()
            print(d)
            self.worker.loadCurrentTermFinished.emit({
                'success': True,
                'data': d
            })
        except Exception as e:
            self.worker.loadCurrentTermFinished.emit({
                'success': False,
                'reason': e
            })
