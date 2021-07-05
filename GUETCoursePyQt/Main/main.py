import sys
from GUETCoursePyQt.Window.MainWindow import *
from GUETCoursePyQt.QtResources.RCC_res import *

# program entry here
if __name__ == '__main__':
    # global instance
    a = QApplication(sys.argv)

    # load the style sheet
    # file = QFile(':Resources/Dark.qss')
    # file.open(QIODevice.ReadOnly)
    # style = str(bytes(file.readAll()), encoding='utf-8')
    # a.setStyleSheet(style)
    # file.close()

    # init window
    w = MainWindow()

    # event loop
    a.exec()
