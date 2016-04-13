import sys
from PyQt5 import QtWidgets
from main_form import MainWindow

if __name__ == '__main__':
    a = QtWidgets.QApplication(sys.argv)
    q = QtWidgets.QMainWindow()
    w = MainWindow(q)
    q.show()

    sys.exit(a.exec_())