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
        domain=[('location_id', '=', 15)],
        help="Sets a destination location where to put the stock after reception."
        )
    
    organic = fields.Boolean(
        string='Organic',
        help='Organic Maple Syrup'
        )
    
    maple_type = fields.Selection([
        ('B', 'Organic'),
        ('R', 'Regular')],
        help="Maple Container Type. "
        ) 
    
    container_type = fields.Selection([
        ('B', 'Barrel'),
        ('T', 'Tote')],
        default='B',
        help="Maple Container Type. "
        ) 

    qty_container = fields.Integer(
        string='Barrels',
        help='Number of container(s)'
        )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Producer',
        domain=[('maple_farm', '=', True)],
        required=True,
        index=True
        )
    
    owner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer',
        domain=[('maple_buyer', '=', True)],
        required=True,
        index=True
        )
    
    date_order = fields.Datetime(
        string='Order Date',
        required=True,
        index=True,
        default=fields.Datetime.now
        )
    
    date_planed = fields.Datetime(
        string='Planed Date',
        index=True
        )
    
    partner_fpaqCode = fields.Char(
        string='FPAQ',
        related='partner_id.parent_id.fpaqCode'
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
    
    maple_bio_check_on_order = fields.Boolean(string="Must Confirm", 
        related='partner_id.maple_bio_check_on_order',                                              
        help="The maple syrup producer must specify Organic or Regular Order. "        
        )
    
    maple_bio_state = fields.Selection([
        ('N', 'None'),
        ('P', 'Pending'),
        ('V', 'Valid')],
        string='Organic Certs',
        related='partner_id.maple_bio_state'
        )
    
    @api.multi
    def action_maple_purchase(self):
        product_obj = self.env['product.product']
        purchase_obj = self.env['purchase.order']
        purchase_line_obj = self.env['purchase.order.line']
                
        purchase_vals = {
            'partner_id':self.partner_id.id,
            'date_planned':self.date_order,
            'location_id':self.location_id.id,
            'owner_id':self.owner_id.id,
            'state':'purchase'
        }
  
        purchase_order = purchase_obj.create(purchase_vals)
             
        if self.qty_container > 0 :
          
            product_code = self.container_type + self.maple_type
            product = product_obj.search([('default_code','=',product_code)])
            
            purchase_barrel_vals = {
                'product_id':product.id,
                'product_qty':self.qty_container,
                'order_id':purchase_order.id,
                'owner_id':self.owner_id.id,
                'name':purchase_order.name + product_code,
                'product_uom':product.uom_id.id,
                'date_planned':self.date_order,
                'price_unit':product.price # champ de prchase_order_line : champs de product_template                
            }
            
            purchase_order_line = purchase_line_obj.create(purchase_barrel_vals)
                        
        return(
            { 'type':'ir.actions.client', 'tag':'reload'}
            )
            
    @api.onchange('partner_id') # if these fields are changed, call method
    def check_change(self):
        if self.maple_bio_state in ['P','V']:
            self.organic = True
        else:
            self.organic = False