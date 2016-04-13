from PyQt5 import QtGui, QtCore, QtWidgets, QtSql
import sys

class POEditView(QtWidgets.QDialog):
    def __init__(self, settings):
        QtWidgets.QDialog.__init__(self)
        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('PO_Database')
        self.db.open()

        self.model = QtSql.QSqlTableModel(self, self.db)
        self.model.setTable("stores")
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.select()
        #self.model.setHeaderData(0, QtCore.Qt.Horizontal, 'ponum')
        #self.model.setHeaderData(1, QtCore.Qt.Horizontal, 'customer')

        self.table = QtWidgets.QTableView(self)
        self.table.setModel(self.model)
        self.table.show()
        self.vertical_layout.addWidget(self.table)

if __name__ == '__main__':
    settings = dict()
    settings['po_db'] = 'PO_Database.db'
    a = QtWidgets.QApplication(sys.argv)
    d = POEditView(settings)
    d.exec_()