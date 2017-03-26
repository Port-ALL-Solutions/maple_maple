# -*- coding: utf-8 -*-
from openerp import models, fields, api

class container_condition(models.Model):
    _name = 'maple.container_state'

    name = fields.Char('Containter condition', index=True, required=True)
    code = fields.Char('Container condition code', required=True, size=1, help="Short name used to that container condition. ")


class container_materiaL(models.Model):
    _name = 'maple.container_material'

    name = fields.Char('Container material', index=True, required=True)
    code = fields.Char('Container material code', required=True, size=1, help="Specifies the material of the container. ")

class container_owner_type(models.Model):
    _name = 'maple.container_owner_type'

    name = fields.Char('Container Owner Type', index=True, required=True)
    code = fields.Char('Container owner code', required=True, size=1, help="Specifies the type of owner. [A:Buyer, P:Producer]. ")


class maple_control(models.Model):
    _name = 'maple.control'
    
    controler = fields.Many2one('hr.employee', string="Controled by")
    
    container_total_weight = fields.Integer(
        string='Weight', 
        help='Weight of the maple container.')
    
    container_tar_weight = fields.Integer(
        string='Tare', 
        help='Weight of empty container.')

    container_serial = fields.Char(
        string='Barel Id', 
        index=True 
        )

    container_ownership = fields.Selection(
        [   ('A', 'Buyer'),
            ('P', 'Producer')   ], 
        string='Ownership', 
        readonly=True,
        copy=False, 
        index=True, 
        track_visibility='onchange', 
        default='P'
        )

    container_type = fields.Many2one(
        comodel_name='product.product',
        string='Container Type' 
        )

    container_state = fields.Many2one(
        comodel_name='maple.container_state',
        string='Container State',
        help="Maple Syrup Container State"
        )
    
    maple_producer = fields.Many2one(
        'res.partner', 'Producer',
        help="Producer"
        )

    maple_state = fields.Selection(
        [   ('ready', 'Ready to pick'),
            ('confirmed', 'Confimation for delivery'),
            ('tagged', 'Maple stock tagged'),
            ('stocked-pre', 'Maple stock before classify'),
            ('weighed', 'Maple stock as been weitgh'),
            ('classified', 'Maple stock as been classified'),
            ('rejected', 'Maple stock as rejected'),
            ('stocked-post', 'Maple stock after classify'),
            ('empty', 'Empty container'),
            ('done', 'Locked'),
            ('cancel', 'Cancelled')     ], 
        string='Status',         
        readonly=True, 
        copy=False, 
        index=True, 
        track_visibility='onchange', 
        default='ready'
        )

    maple_light = fields.Integer(
        string="Light",
        help="% of light transmission defining maple syrup color class"
        )
    
    maple_grade = fields.Char(
        compute='check_change_maple_light',
        string="Class",
        help="Maple syrup class",
        readonly=True
        )
    
    maple_brix = fields.Float(
        string="Brix",
        help="Sugar concentration of the maple syrup in degrees Brix - °Bx - defining its color class"
        )    
     
    state = fields.Selection(
        [   ('ready', 'Ready to pick'),
            ('confirmed', 'Confimation for delivery'),
            ('tagged', 'Maple stock tagged'),
            ('stocked-pre', 'Maple stock before classify'),
            ('weighed', 'Maple stock as been weitgh'),
            ('classified', 'Maple stock as been classified'),
            ('rejected', 'Maple stock as rejected'),
            ('stocked-post', 'Maple stock after classify'),
            ('empty', 'Empty container'),
            ('done', 'Locked'),
            ('cancel', 'Cancelled')     ], 
        string='Status', 
        readonly=True, 
        copy=False, 
        index=True, 
        track_visibility='onchange', 
        default='ready'
        )

    @api.onchange('container_type') # if these fields are changed, call method
    def check_change_container_type(self):
        self.container_tar_weight = self.container_type.weight

    @api.onchange('maple_light') # if these fields are changed, call method
    def check_change_maple_light(self):
        for control in self:
            if control.maple_brix > 0:
                if control.maple_light <= 25 :
                    control.maple_grade = 'TF'
                elif control.maple_light < 50 :
                    control.maple_grade = 'FO'
                elif control.maple_light < 75 :
                    control.maple_grade = 'AM'
                else :
                    control.maple_grade = 'DO'
            else:
                control.maple_grade = ''
        
#        partner_obj = self.env['res.partner']
#        partner = partner_obj.browse([self.partner_id.id])
#        owner = partner_obj.browse([partner.default_owner_id.id])

#        if self.maple_bio_state in ['P','V']:
#            self.maple_type = "B"
#        else:
#            self.maple_type = "R"
#        self.owner_id = owner    
# modifier le contact (partner) de Odoo pour inclure sa région et son numéro FPAQ



class stockQuant(models.Model):
    _name = 'stock.quant'
    _inherit = ['stock.quant', 'maple.control']
    
    product_categ_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category', 
        related='product_id.categ_id',
        readonly=True)

    producer = fields.Many2one(
        comodel_name='res.partner',
        string='Producer', 
        readonly=False)

    producer_name = fields.Char(
        string='Producer',
        related='producer.name',
        readonly=False)
    
    tmp_material = fields.Many2one(
        comodel_name='maple.container_material',
        string='Type', 
        readonly=False)
    
    tmp_owner = fields.Many2one(
        comodel_name='maple.container_owner_type',
        string='Owner', 
        readonly=False)
    
    tmp_tare = fields.Integer(
        string='Tare',
        readonly=False)

    buyer = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer', 
        readonly=False)
    
    buyer_code = fields.Char(
        string='Buyer',
        related='buyer.ref',
        readonly=False)

    def _quant_create_from_move(self, qty, move, lot_id=False, owner_id=False, src_package_id=False, dest_package_id=False, force_location_from=False, force_location_to=False):
        quant = super(stockQuant, self)._quant_create_from_move(qty, move, 
                                                                lot_id=lot_id, 
                                                                owner_id=move.picking_partner_id.id, 
                                                                src_package_id=src_package_id, 
                                                                dest_package_id=dest_package_id, 
                                                                force_location_from=force_location_from, 
                                                                force_location_to=force_location_to)
        quant.sudo().write({
            'producer': move.picking_partner_id.id,
            'buyer': move.purchase_line_id.owner_id.id
            })
        return quant 

    @api.constrains('container_total_weight','tmp_tare','container_serial','tmp_material','container_state','tmp_owner')
    def _constrains_weighing_line(self):
        for r in self:
            if r.container_total_weight:
                if r.container_total_weight < 400:
                    raise models.ValidationError('Weight value too low')
                elif r.container_total_weight > 5000:
                    raise models.ValidationError('Weight value too high')
                elif not r.tmp_tare:
                    raise models.ValidationError('You must enter Tare value')
                elif not r.container_serial:
                    raise models.ValidationError('You must enter container serial number')
                elif not r.tmp_material:
                    raise models.ValidationError('You must select barrel material')
                elif not r.container_state:
                    raise models.ValidationError('You must select barrel state')
                elif not r.tmp_owner:
                    raise models.ValidationError('You must select barrel owner')

            if r.tmp_tare:
                if r.tmp_tare < 2:
                    raise models.ValidationError('Tare value too low')
                elif r.tmp_tare > 200:
                    raise models.ValidationError('Tare value too high')
                elif r.tmp_tare >= r.container_total_weight:
                    raise models.ValidationError('Tare can\'t be equal to or higher than total weight')


#    @api.onchange('history_ids') # if these fields are changed, call method
#    def check_change(self):
#        moves = self.history_ids
#        for move in moves:
#            if move.partner_id:
#                self.producer = move.partner_id
        
#    def _quant_create_from_move(self, qty, move, lot_id=False, owner_id=False,
#                                src_package_id=False, dest_package_id=False,
#                                force_location_from=False, force_location_to=False):

        
#        result = super(stockQuant, self)._quant_create_from_move(qty, move, lot_id, owner_id,
#                                src_package_id, dest_package_id,
#                                force_location_from, force_location_to)

#        result = super(stockQuant, self)._quant_create_from_move(qty, move, lot_id=False, owner_id=move.picking_partner_id.id,
#                                src_package_id=False, dest_package_id=False,
#                                force_location_from=False, force_location_to=False)

        
#        return result



