from odoo import models, fields, api


class TaiSan(models.Model):
    _name = 'qlts.tai.san'
    _description = 'Tài sản'

    ma_tai_san = fields.Char("Mã tài sản", required=True)
    ten_tai_san = fields.Char("Tên tài sản", required=True)
    loai_tai_san_id = fields.Many2one('qlts.loai.tai.san', string="Loại tài sản", required=True)
    ngay_mua = fields.Date("Ngày mua", required=True, default=fields.Date.today)
    nguyen_gia = fields.Float("Nguyên giá", required=True, digits=(16, 2))
    gia_tri_con_lai = fields.Float("Giá trị còn lại", digits=(16, 2), default=0)
    tinh_trang = fields.Selection([
        ('moi', 'Mới'),
        ('dang_su_dung', 'Đang sử dụng'),
        ('bao_tri', 'Bảo trì'),
        ('thanh_ly', 'Thanh lý')
    ], string="Tình trạng", default='moi', required=True)
    vi_tri = fields.Char("Vị trí")
    ghi_chu = fields.Text("Ghi chú")
    tong_khau_hao = fields.Float("Tổng khấu hao", digits=(16, 2), default=0)

    _sql_constraints = [
        ('ma_tai_san_unique', 'unique(ma_tai_san)', 'Mã tài sản phải là duy nhất!')
    ]

    @api.model
    def create(self, vals):
        # Automatically set the default value for 'ma_tai_san' field
        if 'ma_tai_san' not in vals:
            vals['ma_tai_san'] = self.env['ir.sequence'].next_by_code('qlts.tai.san') or '/'
        return super(TaiSan, self).create(vals)