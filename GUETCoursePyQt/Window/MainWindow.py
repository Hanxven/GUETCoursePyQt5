import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from GUETCoursePyQt.Worker.ThreadWorker import *
from GUETCoursePyQt.Window.UI_MainWindow import *
import GUETCoursePyQt.QtResources.RCC_res
from GUETCoursePyQt.GUET.GUET import *
from GUETCoursePyQt.Window.LoginWindow import *
from GUETCoursePyQt.Window.SettingsWindow import *


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    The main window
    """
    def __init__(self):
        super().__init__(flags=Qt.Widget)
        self.setWindowTitle('The Window is Me!')
        self.setupUi(self)
        self.setWindowTitle('主窗口')
        self.guet = GUET()  # global GUET()
        self.worker = HWorker(self)  # global HWorker()
        self.globalData = {}  # 全局信息保存

        # table - selected courses
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['课程名', '课程ID', '课程序号', '学分', '性质', '选课类别', '选课时间', '附加'])
        self.tableSelectedCourses.setModel(model)
        self.worker.loadSelectedCoursesFinished.connect(self.onLoadSelectedCoursesFinished)

        # other
        self.actionLogin.triggered.connect(self.showLoginDialog)
        self.actionSettings.triggered.connect(self.onActionSettingsTriggered)
        self.worker.loadPersonInfoFinished.connect(self.onLoadPersonInfoFinished)
        self.btnQuery.clicked.connect(self.onBtnQueryClicked)
        self.worker.loadCurrentTermFinished.connect(self.onLoadCurrentTermFinished)

        self.log('Finished Launching Window')  # LOG
        self.show()
        self.showLoginDialog()

    def onDialogLoginFinished(self, val: dict):
        self.log(f'Login Result: {json.dumps(val, ensure_ascii=False)}')  # log
        self.stackedWidget.setCurrentIndex(1)
        self.worker.getPersonInfo()

    def showLoginDialog(self):
        loginWindow = LoginWindow(self)
        loginWindow.loginFinished.connect(self.onDialogLoginFinished)
        loginWindow.exec()

    def onActionSettingsTriggered(self):
        # toggle settings window
        settingsWindow = SettingsWindow(self)
        settingsWindow.applySettings.connect(self.settingsChanged)
        settingsWindow.exec()

    def settingsChanged(self, val: dict):
        self.guet.setSettings(val)

    def onLoadPersonInfoFinished(self, val):
        self.globalData['person'] = val
        pre = '具体信息. 其中spno为专业代号.\n注意, 此处存在大量意义不明的键.\n'
        self.textInfo.setPlainText(f'{pre}\n{json.dumps(val, ensure_ascii=False, sort_keys=True, indent=4)}')
        self.worker.getCurrentTerm()

    def log(self, info: str):
        t = QDateTime().currentDateTime().toString('yyyy.MM.dd hh:mm:ss.zzz')
        self.textLog.appendPlainText(f'[{t}] {info}')

    def onBtnQueryClicked(self):
        term = self.comboBoxTerms.currentText()
        self.worker.getSelectedCourse(term)

    def onLoadCurrentTermFinished(self, val: dict):
        self.comboBoxTerms.clear()
        d: list = val['data']['data']
        self.comboBoxTerms.addItems(d)

    def onLoadSelectedCoursesFinished(self, val: dict):
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

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        重写方法, 程序退出事件. 在程序关闭时关闭Session连接
        :param event:
        :return: Node
        """
        self.guet.closeSession()
        event.accept()


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MainWindow()
    a.exec()
