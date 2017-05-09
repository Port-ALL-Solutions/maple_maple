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

    producer_present = fields.Boolean(
        string="Producer present",
        )
 
    @api.multi
    def action_print(self):
      
        if not self.location_id:
            raise UserError(_('You have to select at least one location. And try again.'))
        
        if self.reception_date:
            quants = self.env['stock.quant'].search([('location_id','=',self.location_id.id)])
            for quant in quants:
                quant.write({
                    'maple_reception_date':self.reception_date,
                    'producer_present':self.producer_present
                    })
        
        return self.env['report'].get_action(self.location_id.id, 'maple.qweb_fpaq_reception')
