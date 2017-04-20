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
    
    pick_qty_done = fields.Float(
        string='Qty done',
        compute='_compute_qty',
        store=True)

    pick_qty_todo  = fields.Float(
        string='Qty todo',
        compute='_compute_qty',
        store=True)

    daily_in_cpt = fields.Char(
        string='Daily Cpt',
        compute='_compute_daily_id',
        )
    
    partner_ref = fields.Char(
        string='Producer',
        compute='_partner_ref',
        store=True
        )  
    
    daily_in_sequence = fields.Char('Daily Id')
     
    @api.depends('partner_id')
    def _partner_ref(self):
        for record in self:
            if record.partner_id.ref:
                record.partner_ref = record.partner_id.ref
            else:
                record.partner_ref = record.partner_id.parent_id.ref
            
    @api.depends('pack_operation_ids','pack_operation_ids.product_qty','pack_operation_ids.qty_done')
    def _compute_qty(self):
        for record in self:
            packs = record.pack_operation_ids
            qty_done = 0
            qty_todo = 0
            
            for pack in packs :
                qty_todo += pack.product_qty
                qty_done += pack.qty_done
            record.pick_qty_done = qty_done
            record.pick_qty_todo = qty_todo
            
    @api.depends('daily_in_sequence')
    def _compute_daily_id(self):
        for record in self:
            if record.daily_in_sequence:
                record.daily_in_cpt = record.daily_in_sequence[-2:]
            else:
                record.daily_in_cpt = ''