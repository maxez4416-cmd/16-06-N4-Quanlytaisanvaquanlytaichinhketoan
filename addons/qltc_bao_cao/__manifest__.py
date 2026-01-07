{
    'name': 'Báo cáo tài chính',
    'version': '1.0',
    'depends': ['base', 'qlts_base', 'qltc_ke_toan'],
    'data': [
        'security/ir.model.access.csv',
        'views/bao_cao_tai_san_views.xml',
        'views/bao_cao_tai_chinh_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
}