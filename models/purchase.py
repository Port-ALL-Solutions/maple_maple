# -*- coding: utf-8 -*-
from openerp import models, fields, api
class PurchaseOrder(models.Model):
#    _name = "purchase.order"
    _inherit = 'purchase.order'

    location_id = fields.Many2one(
        'stock.location', 'Destination Location',
        index=True, required=True, states={'done': [('readonly', True)]},
        help="Sets a destination location where to put the stock after reception.")

    owner_id = fields.Many2one(
        'res.partner', 'Owner',
        domain=[('maple_buyer', '=', True)],
        help="Default Owner")

    owner_ref = fields.Char(
        string='Owner',
        related='owner_id.ref',
        store=True
        )

    maple_outside_qc = fields.Boolean(string='HQ',
        related='partner_id.maple_outside_qc',
        help="This is an outside of Quebec Partner. ",
        store=True)

    partner_fpaqCode = fields.Char(
        string='FPAQ',
        related='partner_id.fpaqCode'
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
        store = True
        )

    qty_container = fields.Float(
        string='Quantity',
        compute='_compute_qty_container',
        store=True
        )

    qty_received = fields.Float(
        string='Quantity received'
        )


    maple_type = fields.Selection([
        ('B', 'Organic'),
        ('R', 'Regular')],
        help="Maple Container Type. "
        )

    @api.depends('order_line')
    def _compute_qty_container(self):
        for record in self:
            qty = 0 
            for line in record.order_line:
                if line.product_id.maple_container:
                    qty += line.product_qty
            record.qty_container = qty


#    @api.multi
#    def _get_destination_location(self):
#        result = super(PurchaseOrder, self)._get_destination_location()
#        if self.location_id:
#            return self.location_id.id
#        return result


# WORK FINE TO CREATE SERIAL ON PURCHASE ORDER BUT NOT NEEDED
#    @api.multi
#    def _create_picking(self):
#        operation_lot_obj = self.env['stock.pack.operation.lot']
#
#        result = super(PurchaseOrder, self)._create_picking()
#
#        pickings = self.picking_ids
#        if len(pickings) == 1:
#            pack_operations = pickings.pack_operation_ids
#            for operation in pack_operations:
#                product = operation.product_id
#                if product.order_create_serial:
#                    for x in range(0, int(operation.ordered_qty)):
#                        operation_lot_vals = {
#                            'operation_id':operation.id,
#                            'lot_name':pickings.origin + "-"+ str(x+1) + "/" +  str(int(operation.ordered_qty)),                           
#                            'qty':0,
#                            'qty_todo':1
#                            }
#                        operation_lot = operation_lot_obj.create(operation_lot_vals)
#
#        return result

    @api.multi
    def _create_picking(self):
#
        result = super(PurchaseOrder, self)._create_picking()
#
        pickings = self.picking_ids
        for picking in pickings:
            start_moves = picking.move_lines
            for final_move in start_moves:
                while final_move.move_dest_id : 
                    final_move =final_move.move_dest_id
                final_move.location_dest_id = self.location_id.id
                final_picking = final_move.picking_id
                final_picking.location_dest_id = self.location_id.id
        return result
                 
            
#        if len(pickings) == 1:
#            pack_operations = pickings.pack_operation_ids
#            for operation in pack_operations:
#                product = operation.product_id
#                if product.order_create_serial:
#                    for x in range(0, int(operation.ordered_qty)):
#                        operation_lot_vals = {
#                            'operation_id':operation.id,
#                            'lot_name':pickings.origin + "-"+ str(x+1) + "/" +  str(int(operation.ordered_qty)),                           
#                            'qty':0,
#                            'qty_todo':1
#                            }
#                        operation_lot = operation_lot_obj.create(operation_lot_vals)
#
#        return result

class PurchaseOrderLine(models.Model):
#    _name = "purchase.order"
    _inherit = 'purchase.order.line'

    maple_outside_qc = fields.Boolean(string='HQ',
        related='partner_id.maple_outside_qc',
        help="This is an outside of Quebec Partner. ",
        store=True
        )

    partner_fpaqCode = fields.Char(
        string='FPAQ',
        related='partner_id.fpaqCode'
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
        store = True
        )

#    devra être remplacé par l'actuel buyer
    partner_default_buyer = fields.Char(
        string='Buyer',
        related='partner_id.default_owner_id.ref',
        store = True
        )

#    partner_phone_farm = fields.Char(
#        string='Phone',
#        related='partner_id.phone',
#        store = True
#       )

    owner_id = fields.Many2one(
        'res.partner', 'Owner',
        help="Default Owner"
        )

    owner_ref = fields.Char(
        string='Owner',
        related='owner_id.ref'
        )

    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Destination Location',
        index=True, 
        help="Sets a destination location where to put the stock after reception."
        )
