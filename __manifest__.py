# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Maple',
    'category': 'Vertical',
    'version': '1.0',
    'author': "Benoit Vézina & Pierre Dalpé pour Portall",
    'website': "portall.ca",
    'summary': 'Odoo adaptation for maple syrup industry.',
    'description':
        """
Odoo adaptation for maple syrup industry.
================================================

This module provides mosly fields and views.
        """,
    'depends': [
        'auto_backup',
        'base',
#        'base_phone',        
        'base_location',        
        'contacts',
        'document',
        'fleet',
        'hr',
        'mrp',
        'partner_identification',
        'purchase',
        'sale',
        'stock_calendar',
        'stock_picking_wave',
        'web_favicon',
    ],
    'data': [
# Chargement des groups, users et rules pour la sécurité
        'data/lang.xml',        
        'data/identification.xml',        
 #       'data/res.groups.users.rel.csv',        
        'security/groups.xml',
# COMMENTÉ CAR MESSAGE :
# "You cannot create a new user from here.
#  To create new user please go to configuration panel.
#        'security/users.xml',
#        'security/rules.xml,
# Chargement des modifications au vues standard
        'views/partner_view.xml',
        'views/product_view.xml',
        'views/stock_location_view.xml',
# Chargement des nouvelles vues spécifiques à Maple
        'views/barrel_view.xml',
        'views/grade_view.xml',
        'views/region_view.xml',
        'views/producer_view.xml',
        'views/purchase_view.xml',
# Chargement d'enregistrements, les fichiers devraient correspondres au modèles
# Devrait être au pluriel sauf exceptions
        'data/grades.xml',
        'data/product_categories.xml',        
        'data/products.xml',
        'data/product.template.csv',
        'wizard/purchase_wizard.xml',
# Chargement des actions et des menus
        'views/actions.xml',                
        'views/maple_location_view.xml',
        'views/menuitems.xml',                
    ],
    'qweb': [
#        "static/src/xml/*.xml",
    ],
#    'bootstrap': True,  # load translations for login screen
    'installable': True,
    'application': True,
    'auto_install': False,
}

