from PODatabase import PODatabase

if __name__ == '__main__':
    po_db = PODatabase('c')
    print("""Marco Bicego EDI PO Database

    Commencing update\n""")
    for customer in po_db.settings['customers'].keys():
        print("Updating %s POs" % customer)
        try:
            po_db.read_export(customer)
        except (TypeError, FileNotFoundError):
            print("No valid file for %s" % customer)
    print("""Update complete""")
    po_db.purchase_orders.close()