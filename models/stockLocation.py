# -*- coding: utf-8 -*-
from openerp import models, fields, api
from odoo.tools.yaml_tag import record_constructor

# modifier le contact (partner) de Odoo pour inclure sa région et son numéro FPAQ
class stockLocation(models.Model):
    _name = 'stock.location'
    _inherit = 'stock.location'
        
    maxItem = fields.Integer(
        string="Maximum capacity",
        help="The maximum count of product that can be put in that location. ")
    
    spaceLeft = fields.Integer(
        string="Product Space Left",
        help="The empty product space in that location. ")
    
    purchase_lines = fields.One2many(           
        comodel_name='purchase.order.line', 
        inverse_name='location_id',
        string="Purchases",
        help='Stock purchase planed for that location. ')
    
    qty_purchased  = fields.Float(
        string='Quantity Purchased',
        compute='_compute_qty_purchase',
        store=True
        )
    
    @api.depends('purchase_lines')
    def _compute_qty_purchase(self):
        for record in self:
            qty = 0 
            for line in record.purchase_lines:
                if line.product_id.maple_container:
                    qty += line.product_qty          
            record.qty_purchased = qty