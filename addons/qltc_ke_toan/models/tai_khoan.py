from odoo import models, fields, api


class TaiKhoanKeToan(models.Model):
    _name = 'qltc.tai.khoan'
    _description = 'Tài khoản kế toán'

    ma_tai_khoan = fields.Char("Mã tài khoản", required=True)
    ten_tai_khoan = fields.Char("Tên tài khoản", required=True)
    loai_tai_khoan = fields.Selection([
        ('tai_san', 'Tài sản'),
        ('nguon_von', 'Nguồn vốn'),
        ('doanh_thu', 'Doanh thu'),
        ('chi_phi', 'Chi phí'),
    ], string="Loại tài khoản", required=True)
    tai_khoan_cap_tren_id = fields.Many2one('qltc.tai.khoan', string="Tài khoản cấp trên")
    tai_khoan_cap_duoi_ids = fields.One2many('qltc.tai.khoan', 'tai_khoan_cap_tren_id', 
                                               string="Tài khoản cấp dưới")
    mo_ta = fields.Text("Mô tả")
    so_du_dau_ky = fields.Float("Số dư đầu kỳ", digits=(16, 2))
    so_du_cuoi_ky = fields.Float("Số dư cuối kỳ", compute='_compute_so_du_cuoi_ky', store=True, digits=(16, 2))
    but_toan_no_ids = fields.One2many('qltc.but.toan', 'tai_khoan_no_id', string="Bút toán Nợ")
    but_toan_co_ids = fields.One2many('qltc.but.toan', 'tai_khoan_co_id', string="Bút toán Có")

    _sql_constraints = [
        ('ma_tai_khoan_unique', 'unique(ma_tai_khoan)', 'Mã tài khoản phải là duy nhất!')
    ]

    @api.depends('so_du_dau_ky', 'but_toan_no_ids.so_tien', 'but_toan_co_ids.so_tien')
    def _compute_so_du_cuoi_ky(self):
        for record in self:
            tong_no = sum(record.but_toan_no_ids.mapped('so_tien'))
            tong_co = sum(record.but_toan_co_ids.mapped('so_tien'))
            record.so_du_cuoi_ky = record.so_du_dau_ky + tong_no - tong_co
