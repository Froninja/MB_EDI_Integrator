import shelve
import PurchaseOrder
import PODatabase

def start_dialog():
    print """Welcome to the Marco Bicego EDI Purchase Order Database command line interface.
    Please select an option and press Enter.

    1) View an existing Purchase Order
    2) Edit an existing Purchase Order
    3) Add a new Purchase Order
    4) Remove an existing Purchase Order"""

def get_and_validate_input(num_options):
    input = raw_input()
    try:
        if input == 'q' or input == 'Q':
            return False
        elif int(input) not in range(1,num_options):
            print "Please select a valid option."
            return
        else:
            return input
    except ValueError:
        print "Please select a valid option.\n\n"
        return

def update_po():
    pass

def view_po():
    print """Please select view mode:
    
    1) View single PO#
    2) View POs by customer
    """
    input = raw_input()
    if input == '1':
        view_single_po()

def view_single_po():
    print "Please enter the desired PO#:"
    db = shelve.open('PO_Data')
    po = ''
    while True:
        input = raw_input()    
        try:
            po = db[str(input)]
            break
        except KeyError:
            print "That PO# is not in the database. Please enter another PO#:"
    print_po_labels()
    print_po(po)
    

def print_po_labels():
    print "PO#".ljust(9), "Label".ljust(15), "Cost".ljust(10),
    print "Units".ljust(8), "Start Ship".ljust(10), "Cancel".ljust(10)

def print_po(po):
    print po.po_number.ljust(9), po.label.ljust(15),
    print str("$%s" % po.total_cost).ljust(10), "0".ljust(8),
    print po.start_ship.ljust(10), po.cancel_ship.ljust(10)

def add_po():
    pass

def delete_po():
    pass

if __name__ == '__main__':
    while True:
        start_dialog()
        input = get_and_validate_input(5)
        if input == False:
            break
        elif input == '1':
            view_po()