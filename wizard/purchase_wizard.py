# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import date
class MaplePurchaseOrder(models.TransientModel):
    _name = 'maple.purchase.order'
#    _inherit = 'purchase.order'
    
    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Destination Location',
        index=True,
        required=True,
        help="Sets a destination location where to put the stock after reception."
        )
    
    organic = fields.Boolean(
        string='Organic',
        help='Organic Maple Syrup'
        )
    
    qty_barrel = fields.Integer(
        string='Barrels',
        help='Number of barrel(s)'
        )
    
    qty_tote = fields.Integer(
        string='Totes',
        help='Number of tote(s)'
        )
    
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Producer',
        required=True,
        index=True
        )
    
    owner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer',
        required=True,
        index=True
        )
    
    date_order = fields.Datetime(
        string='Order Date',
        required=True,
        index=True,
        default=fields.Datetime.now
        )
    
    @api.multi
    def action_maple_purchase(self):
        product_obj = self.env['product.product']
        purchase_obj = self.env['purchase.order']
        purchase_line_obj = self.env['purchase.order.line']
        
        purchase_vals = {
            'partner_id':self.partner_id.id,
            'date_planned':self.date_order,
            'location_id':self.location_id.id
        }
        
        purchase_order = purchase_obj.create(purchase_vals)
        
        if self.qty_barrel > 0 :
            if self.organic :
                product_code = 'BB'
            else :
                product_code = 'BR'
            
            product = product_obj.search([('default_code','=',product_code)])
            
            purchase_barrel_vals = {
                'product_id':product.id,
                'product_qty':self.qty_barrel,
                'order_id':purchase_order.id,
                'name':purchase_order.name + product_code,
                'product_uom':product.uom_id.id,
                'date_planned':self.date_order,
                'price_unit':product.price # champ de prchase_order_line : champs de product_template
            }
            
            purchase_order_line = purchase_line_obj.create(purchase_barrel_vals)
            
        if self.qty_tote > 0 :
            if self.organic :
                product_code = 'TB'
            else :
                product_code = 'TR'
            
            product = product_obj.search([('default_code','=',product_code)])
            
            purchase_tote_vals = {
                'product_id':product.id,
                'product_qty':self.qty_tote,
                'order_id':purchase_order.id,
                'name':purchase_order.name + product_code,
                'product_uom':product.uom_id.id,
                'date_planned':self.date_order,
                'price_unit':product.price # champ de purchase_order_line : champs de product_template
            }
            
            purchase_order_line = purchase_line_obj.create(purchase_tote_vals)
            
    