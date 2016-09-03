from ui.pyuic.UiLauncherDialog import Ui_Launcher
from ui.powindow import POWindow
from ui.shipwindow import ShippingWindow
from PyQt5 import QtWidgets, QtGui
import sys

class Launcher(Ui_Launcher):
    def __init__(self, dialog):
        super(Launcher, self).__init__()
        self.setupUi(dialog)
        dialog.setWindowTitle("MB EDI Launcher")
        dialog.setWindowIcon(QtGui.QIcon("Resources\MBIcon.bmp"))
        self.VersionLabel.setText("Beta 0.5.6 9-2-2016")
        self.ShipButton.clicked.connect(self.ship_clicked)
        self.POButton.clicked.connect(self.po_clicked)

    def ship_clicked(self):
        self.s = QtWidgets.QMainWindow()
        self.sw = ShippingWindow(self.s)
        self.s.show()

    def po_clicked(self):
        self.p = QtWidgets.QMainWindow()
        self.pw = POWindow(self.p)
        self.p.show()

if __name__ == '__main__':
    a = QtWidgets.QApplication(sys.argv)
    q = QtWidgets.QDialog()
    w = Launcher(q)
    q.show()

    sys.exit(a.exec_())