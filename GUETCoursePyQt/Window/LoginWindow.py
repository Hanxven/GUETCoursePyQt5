import logging
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from GUETCoursePyQt.Worker.ThreadWorker import HWorker
from GUETCoursePyQt.Window.UI_LoginWindow import *

# temporary baidu ORC token
BAIDU_OCR_TOKEN = '24.bb714e66010de2e2c8abfbf62af23d5b.2592000.1628157200.282335-23548153'


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
        self.worker.identifyImageFinished.connect(self.onImageIdentified)
        self.worker.loginFinished.connect(self.onLoginFinished)
        self.btnRefresh.clicked.connect(self.onBtnRefreshCkCodeClicked)
        self.btnLogin.clicked.connect(self.onBtnLoginClicked)
        self.loadValidateCode()

        # DEBUG
        self.lineEditAccount.setText('1900301037')
        self.lineEditPasswd.setText('3092599')

    def onBtnRefreshCkCodeClicked(self):
        self.loadValidateCode()

    def loadValidateCode(self):
        self.btnRefresh.setEnabled(False)
        self.worker.getValidationCode()

    def onLoadValidateCodeFinished(self, val: dict):
        self.btnRefresh.setEnabled(True)

        if val['success']:
            p = QPixmap()
            p.loadFromData(val['data'])
            self.labelCkCode.setPixmap(p)
            self.tryIdentifyImage(val['data'], BAIDU_OCR_TOKEN)
        else:
            QMessageBox().critical(self, '发生错误', f'验证码加载失败\n 原因: {val["reason"]}', QMessageBox.Ok)

    def onBtnLoginClicked(self):
        account = self.lineEditAccount.text()
        password = self.lineEditPasswd.text()
        ck = self.lineEditValidationCode.text()

        if len(account) == 0:
            QMessageBox().warning(self, '警告', '用户标识为空', QMessageBox.Ok)
            return

        if len(password) == 0:
            QMessageBox().warning(self, '警告', '需要提供凭据', QMessageBox.Ok)
            return

        if len(ck) == 0:
            QMessageBox().warning(self, '警告', '需要验证码', QMessageBox.Ok)
            return

        self.btnLogin.setEnabled(False)
        self.btnLogin.setText('正在登录...')
        self.worker.loginToGUET(account, password, ck)

    def onLoginFinished(self, val):
        self.btnLogin.setEnabled(True)
        self.btnLogin.setText('登录')

        if val['success']:
            # QMessageBox().information(self, '登录成功', f'登录成功. 消息\n{val}', QMessageBox.Ok)
            self.loginFinished.emit(val)
            self.deleteLater()
        else:
            QMessageBox().critical(self, '登录失败', f'无法登录, 原因\n{val}', QMessageBox.Ok)

    def tryIdentifyImage(self, d: bytes, token: str):
        self.worker.identityImageBaidu(d, token)

    def onImageIdentified(self, val: dict):
        # 识别内容
        if val['success'] and 'words_result' in val['data'].keys():
            l: list = val['data']['words_result']
            if len(l) != 0 and 'words' in l[0].keys():
                r: str = l[0]['words']
                self.lineEditValidationCode.setText(r)
        else:
            print(val['reason'])
