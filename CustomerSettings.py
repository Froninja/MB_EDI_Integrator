class CustomerSettings(object):
    def __init__(self):
        self.a_name = ''
        self.b_asset_dept = ''
        self.c_memo_dept = ''
        self.f_inv_edi_id = ''
        self.g_ship_edi_id = ''
        self.h_edi_version = ''
        self.j_ship_out_file = ''
        self.i_inv_out_file = ''
        self.k_po_in_file = ''
        self.d_desc_needed = ''
        self.e_create_date_needed = ''
        self.l_po_edi_id = ''

    def sorted_dict(self):
        sorted_dict = list(self.__dict__.keys())
        return sorted(sorted_dict)