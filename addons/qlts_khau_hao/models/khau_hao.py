from odoo import models, fields, api
from odoo.exceptions import ValidationError


class KhauHao(models.Model):
    _name = 'qlts.khau.hao'
    _description = 'Khấu hao tài sản'
    _order = 'nam desc, thang desc'

    tai_san_id = fields.Many2one('qlts.tai.san', string="Tài sản", required=True, ondelete='cascade')
    thang = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
        ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
        ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12')
    ], string="Tháng", required=True)
    nam = fields.Integer("Năm", required=True)
    gia_tri_khau_hao = fields.Float("Giá trị khấu hao", required=True, digits=(16, 2))
    gia_tri_con_lai = fields.Float("Giá trị còn lại", compute='_compute_gia_tri_con_lai', store=True, digits=(16, 2))
    ghi_chu = fields.Text("Ghi chú")
    but_toan_id = fields.Many2one('qltc.but.toan', string="Bút toán liên quan", readonly=True)

    _sql_constraints = [
        ('unique_khau_hao', 'unique(tai_san_id, thang, nam)', 
         'Đã tồn tại bản ghi khấu hao cho tài sản này trong tháng/năm này!')
    ]

    @api.depends('tai_san_id.nguyen_gia', 'tai_san_id.tong_khau_hao')
    def _compute_gia_tri_con_lai(self):
        for record in self:
            if record.tai_san_id:
                record.gia_tri_con_lai = max(0.0, (record.tai_san_id.nguyen_gia or 0.0) - (record.tai_san_id.tong_khau_hao or 0.0))
            else:
                record.gia_tri_con_lai = 0.0

    @api.constrains('gia_tri_khau_hao')
    def _check_gia_tri_khau_hao(self):
        for record in self:
            if record.gia_tri_khau_hao <= 0:
                raise ValidationError("Giá trị khấu hao phải lớn hơn 0!")
            if record.tai_san_id:
                tong_kh_khac = sum(record.tai_san_id.khau_hao_ids.filtered(lambda x: x.id != record.id).mapped('gia_tri_khau_hao'))
                if tong_kh_khac + record.gia_tri_khau_hao > (record.tai_san_id.nguyen_gia or 0.0):
                    raise ValidationError("Tổng giá trị khấu hao không được vượt quá nguyên giá!")

    def action_tao_but_toan(self):
        """Tạo bút toán kế toán cho khấu hao"""
        self.ensure_one()
        if self.but_toan_id:
            raise ValidationError("Đã tồn tại bút toán cho khấu hao này!")
        
        ButToan = self.env['qltc.but.toan']
        but_toan = ButToan.create({
            'ngay_ghi_nhan': fields.Date.today(),
            'dien_giai': f"Khấu hao tài sản {self.tai_san_id.ten_tai_san} - {self.thang}/{self.nam}",
            'so_tien': self.gia_tri_khau_hao,
            'loai_but_toan': 'khau_hao',
        })
        self.but_toan_id = but_toan.id
        return True
