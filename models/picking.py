# -*- coding: utf-8 -*-

from openerp import models, fields, api

# modifier le contact (partner) de Odoo pour inclure sa région et son numéro FPAQ
class Picking(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'
    
    owner_id = fields.Many2one(
        'res.partner', 'Owner',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        domain=[('maple_buyer', '=', True)],        
        help="Default Owner")