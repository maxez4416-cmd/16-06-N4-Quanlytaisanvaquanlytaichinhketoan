{
    'name': 'Quản lý Tài sản - Cơ sở',
    'version': '1.0',
    'category': 'Accounting',
    'license': 'LGPL-3',
    'summary': 'Module quản lý tài sản cơ bản',
    'description': """
        Module quản lý tài sản bao gồm:
        - Danh mục tài sản
        - Loại tài sản
        - Quản lý thông tin tài sản
    """,
    'author': 'Your Company',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/loai_tai_san_views.xml',
        'views/tai_san_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}