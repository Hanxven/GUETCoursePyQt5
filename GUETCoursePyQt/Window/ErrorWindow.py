from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget
from GUETCoursePyQt.Window.UI_ErrorWindow import *


class ErrorWindow(QWidget, Ui_ErrorWindow):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupUi(self)

    def showErrorMessage(self, msg: str):
        time = QDateTime.currentDateTime().toString('yyyy.MM.dd hh:mm:ss.zzz')
        self.textEdit.setTextColor(QColor('#800000'))
        self.textEdit.append(f'[{time}] {msg}')

    def showWaringMessage(self, msg: str):
        time = QDateTime.currentDateTime().toString('yyyy.MM.dd hh:mm:ss.zzz')
        self.textEdit.setTextColor(QColor('#D2691E'))
        self.textEdit.append(f'[{time}] {msg}')
