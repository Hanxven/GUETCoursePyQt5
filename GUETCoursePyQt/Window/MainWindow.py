import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from GUETCoursePyQt.Worker.ThreadWorker import *
from GUETCoursePyQt.Window.UI_MainWindow import *
import GUETCoursePyQt.QtResources.RCC_res
from GUETCoursePyQt.GUET.GUET import *
from GUETCoursePyQt.Window.LoginWindow import *


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
        self.actionLogin.triggered.connect(self.showLoginDialog)
        self.worker.loadPersonInfoFinished.connect(self.displayPersonInfo)
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

    def displayPersonInfo(self, val):
        # 多此一举, 非重要部分
        pre = '具体信息. 其中spno为专业代号.\n注意, 此处存在大量意义不明的键.\n'
        self.textInfo.setPlainText(f'{pre}\n{json.dumps(val, ensure_ascii=False, sort_keys=True, indent=4)}')

    def log(self, info: str):
        t = QDateTime().currentDateTime().toString('yyyy.MM.dd hh:mm:ss.zzz')
        self.textLog.appendPlainText(f'[{t}] {info}')


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MainWindow()
    a.exec()
