# -*- coding: utf-8 -*-

{
    'name': "Biens Immobiliers",

    'category': 'Uncategorized',

    'description': """
    Module dédié à la gestion de biens immobiliers.
    """,

    'author': "Thomas BOIDUN",
    'website': 'https://github.com/thomasboidun/odoo-real-estate-addon',

    'application': True,
    'version': '1.0',
    'depends': ['base', 'hr'],

    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        
        'views/real_estate_menu_views.xml',
        'views/real_estate_list_view.xml',
        'views/real_estate_search_view.xml',
        'views/real_estate_action_view.xml',
        'views/real_estate_form_view.xml',
        'views/real_estate_owner_views.xml',
    ],

    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
}
