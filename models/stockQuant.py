# -*- coding: utf-8 -*-
from openerp import models, fields, api

class containter_condition(models.Model):
    _name = 'maple.container_state'

    name = fields.Char('Containter condition', index=True, required=True)
    code = fields.Char('Container condition code', required=True, size=1, help="Short name used to that container condition. ")


class maple_control(models.Model):
    _name = 'maple.control'
    
    controler = fields.Many2one('hr.employee', string="Controled by")
    
    container_total_weight = fields.Float(
        string='Weight', 
        help='Weight of the maple container.')
    
    container_tar_weight = fields.Float(
        string='Tare', 
        help='Weight of empty container.')

    container_ownership = fields.Selection(
        [   ('A', 'Buyer'),
            ('P', 'Producer')   ], 
        string='Ownership', 
        readonly=True,
        copy=False, 
        index=True, 
        track_visibility='onchange', 
        default='P'
        )

    container_type = fields.Many2one(
        comodel_name='product.product',
        string='Container Type' 
        )

    container_state = fields.Many2one(
        comodel_name='maple.container_state',
        string='Container State',
        help="Maple Syrup Container State"
        )
    
    maple_producer = fields.Many2one(
        'res.partner', 'Producer',
        help="Producer"
        )
        
    maple_state = fields.Selection(
        [   ('ready', 'Ready to pick'),
            ('confirmed', 'Confimation for delivery'),
            ('tagged', 'Maple stock tagged'),
            ('stocked-pre', 'Maple stock before classify'),
            ('weighed', 'Maple stock as been weitgh'),
            ('classified', 'Maple stock as been classified'),
            ('rejected', 'Maple stock as rejected'),
            ('stocked-post', 'Maple stock after classify'),
            ('empty', 'Empty container'),
            ('done', 'Locked'),
            ('cancel', 'Cancelled')     ], 
        string='Status', 
        readonly=True, 
        copy=False, 
        index=True, 
        track_visibility='onchange', 
        default='ready'
        )

    maple_light = fields.Integer(
        string="Light",
        help="% of light transmission defining maple syrup color class"
        )
    
    maple_brix = fields.Float(
        string="Brix",
        help="Sugar concentration of the maple syrup in degrees Brix - °Bx - defining its color class"
        )    
     
    state = fields.Selection(
        [   ('ready', 'Ready to pick'),
            ('confirmed', 'Confimation for delivery'),
            ('tagged', 'Maple stock tagged'),
            ('stocked-pre', 'Maple stock before classify'),
            ('weighed', 'Maple stock as been weitgh'),
            ('classified', 'Maple stock as been classified'),
            ('rejected', 'Maple stock as rejected'),
            ('stocked-post', 'Maple stock after classify'),
            ('empty', 'Empty container'),
            ('done', 'Locked'),
            ('cancel', 'Cancelled')     ], 
        string='Status', 
        readonly=True, 
        copy=False, 
        index=True, 
        track_visibility='onchange', 
        default='ready'
        )
    
# modifier le contact (partner) de Odoo pour inclure sa région et son numéro FPAQ
class stockQuant(models.Model):
    _name = 'stock.quant'
    _inherit = ['stock.quant', 'maple.control']
    
    product_categ_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category', 
        related='product_id.categ_id',
        readonly=True)

    producer = fields.Many2one(
        comodel_name='res.partner',
        string='Producer', 
        related='product_id.categ_id',
        readonly=True)