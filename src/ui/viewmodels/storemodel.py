from src.models.purchaseorder import PurchaseOrder, Store, Item
from src.models.models import Order, Store, Item
from PyQt5 import QtCore, QtWidgets

class TreeNode(object):
    def __init__(self, parent, row):
        self.parent = parent
        self.row = row
        self.subNodes = self._getChildren()

    def _getChildren(self):
        raise NotImplementedError()

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self):
        QtCore.QAbstractItemModel.__init__(self)
        self.rootNodes = self._getRootNodes()

    def _getRootNodes(self):
        raise NotImplementedError()

    def index(self, row, column, parent):
        if not parent.isValid():
            return self.createIndex(row, column, self.rootNodes[row])
        parentNode = parent.internalPointer()
        if not parentNode.subNodes is None:
            return self.createIndex(row, column, parentNode.subNodes[row])
        return QtCore.QModelIndex()

    def getNodeFromIndex(self, index):    
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node            
        return self.po_list

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        node = index.internalPointer()
        if node.parent is None:
            return QtCore.QModelIndex()
        else:
            return self.createIndex(node.parent.row, 0, node.parent)

    def reset(self):
        self.rootNodes = self._getRootNodes()
        QtCore.QAbstractItemModel.resetInternalData(self)

    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.rootNodes)
        node = parent.internalPointer()
        if not node.subNodes is None:
            return len(node.subNodes)
        else:
            return 1

class ModelElement(object):
    def __init__(self, name, subelements):
        self.name = name
        self.subelements = subelements

class ModelNode(TreeNode):
    def __init__(self, ref, parent, row):
        self.ref = ref
        TreeNode.__init__(self, parent, row)

    def _getChildren(self):
        try:
            node_list = []
            for num in range(len(self.ref.items)):
                node_list.append(ModelNode(self.ref.stores[num], self, num))
            return node_list
        except AttributeError:
            try:
                node_list = []
                for num in range(len(self.ref.items)):
                    node_list.append(ModelNode(self.ref.items[num], self, num))
                return node_list
            except AttributeError:
                return None

class StoreModel(TreeModel):
    def __init__(self, stores):
        self.stores = sorted(stores, key=lambda store: store.store_number)
        TreeModel.__init__(self)
        self.headers = ['Store/UPC #', 'Style Number', 'Cost', 'Total Qty', 'Shipped Cost']
        self.store_attr = ['store_number', '', 'total_cost', 'total_qty', 'shipped_cost']
        self.item_attr = ['upc', 'style', 'cost', 'qty', '']
        self.parent_form = ''

    def flags(self, index):
        if isinstance(index.internalPointer().ref, Order) and index.column() == 1:
            return QtCore.Qt.ItemIsEditable | super().flags(index)
        else:
            return super().flags(index)

    def _getRootNodes(self):
        node_list = []
        for num in range(len(self.stores)):
            node_list.append(ModelNode(self.stores[num], None, num))
        return node_list

    def columnCount(self, parent):
        return len(self.headers)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            if isinstance(node.ref, Store):
                try:
                    return QtCore.QVariant(getattr(node.ref, self.store_attr[index.column()]))
                except (AttributeError, IndexError):
                    return None
            elif isinstance(node.ref, Item):
                try:
                    return QtCore.QVariant(getattr(node.ref, self.item_attr[index.column()]))
                except (AttributeError, IndexError):
                    return None
        return None

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole and index.isValid() and index.column() == 1:
            po = index.internalPointer().ref
            po.label = value
            self.parent_form.po_db.purchase_orders[po.po_number] = po
            return True
        else:
            return False

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.headers[section]
        return None