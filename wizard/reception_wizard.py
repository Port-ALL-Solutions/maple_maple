# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import date

class MapleReception(models.TransientModel):
    _name = 'maple.reception'
#    _inherit = 'purchase.order'
    
    picking = fields.Many2one(
        comodel_name='stock.picking',
        string='Reception',
        domain=[('state','=', 'assigned')],        
        help="Stock picking to receive. "
        )

    from_location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Origin',
        related='picking.location_id',
        help="Sets a destination location where to put the stock come from."
        )

    to_location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Destination',
        related='picking.location_dest_id',
        help="Sets a destination location where to put the stock after reception."
        )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='From',
        related='picking.partner_id',
        )

    partner_fpaqCode = fields.Char(
        string='FPAQ',
        related='partner_id.parent_id.fpaqCode'
        )
    
    partner_street = fields.Char(
        string='Address',
        related='partner_id.street'
        )
    
    partner_city = fields.Char(
        string='City',
        related='partner_id.city'
        )
        
    partner_state = fields.Char(
        string='Province / State',
        related='partner_id.state_id.name'
        )

    partner_region = fields.Char(
        string='Region',
        related='partner_id.maple_region.name',
        )
    
    owner_id = fields.Many2one(
        comodel_name='res.partner',
        string='For',
        related='picking.owner_id',
        )
    
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        related='picking.pack_operation_ids.product_id'
        )
    
    qty_container = fields.Integer(
        string='Quantity',
        help='Number of container(s) received'
        )

    qty_ordered = fields.Float(
        string='Qty ordered',
        related='picking.pack_operation_ids.ordered_qty',
        help='Number of container(s) ordered'
        )

    validate_each = fields.Boolean(
        string='Validate each',
        default=False,
        help='Do you need more confirmation than job done. '
        )
    
    @api.multi
    def action_maple_reception(self):
        
        operation_lot_obj = self.env['stock.pack.operation.lot']
        #picking_obj = self.env['stock.picking']
        date_range_obj = self.env['ir.sequence.date_range']
        
        # Doit ont tous les checker un à un 
        if self.validate_each:
            placed_qty = 0
        else:
            placed_qty = 1
        
#        pickings = picking_obj.browse(self.picking)
        pickings = self.picking
        if len(pickings) == 1:
            my_sequence = self.env['ir.sequence'].next_by_code('stock.daily_in')
#            pickings.write({'daily_in_sequence':my_sequence})
            pickings.daily_in_sequence = my_sequence

            pack_operations = pickings.pack_operation_ids
#            my_sequence = self.pool['ir.sequence'].get(cr, uid, 'stock.daily_in')
#            for move in pickings.move_lines:
#                my_sequence = self.env['ir.sequence'].next_by_code('stock.daily_in')
#                move.daily_in_sequence = my_sequence
#            daily_cpt = move.daily_in_cpt          
            for operation in pack_operations:
                product = operation.product_id
                if product.order_create_serial:
                    for x in range(0, int(self.qty_container)):
                        if pickings.purchase_id.partner_id.ref :
                            ref_name = pickings.purchase_id.partner_id.ref
                        else:
                            ref_name = pickings.purchase_id.partner_id.parent_id.ref
                        ref_date = date.today().strftime('%Y%m%d')
#                        ref_day_seq = pickings.
                        operation_lot_vals = {
                            'operation_id':operation.id,
                            'lot_name':ref_name + "-" + ref_date + "-" + pickings.daily_in_cpt + "-" + str(x+1).zfill(3) + "-" +  str(int(self.qty_container)).zfill(3),                           
                            'qty':placed_qty,
                            'qty_todo':1
                            }
                        operation_lot = operation_lot_obj.create(operation_lot_vals)
                                            
        return(
            { 'type':'ir.actions.client', 'tag':'reload'}
            )

    @api.onchange('picking') # if these fields are changed, call method
    def check_change(self):
        self.qty_container = self.qty_ordered
        
    
