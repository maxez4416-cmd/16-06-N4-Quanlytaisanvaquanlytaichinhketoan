from odoo import models, fields, api


class BaoCaoTaiSan(models.TransientModel):
    _name = 'qltc.bao.cao.tai.san'
    _description = 'Báo cáo tài sản'

    tu_ngay = fields.Date("Từ ngày", required=True, default=fields.Date.today)
    den_ngay = fields.Date("Đến ngày", required=True, default=fields.Date.today)
    loai_tai_san_id = fields.Many2one('qlts.loai.tai.san', string="Loại tài sản")
    tinh_trang = fields.Selection([
        ('tat_ca', 'Tất cả'),
        ('moi', 'Mới'),
        ('dang_su_dung', 'Đang sử dụng'),
        ('bao_tri', 'Bảo trì'),
        ('thanh_ly', 'Thanh lý')
    ], string="Tình trạng", default='tat_ca')
    
    chi_tiet_ids = fields.One2many('qltc.bao.cao.tai.san.chi.tiet', 'bao_cao_id', 
                                    string="Chi tiết", readonly=True)
    tong_nguyen_gia = fields.Float("Tổng nguyên giá", compute='_compute_tong', digits=(16, 2))
    tong_khau_hao = fields.Float("Tổng khấu hao", compute='_compute_tong', digits=(16, 2))
    tong_con_lai = fields.Float("Tổng giá trị còn lại", compute='_compute_tong', digits=(16, 2))

    @api.depends('chi_tiet_ids.nguyen_gia', 'chi_tiet_ids.tong_khau_hao', 'chi_tiet_ids.gia_tri_con_lai')
    def _compute_tong(self):
        for record in self:
            record.tong_nguyen_gia = sum(record.chi_tiet_ids.mapped('nguyen_gia'))
            record.tong_khau_hao = sum(record.chi_tiet_ids.mapped('tong_khau_hao'))
            record.tong_con_lai = sum(record.chi_tiet_ids.mapped('gia_tri_con_lai'))

    def action_tao_bao_cao(self):
        self.ensure_one()
        
        # Xóa chi tiết cũ
        self.chi_tiet_ids.unlink()
        
        # Tìm tài sản theo điều kiện
        domain = [('ngay_mua', '>=', self.tu_ngay), ('ngay_mua', '<=', self.den_ngay)]
        if self.loai_tai_san_id:
            domain.append(('loai_tai_san_id', '=', self.loai_tai_san_id.id))
        if self.tinh_trang != 'tat_ca':
            domain.append(('tinh_trang', '=', self.tinh_trang))
        
        tai_san_list = self.env['qlts.tai.san'].search(domain)
        
        # Tạo chi tiết báo cáo
        for tai_san in tai_san_list:
            self.env['qltc.bao.cao.tai.san.chi.tiet'].create({
                'bao_cao_id': self.id,
                'tai_san_id': tai_san.id,
                'ma_tai_san': tai_san.ma_tai_san,
                'ten_tai_san': tai_san.ten_tai_san,
                'loai_tai_san': tai_san.loai_tai_san_id.ten_loai,
                'nguyen_gia': tai_san.nguyen_gia,
                'tong_khau_hao': tai_san.tong_khau_hao,
                'gia_tri_con_lai': tai_san.gia_tri_con_lai,
                'tinh_trang': tai_san.tinh_trang,
            })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'qltc.bao.cao.tai.san',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }


class BaoCaoTaiSanChiTiet(models.TransientModel):
    _name = 'qltc.bao.cao.tai.san.chi.tiet'
    _description = 'Chi tiết báo cáo tài sản'

    bao_cao_id = fields.Many2one('qltc.bao.cao.tai.san', string="Báo cáo", ondelete='cascade')
    tai_san_id = fields.Many2one('qlts.tai.san', string="Tài sản")
    ma_tai_san = fields.Char("Mã tài sản")
    ten_tai_san = fields.Char("Tên tài sản")
    loai_tai_san = fields.Char("Loại tài sản")
    nguyen_gia = fields.Float("Nguyên giá", digits=(16, 2))
    tong_khau_hao = fields.Float("Tổng khấu hao", digits=(16, 2))
    gia_tri_con_lai = fields.Float("Giá trị còn lại", digits=(16, 2))
    tinh_trang = fields.Selection([
        ('moi', 'Mới'),
        ('dang_su_dung', 'Đang sử dụng'),
        ('bao_tri', 'Bảo trì'),
        ('thanh_ly', 'Thanh lý')
    ], string="Tình trạng")