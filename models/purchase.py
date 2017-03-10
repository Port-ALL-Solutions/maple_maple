# -*- coding: utf-8 -*-
from openerp import models, fields, api
class PurchaseOrder(models.Model):
#    _name = "purchase.order"
    _inherit = 'purchase.order'
    
    location_id = fields.Many2one(
        'stock.location', 'Destination Location',
        index=True, required=True, states={'done': [('readonly', True)]},
        help="Sets a destination location where to put the stock after reception.")
    
class PurchaseOrderLine(models.Model):
#    _name = "purchase.order"
    _inherit = 'purchase.order.line'
    
    partner_fpaqCode = fields.Char(
        string='FPAQ',
        related='partner_id.fpaqCode'
        )
    
    partner_street = fields.Char(
        string='Address',
        related='partner_id.street'
        )
    
    partner_city = fields.Char(
        string='City',
        related='partner_id.city'
        )
        
    partner_state = fields.Char(
        string='Province / State',
        related='partner_id.state_id.name'
        )

    partner_region = fields.Char(
        string='Region',
        related='partner_id.maple_region.name',
        store = True
        )
    
#    devra être remplacé par l'actuel buyer
    partner_default_buyer = fields.Char(
        string='Buyer',
        related='partner_id.default_owner_id.ref',
        store = True
        )
    
#    partner_phone_farm = fields.Char(
#        string='Phone',
#        related='partner_id.phone',
#        store = True
#        )
    

    