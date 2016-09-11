class Exporter(object):
    def __init__(self):
        self.po_list = []

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
            for order in self.po_list:
                po_row = []
                column = []
                column.append(order.po_number)
                for item in order.items.values():
                    column.append(item.upc)
                po_row.append(column)
                for store in order.stores.values():
                    column = [store.store_num]
                    for upc in po_row[0][1:]:
                        if upc in store.items.keys():
                            column.append(str(store.items[upc].total_qty))
                        else:
                            column.append(str(0))
                    po_row.append(column)
                output.append(po_row)
            output_string = ''
            for order in output:
                for index in range(len(order[0])):
                    for column in order:
                        output_string += '%s\t' % column[index]
                    output_string += '\n'
                output_string += '\n'
            file.write(output_string)
