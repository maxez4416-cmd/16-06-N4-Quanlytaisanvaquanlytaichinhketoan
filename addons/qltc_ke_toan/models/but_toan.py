from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ButToan(models.Model):
    _name = 'qltc.but.toan'
    _description = 'Bút toán kế toán'
    _order = 'ngay_ghi_nhan desc'

    ma_but_toan = fields.Char("Mã bút toán", required=True, copy=False, 
                                readonly=True, default='New')
    ngay_ghi_nhan = fields.Date("Ngày ghi nhận", required=True, 
                                  default=fields.Date.today)
    tai_khoan_no_id = fields.Many2one('qltc.tai.khoan', string="Tài khoản Nợ", required=True)
    tai_khoan_co_id = fields.Many2one('qltc.tai.khoan', string="Tài khoản Có", required=True)
    so_tien = fields.Float("Số tiền", required=True, digits=(16, 2))
    dien_giai = fields.Text("Diễn giải", required=True)
    loai_but_toan = fields.Selection([
        ('thu', 'Thu'),
        ('chi', 'Chi'),
        ('khau_hao', 'Khấu hao'),
        ('khac', 'Khác')
    ], string="Loại bút toán", default='khac', required=True)
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('xac_nhan', 'Xác nhận'),
        ('huy', 'Hủy')
    ], string="Trạng thái", default='nhap', required=True)
    khau_hao_ids = fields.One2many('qlts.khau.hao', 'but_toan_id', string="Khấu hao")

    _sql_constraints = [
        ('ma_but_toan_unique', 'unique(ma_but_toan)', 'Mã bút toán phải là duy nhất!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('ma_but_toan', 'New') == 'New':
            vals['ma_but_toan'] = self.env['ir.sequence'].next_by_code('qltc.but.toan') or 'New'
        return super(ButToan, self).create(vals)

    @api.constrains('so_tien')
    def _check_so_tien(self):
        for record in self:
            if record.so_tien <= 0:
                raise ValidationError("Số tiền phải lớn hơn 0!")

    @api.constrains('tai_khoan_no_id', 'tai_khoan_co_id')
    def _check_tai_khoan(self):
        for record in self:
            if record.tai_khoan_no_id == record.tai_khoan_co_id:
                raise ValidationError("Tài khoản Nợ và Có phải khác nhau!")

    def action_xac_nhan(self):
        self.write({'trang_thai': 'xac_nhan'})

    def action_huy(self):
        self.write({'trang_thai': 'huy'})

    def action_chuyen_ve_nhap(self):
        self.write({'trang_thai': 'nhap'})