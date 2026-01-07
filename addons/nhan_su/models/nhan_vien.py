from odoo import models, fields, api

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_va_ten'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ho_ten_dem = fields.Char("Họ tên đệm", required=True)
    ho_va_ten = fields.Char("Họ và tên", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    tuoi= fields.Integer("tuoi", compute="_compute_tuoi", store=False)
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    lich_su_cong_tac_ids = fields.One2many(
        "lich_su_cong_tac", 
        inverse_name="nhan_vien_id", 
        string = "Danh sách lịch sử công tác")
    danh_sach_chung_chi_bang_cap_ids = fields.One2many(
        "danh_sach_chung_chi_bang_cap", 
        inverse_name="nhan_vien_id", 
        string = "Danh sách chứng chỉ bằng cấp")
    so_bhxh = fields.Char("so bh xh")
    ngay_tham_ra = fields.Date("ngay ham ra")
    chuyen_mon = fields.Char("chuyen mon", required=True)
    @api.depends("ngay_sinh")
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                record.tuoi = fields.Date.today().year - record.ngay_sinh.year
            else:
                record.tuoi = 0

    @api.constrains('ngay_sinh')
    def _check_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                tuoi = fields.Date.today().year - record.ngay_sinh.year
                if tuoi < 18:
                    raise models.ValidationError("Nhân viên chưa đủ 18 tuổi")
