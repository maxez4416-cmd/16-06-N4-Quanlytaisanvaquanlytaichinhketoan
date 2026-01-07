{
    'name': 'Quản lý Khấu hao Tài sản',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Module quản lý khấu hao tài sản',
    'description': """
        Module quản lý khấu hao tài sản:
        - Tính khấu hao tự động
        - Lịch sử khấu hao
        - Báo cáo khấu hao
    """,
    'author': 'Your Company',
    'depends': ['base', 'qlts_base'],
    'data': [
        'security/ir.model.access.csv',
        'views/khau_hao_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}