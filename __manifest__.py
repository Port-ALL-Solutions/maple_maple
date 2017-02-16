# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Maple',
    'category': 'Vertical',
    'version': '1.0',
    'summary': 'Odoo adaptation for maple syrup industry.',
    'description':
        """
Odoo adaptation for maple syrup industry.
================================================

This module provides mosly fields and views.
        """,
    'depends': ['base','purchase','mrp','fleet','sale', 'hr', 'contacts'],
    'data': [
        'views/partner_view.xml',
        'views/producer_view.xml',
		'views/menuitems.xml',
        'data/maple_partners.xml',
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

