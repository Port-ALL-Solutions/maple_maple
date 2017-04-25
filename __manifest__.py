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
        'contacts',
        'document',
        'fleet',
        'hr',
        'ir_sequence_daily_range',
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
        'data/flavors.xml',
        'data/flaws.xml',       
        'data/identification.xml',        
        'data/container_state.xml',
        'data/container_material.xml',
        'data/container_owner_type.xml',
        'data/sequence.xml',  
#        'data/classification_site.xml',           
#        'data/res.groups.users.rel.csv',
        'data/product_categories.xml',
        'data/product_attributes.xml',
#        'data/products.xml',          
#		'data/product.product.csv',
  		'data/product.template.xml',
		'data/product.product.xml',
        'data/product.template.csv',
        'data/grades.xml',
        'security/groups.xml',
# COMMENTÉ CAR MESSAGE :
# "You cannot create a new user from here.
#  To create new user please go to configuration panel.
#        'security/users.xml',
#        'security/rules.xml,
# Chargement des modifications au vues standard
        'views/employee_view.xml',
        'views/partner_view.xml',
        'views/product_view.xml',
#        'views/stock_location_view.xml',
# Chargement des nouvelles vues spécifiques à Maple
        'views/barrel_view.xml',
        'views/grade_view.xml',
        'views/region_view.xml',
#        'views/producer_view.xml',
        'views/purchase_view.xml',
# Chargement d'enregistrements, les fichiers devraient correspondres au modèles
# Devrait être au pluriel sauf exceptions
# Chargement des actions et des menus
#        'views/maple_location_view.xml',
#        'views/actions.xml',                
        'views/stock_pack_operation.xml',                
        'wizard/purchase_wizard.xml',
        'wizard/reception_wizard.xml',        
        'views/rating_view.xml',                
        'views/weight_view.xml',
        'views/acer_import.xml',                
# other_actions = Action not define in views
        'views/other_actions.xml',         
# menuitems = The menu, need to be put last
        'views/menuitems.xml',
# reports
        'data/report_paperformat.xml',
        'report/fpaq_reception.xml',
        'report/reception_labels.xml',
        'report/acer_classification.xml',

    ],
    'qweb': [
#        "static/src/xml/*.xml",
    ],
#    'bootstrap': True,  # load translations for login screen
    'installable': True,
    'application': True,
    'auto_install': False,
}

