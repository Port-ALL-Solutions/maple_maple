# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from datetime import date

class MaplePrintReceptionLabel(models.TransientModel):
    _name = 'maple.print_reception_labels_wizard'
#    _inherit = 'purchase.order'
    
    picking = fields.Many2one(
        comodel_name='stock.picking',
        string='Picking',
        domain=[('picking_type_id','in', [1,13,25])],
        help="Select the picking to print labels for."
        )


    @api.multi
    def action_print(self):
      
        if not self.picking:
            raise UserError(_('You have to select at least one picking. And try again.'))

        for ops in self.picking.pack_operation_product_ids:
            for lot in ops.pack_lot_ids:
                for quant in lot.lot_id.quant_ids:
                    quant.write({
                        'reception_labels_printed':True,
                        })
        
        return self.env['report'].get_action(self.picking.id, 'maple.view_reception_labels')