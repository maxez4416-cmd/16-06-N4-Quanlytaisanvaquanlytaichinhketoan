from odoo import models, fields, api


class BaoCaoTaiChinh(models.TransientModel):
    _name = 'qltc.bao.cao.tai.chinh'
    _description = 'Báo cáo tài chính'

    tu_ngay = fields.Date("Từ ngày", required=True, default=fields.Date.today)
    den_ngay = fields.Date("Đến ngày", required=True, default=fields.Date.today)
    loai_bao_cao = fields.Selection([
        ('thu_chi', 'Báo cáo thu chi'),
        ('tai_khoan', 'Báo cáo tài khoản'),
        ('tong_hop', 'Báo cáo tổng hợp')
    ], string="Loại báo cáo", default='thu_chi', required=True)
    
    chi_tiet_ids = fields.One2many('qltc.bao.cao.tai.chinh.chi.tiet', 'bao_cao_id', 
                                    string="Chi tiết", readonly=True)
    tong_thu = fields.Float("Tổng thu", compute='_compute_tong', digits=(16, 2))
    tong_chi = fields.Float("Tổng chi", compute='_compute_tong', digits=(16, 2))
    chenh_lech = fields.Float("Chênh lệch", compute='_compute_tong', digits=(16, 2))

    @api.depends('chi_tiet_ids.so_tien_thu', 'chi_tiet_ids.so_tien_chi')
    def _compute_tong(self):
        for record in self:
            record.tong_thu = sum(record.chi_tiet_ids.mapped('so_tien_thu'))
            record.tong_chi = sum(record.chi_tiet_ids.mapped('so_tien_chi'))
            record.chenh_lech = record.tong_thu - record.tong_chi

    def action_tao_bao_cao(self):
        self.ensure_one()
        
        # Xóa chi tiết cũ
        self.chi_tiet_ids.unlink()
        
        # Tìm bút toán theo điều kiện
        domain = [
            ('ngay_ghi_nhan', '>=', self.tu_ngay),
            ('ngay_ghi_nhan', '<=', self.den_ngay),
            ('trang_thai', '=', 'xac_nhan')
        ]
        
        but_toan_list = self.env['qltc.but.toan'].search(domain)
        
        # Tạo chi tiết báo cáo
        for but_toan in but_toan_list:
            so_tien_thu = but_toan.so_tien if but_toan.loai_but_toan == 'thu' else 0
            so_tien_chi = but_toan.so_tien if but_toan.loai_but_toan in ['chi', 'khau_hao'] else 0
            
            self.env['qltc.bao.cao.tai.chinh.chi.tiet'].create({
                'bao_cao_id': self.id,
                'but_toan_id': but_toan.id,
                'ma_but_toan': but_toan.ma_but_toan,
                'ngay_ghi_nhan': but_toan.ngay_ghi_nhan,
                'dien_giai': but_toan.dien_giai,
                'loai_but_toan': but_toan.loai_but_toan,
                'so_tien_thu': so_tien_thu,
                'so_tien_chi': so_tien_chi,
            })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'qltc.bao.cao.tai.chinh',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }


class BaoCaoTaiChinhChiTiet(models.TransientModel):
    _name = 'qltc.bao.cao.tai.chinh.chi.tiet'
    _description = 'Chi tiết báo cáo tài chính'

    bao_cao_id = fields.Many2one('qltc.bao.cao.tai.chinh', string="Báo cáo", ondelete='cascade')
    but_toan_id = fields.Many2one('qltc.but.toan', string="Bút toán")
    ma_but_toan = fields.Char("Mã bút toán")
    ngay_ghi_nhan = fields.Date("Ngày ghi nhận")
    dien_giai = fields.Text("Diễn giải")
    loai_but_toan = fields.Selection([
        ('thu', 'Thu'),
        ('chi', 'Chi'),
        ('khau_hao', 'Khấu hao'),
        ('khac', 'Khác')
    ], string="Loại")
    so_tien_thu = fields.Float("Số tiền thu", digits=(16, 2))
    so_tien_chi = fields.Float("Số tiền chi", digits=(16, 2))