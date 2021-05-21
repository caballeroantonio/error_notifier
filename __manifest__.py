{
    'name': "Server Error Notifier by Email",
    'version': "12.0",
    'author': "David Montero Crespo",
    'category': "Tools",

    'summary':'The module saves the types of errors that happen on the odoo server and I could send a notification by mail',
    'description':"""
    Server Error Notifier
    server error 
    error notifier
    error email
    The module saves the types of errors that happen on the odoo server and I could send a notification by mail"""
    ,
    'license':'LGPL-3',
    'data': [
        'views/error_tracker_views.xml',
        'views/error_config.xml',
    ],
    'demo': [],
    'depends': [],
    'price': 15,
    'currency': 'EUR',
    'images':[
        'static/description/1.jpg',
    ],
    'installable': True,
}