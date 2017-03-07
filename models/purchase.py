# -*- coding: utf-8 -*-
from openerp import models, fields, api
class PurchaseOrder(models.Model):
#    _name = "purchase.order"
    _inherit = 'purchase.order'
    
    location_id = fields.Many2one(
        'stock.location', 'Destination Location',
        index=True, required=True, states={'done': [('readonly', True)]},
        help="Sets a destination location where to put the stock after reception.")