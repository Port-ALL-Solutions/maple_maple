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
        
        data = {}
        data['ids'] = self.location_id.id
        data['model'] = 'stock.location'
#        data['form'] = self.read(['date_from', 'date_to', 'journal_ids', 'target_move'])[0]
        
#        data = self.location_id.id
#        return self.env['report'].render('account_report.payment_report', data)
        return {
           'type': 'ir.actions.report.xml',
           'report_name': 'maple.qweb_fpaq_reception',
           'data': data
           }
        