# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from datetime import date

class MapleClassifAcerProducerReport(models.TransientModel):
    _name = 'maple.print_classif_acer_wizard'
#    _inherit = 'purchase.order'
    
    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Location',
        domain=[('id','in', [43, 44, 49])],
        help="Select the appropriate weighing location."
        )

    @api.multi
    def action_print(self):
      
        if not self.location_id:
            raise UserError(_('You have to select at least one location. And try again.'))
        
        return self.env['report'].get_action(self.location_id.id, 'maple.qweb_classif_acer_producer')
