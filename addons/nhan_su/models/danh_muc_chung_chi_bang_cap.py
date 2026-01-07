from odoo import models, fields
class ChungChi(models.Model):
    _name = 'danh_muc_chung_chi_bang_cap'
    _description = 'Danh mục chứng chỉ - bằng cấp'
    _rec_name = 'ten_chung_chi'

    ma_chung_chi = fields.Char("Mã chứng chỉ", required=True)
    ten_chung_chi = fields.Char("Tên chứng chỉ / bằng cấp", required=True)
    cap_do = fields.Char("Cấp độ")
