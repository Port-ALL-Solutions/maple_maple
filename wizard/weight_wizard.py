# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError

class MapleWeightWizard(models.TransientModel):
    _name = 'maple.weight_wizard'
#    _inherit = 'purchase.order'

    note = fields.Text('Internal Notes')
    
    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Picking Type',
        )
    
    maple_producer = fields.Many2one(
        comodel_name='res.partner',
        string= 'Producer',
        help="Producer. "
        )

    partner_fpaqCode = fields.Char(
        string='FPAQ',
        related='maple_producer.parent_id.fpaqCode'
        )
    
    partner_street = fields.Char(
        string='Address',
        related='maple_producer.street'
        )
    
    partner_city = fields.Char(
        string='City',
        related='maple_producer.city'
        )
        
    partner_state = fields.Char(
        string='Province / State',
        related='maple_producer.state_id.name'
        )

    partner_region = fields.Char(
        string='Region',
        related='maple_producer.maple_region.name',
        )
    
#    employee_id = fields.Many2one(
#        comodel_name='hr.employee',
#        string= 'Employee',
#        help="Employee. "
#ajouter domaine pour limiter aux inspecteurs
#        )
    
    date_planed = fields.Date(
        string='Date planed',
        required=True,
        index=True,
        default=fields.Date.today,
        help='Date at which weighing is planed to be done. '
        )            

    related_ids = fields.Char(
        string='Related',
        compute='_compute_related',
        )

    @api.onchange('maple_producer')
    def _compute_related(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        
        self.related_ids =  ''.join(str(e) for e in active_ids)

    @api.multi
    def create_weighing_picking(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        product_obj = self.env['product.product']

        picking_obj = self.env['stock.picking']
        picking_type_obj = self.env['stock.picking.type'].browse(self.picking_type_id.id)
        
        move_obj = self.env['stock.move']
        operation_obj = self.env['stock.pack.operation']
        operation_lot_obj = self.env['stock.pack.operation.lot']

        
#location from qunantt 
#destion from picking_type
 
        partners = []
        locations = []
        products = []
        quantity = 0.
        for record in self.env['stock.quant'].browse(active_ids):
            quantity += record.qty
            if record.producer.id not in partners:
                partners.append(record.producer.id)
            if record.location_id.id not in locations:
                locations.append(record.location_id.id)
            if record.product_id.id not in products:
                products.append(record.product_id.id)

        if not products:
             raise UserError(_("No product."))

        if len (products) > 1:
             raise UserError(_("More than one product."))
        
        if not partners:
             raise UserError(_("No producer."))

        if len (partners) > 1:
             raise UserError(_("More than one producer."))
        
        if not locations:
             raise UserError(_("No locations."))

        if len (locations) > 1:
             raise UserError(_("More than one locations."))

        picking_vals = {
            'origin': "Manualy created",
            'partner_id': False,
            'date_done': self.date_planed,
            'picking_type_id': self.picking_type_id.id,
            'move_type': 'direct',
            'note': self.note or "",
            'location_id': locations[0],
            'location_dest_id': picking_type_obj.default_location_dest_id.id,
            }
         
        picking = picking_obj.create(picking_vals)
        product = product_obj.browse(products)
        
        move_vals= {
            'picking_id': picking.id,
            'product_id': products[0],
            'name': "Manualy created",
            'product_uom_qty' : quantity,
            'product_uom' : product.uom_id.id,
            'location_id': locations[0],
            'location_dest_id': picking_type_obj.default_location_dest_id.id,
            }
            
        move = move_obj.create(move_vals)
        picking.action_confirm()
        picking.action_assign()
            
#        for record in self.env['stock.quant'].browse(active_ids):
    #            if record.state not in ('draft', 'proforma', 'proforma2'):
    #                raise UserError(_("Selected invoice(s) cannot be confirmed as they are not in 'Draft' or 'Pro-Forma' state."))
              
 #           record.action_change_test()
        return {'type': 'ir.actions.act_window_close'}
