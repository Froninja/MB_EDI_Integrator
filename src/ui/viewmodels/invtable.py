from PyQt5 import QtCore, QtGui, QtWidgets

class InvoiceTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(QtWidgets.QTableWidget, self).__init__()
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def keyPressEvent(self, e):
        modifiers = QtGui.QGuiApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            if e.key() == QtCore.Qt.Key_D:
                if len(self.selectedRanges()) == 1 and self.selectedRanges()[0].rowCount() > 1:
                    rows = list(range(self.selectedRanges()[0].topRow(),
                                      self.selectedRanges()[0].bottomRow() + 1))
                    columns = list(range(self.selectedRanges()[0].leftColumn(),
                                         self.selectedRanges()[0].rightColumn() + 1))
                    for column in columns:
                        data = self.item(rows[0], column).data(QtCore.Qt.DisplayRole)
                        for row in rows:
                            self.setItem(row, column, QtWidgets.QTableWidgetItem(data, 0))
        elif e.key() == QtCore.Qt.Key_Enter:
            super().keyPressEvent(e)
            if (len(self.selectedIndexes()) == 1
                and self.selectedIndexes()[0].row() != self.rowCount()):
                self.setCurrentCell(self.selectedIndexes()[0].row() + 1,
                                    self.selectedIndexes()[0].column())
        else:
            return super().keyPressEvent(e)
