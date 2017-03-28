# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import date

class container_condition(models.Model):
    _name = 'maple.container_state'

    name = fields.Char('Containter condition', index=True, required=True)
    code = fields.Char('Container condition code', required=True, size=1, help="Short name used to that container condition. ")


class container_materiaL(models.Model):
    _name = 'maple.container_material'

    sequence = fields.Integer('Sequence', index=True, default=100)
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

    maple_seal_no = fields.Char(
        string="Seal No.",
        compute="_compute_seal",
        help="Seal Number"
        )
    
    acer_seal_no = fields.Char(
        string='Acer Seal No.',
        help="Imported Acer Controller Seal Number"
        )

    maple_light = fields.Integer(
        string="Light",
        help="% of light transmission defining maple syrup color class"
        )
    
    maple_grade = fields.Char(
        compute='_check_change_maple_light',
        string="Grade",
        help="Maple syrup class",
        store=True
        )
    
    maple_brix = fields.Float(
        string="Brix",
        help="Sugar concentration of the maple syrup in degrees Brix - °Bx - defining its color class"
        )    
     
    maple_flavor = fields.Selection(
        [   ('CROCHET', 'CROCHET'),
            ('VR', 'VR'),
            ('NC', 'NC')   ], 
        string='Flavor', 
        help='Crochet: légère trace de goût et d’odeur indésirables; VR: Saveur et odeur désagréables - VR1, VR2, VR4, VR5; NC: Non conforme - NC1, NC2, NC3, NC4. NC5, NC6', 
        index=True,
        )
    
    maple_flaw = fields.Selection(
        [   ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6')   ], 
        string='Flaw', 
        help='1:Origine naturelle 2:Origine microbiologique 3:Origine chimique 4:Non identifié 5:Bourgeon 6:Sirop filant',
        index=True,
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
    
    maple_adjust_weight = fields.Integer(
        string="Weight Adjustment",
        compute="_compute_adjust_weight_price",
        store=True,
        help="Weight Adjustment"
        )
    
    maple_adjust_price = fields.Float(
        string="Price Adjustment",
        compute="_compute_adjust_weight_price",
        store=True,
        help="Price Adjustment"
        )

    @api.depends('acer_seal_no','controler','maple_brix') #barrelCnt, InspectNb
    def _compute_seal(self):
        employee_obj = self.env['hr.employee']
        for r in self:
            if not r.maple_seal_no:
                if r.acer_seal_no:
                    r.maple_seal_no = r.acer_seal_no
                else:
                    if r.controler and r.maple_brix != 0:
                        employee = employee_obj.browse([r.controler.id])
                        cpt = employee.barrelCnt + 1
                        employee.write({'barrelCnt':cpt})
                        ctrl_code = date.today().strftime('%y') + str(int(r.controler.inspectNb)).zfill(2) + "-" + str(cpt).zfill(5)
                        r.maple_seal_no = ctrl_code

    @api.depends('maple_brix','container_total_weight','container_tar_weight')
    def _compute_adjust_weight_price(self):
        for r in self:
            if r.maple_brix < 60.5:
                r.maple_adjust_weight = None #Non-conforme
            elif r.maple_brix > 67.:
                if r.maple_brix > 68.999:
                    brix = 68.999
                else:
                    brix = r.maple_brix
                r.maple_adjust_weight = (brix - 67.) * 0.015 * (r.container_total_weight - r.container_tar_weight)
            elif r.maple_brix < 66.:
                r.maple_adjust_weight = (r.maple_brix- 66.) * 0.015 * (r.container_total_weight - r.container_tar_weight)
            else:
                r.maple_adjust_weight = 0
            
            if r.maple_brix < 60.5 or r.maple_brix > 65.7:
                r.maple_adjust_price = 0
            elif r.maple_brix <= 63.4:
                r.maple_adjust_price = -0.2
            else:
                r.maple_adjust_price = -0.1
        
#    La pesanteur initiale du Produit en Baril est révisée à la hausse pour le Produit en Baril d'une densité supérieure à 67° Brix,
#    de 0,15 % par dixième de degré Brix, jusqu'à un maximum de 68,999° Brix et est révisée à la baisse pour une densité inférieure à 66° Brix,
#    de 0,15 % par dixième de degré Brix. Au surplus, pour le Produit dont la densité se situe entre 63,5° et 65,7° Brix, le prix est inférieur
#    de 0,10 $/livre par classe selon la grille des prix minimums applicables. Pour le Produit en Baril dont la densité se situe entre 60,5° et 63,4° Brix,
#    le prix est inférieur de 0,20 $/livre par classe selon la grille des prix par classe prévue à la Convention. Enfin, le Produit en Baril dont la densité
#    est inférieure à 60,5° Brix est considéré (NC).


    @api.onchange('container_type') # if these fields are changed, call method
    def check_change_container_type(self):
        self.container_tar_weight = self.container_type.weight

    @api.onchange('maple_light') # if these fields are changed, call method
    def _check_change_maple_light(self):
        for control in self:
            if control.maple_light > 0:
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
    
    class_site  = fields.Char(
        string='Classification Site',
        compute="_compute_class_site",
        )
    @api.depends("container_total_weight")
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