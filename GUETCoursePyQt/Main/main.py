import sys
from GUETCoursePyQt.Window.MainWindow import *


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = MainWindow()
    a.exec()
