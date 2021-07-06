import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import io
import os
from GUETCoursePyQt.Worker.ThreadWorker import *
from GUETCoursePyQt.Window.UI_MainWindow import *
import GUETCoursePyQt.QtResources.RCC_res
from GUETCoursePyQt.GUET.GUET import *
from GUETCoursePyQt.Window.LoginWindow import *
from GUETCoursePyQt.Window.SettingsWindow import *
from GUETCoursePyQt.Window.ErrorWindow import *


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    主窗口, 部分负责功能的调用以及协调各方面内容

    - 功能调用: 主程序(QApplication) -> GUI(负责显示与操作) -> Worker(事件分配) -> QRunnable(任务本身) -> GUET工具类(具体处理)
            -> requests库 -> urllib3库 -> ...
    - 事件传递: QRunnable对象其调用对象Worker的signal -> 主程序的onXXX槽函数 (信号和槽方式)

    定义信号和槽, 传递的数据为一个dict, 包含一个success: boolean, 和一个data/reason: dict

    {
        'success': True (or False),

        'data': dict (if 'success' is True) or

        'reason': dict (if 'success is False)
    }
    """
    def __init__(self):
        super().__init__(flags=Qt.Widget)
        self.setWindowTitle('The Window is Me!')
        self.setupUi(self)
        self.setWindowTitle('主窗口')

        self.errorWindow = ErrorWindow(None)
        self.guet = GUET()  # 全局GUET工具包
        self.worker = HWorker(self)  # 所拥有的HWorker
        self.mwSettings = {
            'stu': {},  # 个人动态信息
            'person': {}  # 个人详细信息
        }  # 全局设置信息保存

        # table - selected courses
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['课程名', '课程ID', '课程序号', '学分', '性质', '选课类别', '选课时间', '附加'])
        self.tableSelectedCourses.setModel(model)
        self.tableSelectedCourses.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.worker.loadSelectedCoursesFinished.connect(self.onLoadSelectedCoursesFinished)

        # connects
        self.actionErrorWindow.triggered.connect(self.errorWindow.show)
        self.actionLogin.triggered.connect(self.showLoginDialog)
        self.actionSettings.triggered.connect(self.onActionSettingsTriggered)
        self.worker.loadPersonInfoFinished.connect(self.onLoadPersonInfoFinished)
        self.worker.loadStuInfoFinished.connect(self.onLoadStuInfoFinished)
        self.worker.loadCurrentTermFinished.connect(self.onLoadCurrentTermFinished)
        self.worker.loadAvailableCoursesFinished.connect(self.onLoadAvailableCoursesFinished)
        self.worker.loadMajorsFinished.connect(self.onLoadMajorsFinished)
        self.btnQuery.clicked.connect(self.onBtnQueryClicked)

        # components setting
        self.stackedWidget.setCurrentIndex(0)
        self.show()
        self.showLoginDialog()

    def onDialogLoginFinished(self, val: dict):
        self.stackedWidget.setCurrentIndex(1)  # to working page

        # 获取个人详细信息
        self.getPersonInfo()

        # 获取当前动态信息, 重要
        self.getStuInfo()
        # 完成后 -> self.getCurrentTerm()  需要在getStuInfo完成后进行

        # 获取全部部门
        self.getDepartments()
        # 完成后 -> self.getMajors() 需要在getDepartments完成后进行

    def getPersonInfo(self):
        # nothing needed
        # 你要问为什么加了一层函数
        # 是因为要完成GUI的状态设置和进行实际的任务分配
        self.status.showMessage('正在获取个人信息...', 1000)
        self.worker.getPersonInfo()

    def getCurrentTerm(self):
        self.status.showMessage('正在获取可用学期...', 1000)
        self.comboBoxTerms.setEnabled(False)
        self.worker.getCurrentTerm()

    def getStuInfo(self):
        self.status.showMessage('正在获取当前信息...', 1000)
        self.worker.getStuInfo()

    def getMajors(self):
        self.status.showMessage('正在获取专业列表...', 1000)
        self.comboBoxMajors.setEnabled(False)
        self.worker.getMajors()

    def getDepartments(self):
        self.status.showMessage('正在获取部门列表...', 1000)
        self.worker.getDepartments()

    def getSelectedCourses(self, term: str):
        self.status.showMessage(f'正在获取学期{term}已选课程...', 1000)
        self.worker.getSelectedCourse(term)

    def showLoginDialog(self):
        loginWindow = LoginWindow(self)
        loginWindow.loginFinished.connect(self.onDialogLoginFinished)
        loginWindow.exec()

    def onActionSettingsTriggered(self):
        # toggle settings window
        settingsWindow = SettingsWindow(self)
        settingsWindow.applySettings.connect(self.setGUETSettings)
        settingsWindow.exec()

    def setGUETSettings(self, val: dict):
        keys = val.keys()
        if 'timeout' in keys:
            self.guet.setTimeout(val['timeout'])

    def onLoadPersonInfoFinished(self, val):
        self.mwSettings['details'] = val['data']
        pre = '具体信息. 其中spno为专业代号.\n注意, 此处存在大量意义不明的键.\n'
        self.textInfo.setPlainText(f'{pre}\n{json.dumps(val, ensure_ascii=False, sort_keys=True, indent=4)}')

    def onLoadStuInfoFinished(self, val: dict):
        if not val['success']:
            self.errorWindow.showErrorMessage(val['reason'])
            self.errorWindow.show()
            return

        d = val['data']
        self.labelNameAndNo.setText(f'**{d["name"]}** - **{d["stid"]}**')
        self.labelDptNameAndNo.setText(f'{d["dptname"]} **(编号: {d["dptno"]})**')
        self.labelGrade.setText(f'**{d["grade"]}**级')
        self.labelMajorAndNo.setText(f'{d["spname"]} **(专业代号: {d["spno"]})**')
        self.labelCurrentTerm.setText(f'当前学期: **{d["term"]}**')
        self.mwSettings['stu'] = d

        # 在完成StuInfo的读取后, 可以进行目前学期的读取
        self.getCurrentTerm()

    def onBtnQueryClicked(self):
        term = self.comboBoxTerms.currentText()
        if len(term) == 0:
            QMessageBox().critical(self, '错误', '学期为空', QMessageBox.Ok)
            return
        self.btnQuery.setEnabled(False)
        self.btnQuery.setText('加载中')
        self.getSelectedCourses(term)

    def onLoadCurrentTermFinished(self, val: dict):
        if not val['success']:
            self.comboBoxTerms.setEnabled(True)
            self.errorWindow.showErrorMessage(val['reason'])
            self.errorWindow.show()
            return

        self.comboBoxTerms.setEnabled(True)
        self.comboBoxTerms.clear()
        d: list = val['data']['data']
        self.comboBoxTerms.addItems(d)

        # 如果getStuInfo先一步执行完的话, 可以自动设置为当前学期
        if 'term' in self.mwSettings['stu'].keys():
            term = self.mwSettings['stu']['term']
            self.comboBoxTerms.setCurrentText(term)

    def onLoadSelectedCoursesFinished(self, val: dict):
        self.btnQuery.setEnabled(True)
        self.btnQuery.setText('查询')

        if not val['success']:
            self.errorWindow.showErrorMessage(val['reason'])
            self.errorWindow.show()
            return

        d: list = val['data']['data']
        m: QStandardItemModel = self.tableSelectedCourses.model()
        m.removeRows(0, m.rowCount())
        for each in d:
            row = [
                # ['课程名', '课程ID', '课程序号', '学分', '性质', '选课类别', '选课时间', '附加']
                QStandardItem(each['cname']),
                QStandardItem(each['courseid']),
                QStandardItem(each['courseno']),
                QStandardItem(each['xf']),  # 学分
                QStandardItem(each['tname']),
                QStandardItem(each['stype']),
                QStandardItem(each['xksj']),  # 选课时间
                QStandardItem(each['comm'] if each['comm'] else '(无)')  # 可能为空
            ]
            m.appendRow(row)

        # 无数据判断
        if len(d) == 0:
            QMessageBox().information(self, '查询结果', '暂无数据', QMessageBox.Ok)

    def onLoadAvailableCoursesFinished(self, val: dict):
        pass

    def onLoadMajorsFinished(self, val: dict):
        if not val['success']:
            self.comboBoxMajors.setEnabled(True)
            self.errorWindow.showErrorMessage(val['reason'])
            self.errorWindow.show()
            return

        self.comboBoxMajors.setEnabled(True)
        self.comboBoxMajors.clear()
        d = val['data']['data']

        for each in d:  # for each { ... }
            if each['used'] != 0:
                self.comboBoxMajors.addItem(f'{each["spno"]} - {each["spname"]}', each)

    def onLoadDepartmentsFinished(self, val: dict):
        if not val['success']:
            self.errorWindow.showErrorMessage(val['reason'])
            self.errorWindow.show()
            return

        ...  # TODO 完成后

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        重写方法, 程序退出事件. 在程序关闭时关闭Session连接
        :param event: 事件
        :return: None
        """
        self.guet.closeSession()
        event.accept()

    @staticmethod
    def categorizeMajorInfo(d: list) -> dict:
        """
        将获得的专业列表, 按照dptNo分类
        并根据对应
        :return: 返回每个大类对应的专业字典
        """
        ret = {}
        for each in d:  # 存在则加入
            dptNo = each['dptno']
            if dptNo in ret.keys():
                l: list = ret[dptNo]
                l.append(each)
            else:  # 不存在则创建
                l: list = []
                ret[dptNo] = l
        return ret


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MainWindow()
    a.exec()
