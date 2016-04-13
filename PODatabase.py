from PurchaseOrder import PurchaseOrder
import shelve

class PODatabase(object):
    """Stores a set of PurchaseOrder objects and represents them to the user"""
    def __init__(self, flag):
        self.read_config('Config.txt')
        self.purchase_orders = shelve.open(self.settings['po_db'], flag=flag)
        self.self_test()

    def read_config(self, config_file):
        self.settings = dict()
        self.settings['customers'] = dict()
        with open(config_file, 'r') as config:
            for line in config:                
                line = line.strip('\n').strip('\n').split(': ')
                if line[0] == "PO Database File":
                    self.settings['po_db'] = line[1]
                elif line[0] == "Customer":
                    line = line[1].split('>>')
                    self.settings['customers'][line[0]] = line[10]

    def read_export(self, customer):
        """Reads the TLW export based on customer name. If the PO number is not
        already in the program data, adds it"""
        export_file = self.get_export_file(customer)
        with open(export_file, 'r') as export:
            for line in export:
                line = line.rstrip('\n').rstrip('\r').split(',')
                if line[1] != 'PO #':
                    if line[1].lstrip('0') not in self.purchase_orders:
                        PO = PurchaseOrder(line[1].lstrip('0'), customer)
                        print("Adding PO# %s" % PO.po_number)
                        PO.start_ship = line[2]
                        PO.cancel_ship = line[3]
                        PO.creation_date = line[10]
                        PO.get_items_from_export(export_file)
                        PO.get_stores_from_export(export_file)
                        for item in PO.items.values():
                            PO.total_cost += (item.cost * item.total_qty)
                        self.purchase_orders[PO.po_number] = PO
                        self.purchase_orders.sync()
                    else:
                        PO = self.purchase_orders[line[1].lstrip('0')]
                        print("Updating PO# %s" % PO.po_number)
                        PO.start_ship = line[2]
                        PO.cancel_ship = line[3]
                        PO.creation_date = line[10]
                        self.purchase_orders[PO.po_number] = PO
                        self.purchase_orders.sync()

    def get_cost_from_exp(self, po_num, export_file):
        """Searches the TLW export for all lines matching the supplied PO
        number and returns total cost based on the sum of each line's cost"""
        total_cost = 0
        with open(export_file, 'r') as export:
            for line in export:
                line = line.rstrip('\n').rstrip('\r').split(',')
                if line[1] == po_num:
                    total_cost += float(line[7]) * int(line[9])
        return total_cost

    def check_export_against_db(self, PO_num):
        """For a given PO Number in the export file, checks against the data
        file loaded at program start. If the PO already exists, returns false
        """
        if PO_num != "PO #":
            if PO_num in self.purchase_orders:
                return True
            else:
                return False
        else:
            return True

    def get_export_file(self, customer):
        if len(self.settings['customers'][customer]) > 0:
            return self.settings['customers'][customer]

    def self_test(self):
        print("Beginning database self-test")
        po_counter = 0
        error_counter = 0
        for po in self.purchase_orders.keys():
            po_counter += 1
            try:
                self.purchase_orders[po]
            except:
                print("Remove key '%s'" % po)
                del self.purchase_orders[po]
                error_counter += 1
        print("Database self-test complete.")
        print("Tested %s items." % po_counter)
        print("Found %s errors." % error_counter)
                

if __name__ == '__main__':
    po_db = PODatabase()
    for setting in po_db.settings:
        print(setting)