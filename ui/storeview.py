from ui.pyuic.UiStoreViewWindow import Ui_StoreViewWindow
from ui.viewmodels.storemodel import StoreModel
from models.po import Store
from helpers.export import Exporter
from PyQt5 import QtGui

class StoreViewWindow(Ui_StoreViewWindow):
    def __init__(self, main_window, po):
        super(StoreViewWindow, self).__init__()
        self.parent = main_window
        self.setupUi(self.parent)
        self.parent.setWindowTitle("MB EDI PO# %s" % po.po_number)
        self.parent.setWindowIcon(QtGui.QIcon("Resources\MBIcon.bmp"))
        self.po = po
        stores = (Store
                 .select()
                 .where(Store.purchase_order == po))
        self.model = StoreModel(list(stores))
        self.StoreView.setModel(self.model)
        self.actionExport_Spreadsheet.triggered.connect(self.export_for_ss)

    def export_for_ss(self):
        exporter = Exporter()
        exporter.set_po_list(self.po)
        exporter.export_spreadsheet('Export.xls')