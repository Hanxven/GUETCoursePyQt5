from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUETCoursePyQt.Window.UI_SettingsWindow import *


class SettingsWindow(QDialog, Ui_SettingsWindow):
    # 更改设置
    applySettings = pyqtSignal(dict)

    def __init__(self, parent: QWidget):
        super().__init__(parent, Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setupUi(self)

