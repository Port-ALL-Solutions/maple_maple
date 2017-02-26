# -*- coding: utf-8 -*-

from openerp import models, fields, api
from odoo.tools.yaml_tag import record_constructor

# modifier le contact (partner) de Odoo pour inclure sa région et son numéro FPAQ
class stockQuant(models.Model):
    _name = 'stock.quant'
    _inherit = 'stock.quant'
        
    product_categ_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category', 
        related='product_id.categ_id',
        readonly=True)
    
    container_tar_weight = fields.Float(
        string='Tar weight', 
        help='Weight of the container when empty. ')
    
    container_state = fields.Selection(
        selection=[  
            ('O', 'Good condition'),
            ('L', 'Slightly bumped'),
            ('B', 'Bumped'),
            ('T', 'Very bumped'),
            ('R', 'Rusty'),
            ('P', 'Punctured'),
            ('N', 'Non compliant')
            ],
        string='Container Type',
        help="Maple Syrup Container Type")
    