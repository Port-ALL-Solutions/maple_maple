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