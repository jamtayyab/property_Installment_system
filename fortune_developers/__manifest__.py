# -*- coding: utf-8 -*-
{
    'name': "TFD",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/company_data.xml',
        'views/views.xml',
        'views/projects.xml',
        'views/phases.xml',
        'views/floors.xml',
        'views/property_type.xml',
        'views/company_profile.xml',
        'views/property_marlas.xml',
        'views/payment_template.xml',
        'views/property_files.xml',
        'views/templates.xml',
        'views/booking.xml',
        'report/report_template.xml',
        'report/report.xml',
        'wizard/report_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "application": True,
    "installable": True,
}
