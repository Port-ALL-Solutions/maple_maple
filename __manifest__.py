# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Maple',
    'category': 'Vertical',
    'version': '1.0',
    'author': "Benoît Vézina & Pierre Dalpé pour Portall",
    'website': "portall.ca",
    'summary': 'Odoo adaptation for maple syrup industry.',
    'description':
        """
Odoo adaptation for maple syrup industry.
================================================

This module provides mosly fields and views.
        """,
    'depends': [
        'base',
        'contacts',
        'fleet',
        'hr',
        'mrp',
        'purchase',
        'sale',
    ],
    'data': [
        'views/grade_view.xml',
        'views/partner_view.xml',
        'views/producer_view.xml',
        'views/product_view.xml',
        'data/maple_grades.xml',
        'data/maple_partners.xml',
        'data/maple_products.xml',
        'views/menuitems.xml',
#        'views/webclient_templates.xml',
    ],
    'qweb': [
#        "static/src/xml/*.xml",
    ],
#    'bootstrap': True,  # load translations for login screen
    'installable': True,
    'application': True,
    'auto_install': False,
}

