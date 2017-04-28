# -*- coding: utf-8 -*-

from openerp import models, fields, api

# modifier le contact (partner) de Odoo pour inclure sa région et son numéro FPAQ
class PickingWave(models.Model):
    _inherit = 'stock.picking.wave'
    
    qty_todo  = fields.Float(
        string='Qty todo',
        compute='_compute_qty',
        store=True)

    @api.depends('picking_ids','picking_ids.pick_qty_todo')
    def _compute_qty(self):
        for record in self:
            qty = 0
            for pick in record.picking_ids:
                qty += pick.pick_qty_todo
            record.qty_todo = qty