import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from GUETCoursePyQt.Worker.ThreadWorker import HWorker
from UI_LoginWindow import *


class LoginWindow(QDialog, Ui_LoginWindow):
    loginFinished = pyqtSignal(dict)

    def __init__(self, parent):
        super().__init__(parent, flags=Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.setWindowTitle('登录到GUET')
        self.setFixedSize(self.width(), self.height())
        self.worker: HWorker = parent.worker
        self.lineEditAccount.setFocus()  # 默认焦点
        self.btnRefresh.setEnabled(False)
        self.worker.validationReadFinished.connect(self.onLoadValidateCodeFinished)
        self.worker.loginFinished.connect(self.onLoginFinished)
        self.btnRefresh.clicked.connect(self.onBtnRefreshCkCodeClicked)
        self.btnLogin.clicked.connect(self.onBtnLoginClicked)
        self.loadValidateCodeAsync()

    def onBtnRefreshCkCodeClicked(self):
        self.loadValidateCodeAsync()

    def loadValidateCodeAsync(self):
        self.btnRefresh.setEnabled(False)
        self.worker.getValidationCode()

    def onLoadValidateCodeFinished(self, val):
        self.btnRefresh.setEnabled(True)

        if val['success']:
            p = QPixmap()
            p.loadFromData(val['data'])
            self.labelCkCode.setPixmap(p)
        else:
            QMessageBox().critical(self, '发生错误', f'无法获得验证码\n 原因: {val["reason"]}')

    def onBtnLoginClicked(self):
        account = self.lineEditAccount.text()
        password = self.lineEditPasswd.text()
        ck = self.lineEditValidationCode.text()

        if len(account) == 0:
            QMessageBox().warning(self, '警告', '用户标识为空')
            return

        if len(password) == 0:
            QMessageBox().warning(self, '警告', '需要提供凭据')
            return

        if len(ck) == 0:
            QMessageBox().warning(self, '警告', '需要验证码')
            return

        self.btnLogin.setEnabled(False)
        self.btnLogin.setText('正在登录...')
        self.worker.loginToGUET(account, password, ck)

    def onLoginFinished(self, val):
        self.btnLogin.setEnabled(True)
        self.btnLogin.setText('登录')

        if val['success']:
            QMessageBox().information(self, '登录成功', f'登录成功. 消息\n{val}')
            self.loginFinished.emit(val)
            self.deleteLater()
        else:
            QMessageBox().critical(self, '登录失败', f'无法登录, 原因\n{val}')


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = LoginWindow(None)
    w.exec()
    a.exec()
