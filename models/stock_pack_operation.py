# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

#from odoo.addons import decimal_precision as dp
#from odoo.exceptions import UserError, ValidationError
#from odoo.tools.float_utils import float_round, float_compare


class PackOperation(models.Model):
    _inherit = "stock.pack.operation"

    @api.multi
    def do_all(self):
        for lot in self.pack_lot_ids:
            lot.write({'qty': 1})
        self.write({'qty_done': sum(operation_lot.qty for operation_lot in self.pack_lot_ids)})
#        return {'type': 'ir.actions.act_window_close'}
   
    @api.multi
    def do_none(self):
        for lot in self.pack_lot_ids:
            lot.write({'qty': 0})
        self.write({'qty_done': sum(operation_lot.qty for operation_lot in self.pack_lot_ids)})
#        return {'type': 'ir.actions.act_window_close'}
