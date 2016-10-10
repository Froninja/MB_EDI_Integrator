from src.db.podb import PurchaseOrderDB
from src.models.models import Order, Store, Item, engine
from src.ui.warnings import WarningDialog, POWarningDialog, UPCPOWarningDialog
from sqlalchemy.orm import sessionmaker
from PyQt5 import QtWidgets

class DbValidater(object):
    """
    Helper class to check invoice values against the relevant POs in the database and update
    their shipping status
    """
    def __init__(self, db_name, invoice_list):
        """db_name = valid Sqlite database path, invoice_list = [list of invoice objects]"""
        self.database = sessionmaker(bind=engine)()
        self.invoice_list = invoice_list
        self.po_dict = dict()
        self.warning_dialog = None

    def check_po(self):
        """Root for validating invoices against POs. Returns false if user cancels."""
        po_list = get_po_list(self.invoice_list)
        for order in po_list:
            if self.database.query(Order).filter(Order.po_number == order) is None:
                self.warning_dialog = create_po_warning_dialog(order, self.invoice_list)
                self.warning_dialog.exec_()
                if self.warning_dialog.confirmed:
                    self.invoice_list = validate_po_warning(self.warning_dialog, order,
                                                            self.invoice_list)
                else:
                    return False
        for invoice in self.invoice_list:
            order = self.database.query(Order).filter(Order.po_number == invoice.po_number).first()
            if not self.check_store(invoice, order):
                return False            
        return True

    def check_store(self, invoice, order):
        """Validates invoice against stores on the PO. Returns false if user cancels."""
        if order is not None and invoice.store_number.zfill(4) in [store.store_number
                                                                   for store in order.stores]:
            store = [store for store in order.stores
                     if store.store_number == invoice.store_number.zfill(4)][0]
            for item in invoice.items:
                if not self.check_item(item, store, invoice.invoice_number, order.po_number):
                    return False
            self.update_store_ship_status(invoice, order, store)

        elif order is not None:
            self.warning_dialog = create_store_warning_dialog(order, invoice)
            if self.warning_dialog.exec_() == QtWidgets.QMessageBox.Cancel:
                return False
            self.update_po_ship_status(invoice, order)
        return True

    def check_item(self, item, store, inv_num, po_num):
        """
        Validates item's UPC against UPCs for the given store on the PO. Returns false
        if user cancels.
        """
        if item.upc in [item.upc for item in store.items]:
            return self.check_qty(item, store, inv_num, po_num)
        else:
            self.warning_dialog = create_upc_warning_dialog(item, store, inv_num, po_num)
            self.warning_dialog.parent.exec_()
            return validate_upc_warning(self.warning_dialog)

    def check_qty(self, item, store, inv_num, po_num):
        """
        Validates item's qty against qty for the given store on the PO. Returns false if user
        cancels.
        """
        if item.qty == [it.qty for it in store.items if it.upc == item.upc][0]:
            return True
        else:
            self.warning_dialog = create_qty_warning_dialog(item, store, inv_num, po_num)
            if self.warning_dialog.exec_() == QtWidgets.QMessageBox.Cancel:
                return False
            return True

    def update_po_ship_status(self, invoice, order):
        """
        Invoice: invoice, PurchaseOrder: order
        Updates the shipped cost and invoice list for the provided order
        """
        if invoice.invoice_number not in [inv.invoice_number for inv in order.invoices]:
            order.invoices.append(invoice)
            order.shipped_cost += invoice.total_cost
            #order.shipped_retail += invoice.total_retail
            order.shipped_qty += invoice.total_qty
            #self.database.update(order)

    def update_store_ship_status(self, invoice, order, store):
        """
        Invoice: invoice, PurchaseOrder: order, Store: store
        Updates the shipped cost and qty for the given store
        """
        if invoice.invoice_number not in [inv.invoice_number for inv in store.invoices]:
            #if store.shipped_cost is None:
                #store.shipped_cost = 0.0
                #store.shipped_qty = 0
            store.shipped_cost = float(str.shipped_cost) + invoice.total_cost
            #store.shipped_retail += invoice.total_retail
            store.shipped_qty = int(store.shipped_qty) + invoice.total_qty
            store.invoices.append(invoice)
            #self.database.update(order)


def get_po_list(invoice_list):
    """[invoice_list] -> [po_list]"""
    return list({inv.po_number for inv in invoice_list})

def create_po_warning_dialog(po_num, invoice_list):
    """string: po_num, [invoice_list] -> POWarningDialog"""
    return POWarningDialog(po_num, [inv.invoice_number for inv in invoice_list
                                    if inv.po_number == po_num])

def validate_po_warning(dialog, old_po, invoice_list):
    """POWarningDialog: dialog, string: old_po, [invoice_list] ->
    If user confirms with a new PO# -> [invoice_list]
    If user confirms with no PO# -> [invoice_list]
    If user cancels -> False"""
    if dialog.confirmed is False:
        return False
    if dialog.confirmed is True and len(dialog.po_num) > 0:
        update_po_numbers(old_po, dialog.po_num, invoice_list)
    return invoice_list

def update_po_numbers(old_po, new_po, invoice_list):
    """string: old_po, string: new_po, [invoice_list] -> [invoice_list]"""
    for invoice in [inv for inv in invoice_list if inv.po_number == old_po]:
        invoice.po_number = new_po
    return invoice_list

def create_store_warning_dialog(order, invoice):
    """PurchaseOrder: po, Invoice: invoice -> WarningDialog"""
    return WarningDialog("Store# %s (on invoice# %s) is not allocated on PO# %s"
                         % (invoice.store_number, invoice.invoice_number, order.po_number),
                         detail=("Stores on PO# %s: \n" % order.po_number
                                 + "\n".join(["%s"] * len(order.stores))
                                 % tuple([store.store_number for store in order.stores])))


def create_upc_warning_dialog(item, store, inv_num, po_num):
    """Item: item, Store: store, string: inv_num, string: po_num -> UPCPOWarningDialog"""
    return UPCPOWarningDialog(QtWidgets.QDialog(), item, inv_num, po_num, store)

def validate_upc_warning(dialog):
    """UPCPOWarningDialog: dialog ->
    If user confirms -> True
    If user cancels -> False"""
    return dialog.confirmed

def create_qty_warning_dialog(item, store, inv_num, po_num):
    """Item: item, Store: store, string: inv_num, string: po_num -> WarningDialog"""
    return WarningDialog("Qty of style %s on invoice# %s does not match store# %s on PO# %s"
                         % (item.style, store.store_number, inv_num, po_num),
                         detail=("Qty on store# %s: %s"
                                 % (store.store_number, [st_it.qty for st_it in
                                                      store.items if st_it.upc == item.upc][0])))
