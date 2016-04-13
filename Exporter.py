class Exporter(object):
    def __init__(self):
        pass

    def set_po_list(self, po_list):
        try:
            po_list[0]
            self.po_list = po_list
        except TypeError:
            self.po_list = []
            self.po_list.append(po_list)

    def export_spreadsheet(self, export_file):
        with open(export_file, 'w') as file:
            output = []
            for po in self.po_list:
                po_row = []
                column = []
                column.append(po.po_number)
                for item in po.items.values():
                    column.append(item.UPC)
                po_row.append(column)
                for store in po.stores.values():
                    column = [store.store_num]
                    for UPC in po_row[0][1:]:
                        if UPC in store.items.keys():
                            column.append(str(store.items[UPC].total_qty))
                        else:
                            column.append(str(0))
                    po_row.append(column)
                output.append(po_row)
            output_string = ''
            for po in output:
                for index in range(len(po[0])):
                    for column in po:
                        output_string += '%s\t' % column[index]
                    output_string += '\n'
                output_string += '\n'
            file.write(output_string)