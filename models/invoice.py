from datetime import datetime

class Invoice(object):
    """description of class"""   
    def __init__(self, invoice_number):
        self.invoice_number = invoice_number
        self.customer = ""
        self.store_number = ""
        self.tracking_number = ""
        self.ship_date = ""
        self.discount_code = ""
        self.discount_percent = 0
        self.SSCC = ""
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
        if discount_percent >= 0:
            self.discount_percent = discount_percent
        elif discount_percent == None:
            self.discount_percent = 0
        if discount_percent == 0 or discount_percent == None:
            self.discount_code = "05"
        else:
            self.discount_code = "08"

    def get_dept_num(self, memo_val, asset_dept, memo_dept):
        if memo_val == True or memo_val == 2:
            self.department_number = memo_dept.zfill(4)
        else:
            self.department_number = asset_dept.zfill(4)

    def shipping_information(self, shiplog):
        for line in reversed(open(shiplog, "r").readlines()):
            line = line.replace('"','').split(",")
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
        ship_log = open(shiplog, "r")
        for line in ship_log:
            line = line.replace('"','').split(",")
            if line[9] == "{}".format(str(self.tracking_number)):
                self.ship_date = datetime.strptime(line[0], '%Y%m%d')
                self.address1 = line[2]
                self.address2 = line[3]
                self.city = line[4]
                self.state = line[5]
                self.zip_code = line[6][:5]
        ship_log.close()

    def print_shipping_info(self):
        return "{}, {}, {}, {}, {}, {}, {}".format(self._tracking_number,
                                                   self._ship_date,
                                                   self._address1,
                                                   self._address2,
                                                   self._city, self._state,
                                                   self._zip_code)

    def get_SSCC(self):
        base_string = 80327620000000000
        sq_string = base_string + int(self.invoice_number)
        sq_list = [int(num) for num in str(sq_string)]
        check_sum = 0
        for num in range(17):
            if num % 2 == 0:
                check_sum += sq_list[num] * 3
            else:
                check_sum += sq_list[num]
        sq_string = (''.join(str(num) for num in sq_list)
                     + str(((check_sum + 9) // 10 * 10) - check_sum))
        self.SSCC = sq_string

    def UPC_exception_check(self, config_file):
        """Checks a log file for manual UPC exceptions (where a retailer has
        a different UPC for a given style than what is set in the DB) and
        replaces the UPC if the style and customer match"""
        exception_path = ''
        with open(config_file, 'r') as config:
            for line in config:
                line = line.split(": ")
                if line[0] == "UPC Exception File":
                    exception_path = line[1].rstrip('\n')
        with open(exception_path, 'r') as exception_list:
            for line in exception_list:
                line = line.rstrip('\n').split(',')
                for item in self.items:
                    if line[0] == self.customer:
                        if line[1] == item.long_style:
                            item.UPC = line[2]

    def get_create_date(self, po_dict):
        """Checks the PO# of the invoice against the loaded PO database and
        assigns the PO creation date"""
        try:
            self.po_create_date = (
                po_dict[self.purchase_order_number.lstrip('0')].creation_date)
        except:
            pass

    def totals(self):
        self.total_cost = sum([item.unit_cost * item.qty_each for item in self.items])
        self.total_qty = sum([item.qty_each for item in self.items])

    def add_item(self, item):
        self.item_count += 1
        self.total_qty += item.qty_each
        self.total_cost += item.unit_cost * item.qty_each
        if item.long_style not in [i.long_style for i in self.items]:
            self.items.append(item)
        else:
            [i for i in self.items if i.long_style == item.long_style][0].qty_each += item.qty_each

class Product(object):
    """description of class"""
    def __init__(self, long_style):
        self.long_style = long_style
        self.proper_style = ""
        self.UPC = ""
        self.unit_cost = 0
        self.qty_each = 0
        self.description = ""
        self.color = ""
        self.size = ""

    def UPC_exception_check(self, exception_path, customer):
        """Checks a log file for manual UPC exceptions (where a retailer has
        a different UPC for a given style than what is set in the DB) and
        replaces the UPC if the style and customer match"""
        with open(exception_path, 'r') as exception_list:
            for line in exception_list:
                line = line.rstrip('\n').split(',')
                if line[:2] == [customer, self.long_style]:
                    self.UPC = line[2]

    @classmethod
    def from_item(cls, item):
        prod = Product(item.style_num)
        prod.UPC = item.UPC
        prod.unit_cost = item.cost
        prod.qty_each = item.total_qty
        return prod
