# -*- coding: utf-8 -*-
from openerp import models, fields, api
class PurchaseOrder(models.Model):
#    _name = "purchase.order"
    _inherit = 'purchase.order'
    
    location_id = fields.Many2one(
        'stock.location', 'Destination Location',
        index=True, required=True, states={'done': [('readonly', True)]},
        help="Sets a destination location where to put the stock after reception.")
    
    owner_id = fields.Many2one(
        'res.partner', 'Owner',
        domain=[('maple_buyer', '=', True)],
        help="Default Owner")

    owner_ref = fields.Char(
        string='Owner',
        related='owner_id.ref'
        )

    maple_outside_qc = fields.Boolean(string='HQ',
        related='partner_id.maple_outside_qc',                                    
        help="This is an outside of Quebec Partner.",
        store=True)    

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

    qty_container = fields.Float(
        string='Quantity',
        compute='_compute_qty_container',
        store=True
        )
    
    @api.depends('order_line')
    def _compute_qty_container(self):
        for record in self:
            qty = 0 
            for line in record.order_line:
                if line.product_id.maple_container:
                    qty += line.product_qty          
            record.qty_container = qty
                       
class PurchaseOrderLine(models.Model):
#    _name = "purchase.order"
    _inherit = 'purchase.order.line'
    
    maple_outside_qc = fields.Boolean(string='HQ',
        related='partner_id.maple_outside_qc',                                    
        help="This is an outside of Quebec Partner.",
        store=True)    
    
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
    
    partner_phone_farm = fields.Char(
        string='Phone',
        related='partner_id.phone',
        store = True
       )
    
    owner_id = fields.Many2one(
        'res.partner', 'Owner',
        help="Default Owner")
    
    owner_ref = fields.Char(
        string='Owner',
        related='owner_id.ref'
        )
    
    