# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from datetime import date

class MapleWeighingReport(models.TransientModel):
    _name = 'maple.weighing_report_wizard'
#    _inherit = 'purchase.order'
    
    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Location',
        domain=[('id','in', [42, 48])],
        help="Select the appropriate weighing location."
        )

    reception_date = fields.Date(
        string='Date Received',
        default=date.today()
        )


    @api.multi
    def action_print(self):
       
       if not self.location_id:
           raise UserError(_('You have to select at least one location. And try again.'))

       return self.env['report'].get_action(self.location_id.id, 'maple.qweb_fpaq_reception')
        