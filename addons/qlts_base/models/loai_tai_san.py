from odoo import models, fields, api


class LoaiTaiSan(models.Model):
    _name = 'qlts.loai.tai.san'
    _description = 'Loại tài sản'

    ma_loai = fields.Char("Mã loại", required=True)
    ten_loai = fields.Char("Tên loại", required=True)
    mo_ta = fields.Text("Mô tả")
    thoi_gian_su_dung = fields.Integer("Thời gian sử dụng (năm)", default=5)
    ty_le_khau_hao = fields.Float("Tỷ lệ khấu hao (%)", digits=(5, 2))
    tai_san_ids = fields.One2many('qlts.tai.san', 'loai_tai_san_id', string="Danh sách tài sản")
    so_luong_tai_san = fields.Integer("Số lượng tài sản", compute='_compute_so_luong_tai_san', store=True)

    _sql_constraints = [
        ('ma_loai_unique', 'unique(ma_loai)', 'Mã loại tài sản phải là duy nhất!')
    ]

    @api.depends('tai_san_ids')
    def _compute_so_luong_tai_san(self):
        for record in self:
            record.so_luong_tai_san = len(record.tai_san_ids)