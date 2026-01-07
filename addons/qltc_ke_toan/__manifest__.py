{
    'name': 'Quản lý Kế toán - Bút toán',
    'version': '1.0',
    'depends': ['base', 'qlts_base'],
    'data': [
        'security/ir.model.access.csv',
        'views/tai_khoan_views.xml',
        'views/but_toan_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
}
