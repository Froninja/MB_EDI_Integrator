"""Classes and helper functions to represent invoices and products extracted from ERP"""

from datetime import datetime

class Invoice(object):
    """Represents an invoice to be extracted from ERP and transmitted via EDI"""
    def __init__(self, invoice_number):
        self.invoice_number = invoice_number
        self.customer = ""
        self.store_number = ""
        self.tracking_number = ""
        self.ship_date = ""
        self.discount_code = ""
        self.discount_percent = 0
        self.sscc = ""
        self.purchase_order_number = ""
        self.department_number = ""
        self.distribution_center = ""
        self.item_count = 0
        self.total_cost = 0
        self.total_qty = 0
        self.store_name = 0
        self.address1 = ""
        self.address2 = ""
        self.city = ""
        self.state = ""
        self.zip_code = ""
        self.items = []
        self.po_create_date = ""

    def discount(self, discount_percent):
        """Sets the discount value and EDI discount code based on the provided value"""
        if discount_percent >= 0:
            self.discount_percent = discount_percent
        elif discount_percent is None:
            self.discount_percent = 0
        if discount_percent == 0 or discount_percent is None:
            self.discount_code = "05"
        else:
            self.discount_code = "08"

    def get_dept_num(self, memo_val, asset_dept, memo_dept):
        """Sets the department number based on the settings provided"""
        if memo_val is True or memo_val == 2:
            self.department_number = memo_dept.zfill(4)
        else:
            self.department_number = asset_dept.zfill(4)

    def shipping_information(self, shiplog):
        """Searches the shiplog for the invoice number and sets the invoice's tracking and address
        info when a match is found. Searches in reverse order to find recent values faster"""
        for line in reversed(open(shiplog, "r").readlines()):
            line = line.replace('"', '').split(",")
            invoice = line[10].split(" ")
            for item in invoice:
                if len(item) == 5:
                    if item == str(self.invoice_number):
                        self.tracking_number = line[9]
                        self.ship_date = datetime.strptime(line[0], '%Y%m%d')
                        self.address1 = line[2]
                        self.address2 = line[3]
                        self.city = line[4]
                        self.state = line[5]
                        self.zip_code = line[6][:5]

    def shipping_information_from_tracking(self, shiplog):
        """Searches the shiplog for the tracking number and sets the invoice's address info when
        a match is found"""
        with open(shiplog, 'r') as ship_log:
            for line in ship_log:
                line = line.replace('"', '').split(",")
                if line[9] == "{}".format(str(self.tracking_number)):
                    self.ship_date = datetime.strptime(line[0], '%Y%m%d')
                    self.address1 = line[2]
                    self.address2 = line[3]
                    self.city = line[4]
                    self.state = line[5]
                    self.zip_code = line[6][:5]

    def get_sscc(self):
        """Sets the GS1 SSCC number from the invoice number"""
        self.sscc = generate_sscc(self.invoice_number)

    def get_create_date(self, po_dict):
        """Checks the PO# of the invoice against the loaded PO database and
        assigns the PO creation date"""
        try:
            self.po_create_date = (
                po_dict[self.purchase_order_number.lstrip('0')].creation_date)
        except:
            pass

    def totals(self):
        """Sets the total cost and qty based on the items in self.items"""
        self.total_cost = sum([item.unit_cost * item.qty_each for item in self.items])
        self.total_qty = sum([item.qty_each for item in self.items])

    def add_item(self, item):
        """Adds an item to the invoice and increments the invoice's totals"""
        self.item_count += 1
        self.total_qty += item.qty_each
        self.total_cost += item.unit_cost * item.qty_each
        if item.long_style not in [i.long_style for i in self.items]:
            self.items.append(item)
        else:
            [i for i in self.items if i.long_style == item.long_style][0].qty_each += item.qty_each

class Product(object):
    """Represents an item extracted from the ERP and attached to an invoice"""
    def __init__(self, long_style):
        self.long_style = long_style
        self.proper_style = ""
        self.upc = ""
        self.unit_cost = 0
        self.qty_each = 0
        self.description = ""
        self.color = ""
        self.size = ""

    def upc_exception_check(self, exception_path, customer):
        """Checks a log file for manual UPC exceptions (where a retailer has
        a different UPC for a given style than what is set in the DB) and
        replaces the UPC if the style and customer match"""
        with open(exception_path, 'r') as exception_list:
            for line in exception_list:
                line = line.rstrip('\n').split(',')
                if line[:2] == [customer, self.long_style]:
                    self.upc = line[2]

    @classmethod
    def from_item(cls, item):
        """Generates a Product from an order's Item"""
        prod = Product(item.style_num)
        prod.upc = item.upc
        prod.unit_cost = item.cost
        prod.qty_each = item.total_qty
        return prod

def generate_sscc(inv_num):
    """Generates a GS1 18 digit SSCC number from the supplied invoice number"""
    sscc_string = str(80327620000000000 + int(inv_num))
    check_sum = 0
    # pyLint: disable=consider-using-enumerate
    for num in range(len(sscc_string)):
        if num % 2 == 0:
            check_sum += int(sscc_string[num]) * 3
        else:
            check_sum += int(sscc_string[num])
    check_digit = ((check_sum + 9) // 10 * 10) - check_sum
    return sscc_string + str(check_digit)
