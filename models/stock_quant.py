# -*- coding: utf-8 -*-
from openerp import models, fields, api

class containter_condition(models.Model):
    _name = 'maple.container_state'

    name = fields.Char('Containter condition', index=True, required=True)
    code = fields.Char('Container condition code', required=True, size=1, help="Short name used to that container condition. ")


class maple_control(models.Model):
    _name = 'maple.control'
    
    controler = fields.Many2one('hr.employee', string="Controled by")
    
    container_total_weight = fields.Float(
        string='Weight', 
        help='Weight of the maple container.')
    
    container_tar_weight = fields.Float(
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

    buyer = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer', 
        readonly=False)
    
    buyer_code = fields.Char(
        string='Buyer',
        related='buyer.ref',
        readonly=False)
    
    class_site  = fields.Char(
        string='Classification Site',
        compute="_compute_class_site",
        )
    @api.depend("container_total_weight")
    def _compute_class_site(self):
        if self.buyer_code == "SE":
            if self.location_id.location_id.name == "SENB":
                self.class_site = "SENB"
            elif self.location_id.location_id.name == "SE1":
                if self.producer.state_id.code == "QC":
                    self.class_site = "370"
                else:   
                    self.class_site = "SE1"
            else:
                if self.producer.state_id.code == "QC":
                    self.class_site = "177"
                else:   
                    self.class_site = "SE3"
        else:
            if self.location_id.location_id.name == "SENB":
                self.class_site = "LBNB"
            elif self.location_id.location_id.name == "SE1":
                if self.producer.state_id.code == "QC":
                    self.class_site = "375"
                else:   
                    self.class_site = "LB1"
            else:
                if self.producer.state_id.code == "QC":
                    self.class_site = "298"
                else:   
                    self.class_site = "LB3" 

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



