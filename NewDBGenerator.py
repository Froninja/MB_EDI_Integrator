from PurchaseOrderDB import PurchaseOrderDB
from CustomerSettings import CustomerSettings

def read_config(config_file):
    settings = dict()
    settings['customers'] = []
    with open(config_file, 'r') as config:
        for line in config:
            line = line.strip('\n').strip('\n').split(': ')
            if line[0] == "Shipping Log":
                settings['shiplog'] = line[1]
            elif line[0] == "Destination Log":
                settings['destlog'] = line[1]
            elif line[0] == "Description Log":
                settings['desclog'] = line[1]
            elif line[0] == "UPC Exception Log":
                settings['upcexceptlog'] = line[1]
            elif line[0] == "Label Record File":
                settings['outputlog'] = line[1]
            elif line[0] == "PO Database File":
                settings['po_db'] = line[1]
            elif line[0] == "MAPDATA Path":
                settings['mapdata'] = line[1]
            elif line[0] == "Connection String":
                settings['connstring'] = line[1]
            elif line[0] == "Invoice Query":
                settings['invquery'] = line[1]
            elif line[0] == "Destination Query":
                settings['destquery'] = line[1]
            elif line[0] == "Memo Destination Query":
                settings['memodestquery'] = line[1]
            elif line[0] == "UPC Query":
                settings['upcquery'] = line[1]
            elif line[0] == "Ring UPC Query":
                settings['ringupcquery'] = line[1]
            elif line[0] == "Customer":
                customer = CustomerSettings()
                line = line[1].split('>>')
                for index in range(len(customer.sorted_dict())):
                    if index < len(line):
                        setattr(customer, customer.sorted_dict()[index], line[index])
                settings['customers'].append(customer)
    return settings

if __name__ == '__main__':
    settings = read_config('P:\EDI\MB_EDI_Integrator\\bin\config.txt')
    db = PurchaseOrderDB(settings)
    db.get_po_from_export()