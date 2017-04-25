# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import date

class container_condition(models.Model):
    _name = 'maple.container_state'
    _order = 'sequence'

    sequence = fields.Integer('Sequence', index=True, default=100)
    name = fields.Char('Containter condition', index=True, required=True)
    code = fields.Char('Container condition code', required=True, size=1, help="Short name used to that container condition. ")

class flavors(models.Model):
    _name = 'maple.flavors'
    _order = 'sequence'

    sequence = fields.Integer('Sequence', index=True, default=100)
    name = fields.Char('Flavor', index=True, required=True)
    code = fields.Char('Flavor code', required=True, size=1, help="Specifies the flavor default of maple. ")


class flaws(models.Model):
    _name = 'maple.flaws'
    _order = 'sequence'

    sequence = fields.Integer('Sequence', index=True, default=100)
    name = fields.Char('Flaw', index=True, required=True)
    code = fields.Char('Flaw code', required=True, size=1, help="Specifies the code of the default of maple. ")


class container_materiaL(models.Model):
    _name = 'maple.container_material'
    _order = 'sequence'

    sequence = fields.Integer('Sequence', index=True, default=100)
    name = fields.Char('Container material', index=True, required=True)
    code = fields.Char('Container material code', required=True, size=1, help="Specifies the material of the container. ")

class container_owner_type(models.Model):
    _name = 'maple.container_owner_type'

    name = fields.Char('Container Owner Type', index=True, required=True)
    code = fields.Char('Container owner code', required=True, size=1, help="Specifies the type of owner. [A:Buyer, P:Producer]. ")


class maple_control(models.Model):
    _name = 'maple.control'
    
    controler = fields.Many2one('hr.employee', string="Controlled by", related='')
    
    container_total_weight = fields.Integer(
        string='Weight', 
        help='Weight of the maple container.')
    
    container_tar_weight = fields.Integer(
        string='Tare', 
        help='Weight of empty container.')

    maple_net_weight = fields.Integer(
        string="Net Weight",
        compute="_compute_line_data",
        store=True,
        help="Maple syrup net weight calculation. "
        )
    
    maple_payable_weight = fields.Integer(
        string="Adjusted (payable) Net Weight",
        compute="_compute_line_data",
        store=True,
        help="Adjusted maple syrup net weight calculation, payable to the producer. "
        )

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
    
    container_state_code = fields.Char(
        string='One-char Container State',
        help="Maple Syrup Container one-character State",
        related='container_state.code'
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
#        compute="_compute_seal",
        help="Seal Number",
#        store=True
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
        compute='_compute_line_data',
        string="Grade",
        help="Maple syrup class",
        store=True
        )
    
    maple_brix = fields.Float(
        string="Brix",
        help="Sugar concentration of the maple syrup in degrees Brix - °Bx - defining its color class"
        )    
     
    maple_flavor = fields.Many2one(
        comodel_name='maple.flavors',
        string='Flavor', 
        help='Crochet: légère trace de goût et d’odeur indésirables; VR: Saveur et odeur désagréables - VR1, VR2, VR4, VR5; NC: Non conforme - NC1, NC2, NC3, NC4. NC5, NC6', 
        index=True,
        )
    
    maple_flaw = fields.Many2one(
        comodel_name='maple.flaws',
        string='Flaw',
        help='1:Origine naturelle 2:Origine microbiologique 3:Origine chimique 4:Non identifié 5:Bourgeon 6:Sirop filant',
        index=True,
        )
    
    maple_clarity = fields.Integer(
        string="Clarity",
        help="Maple syrup Clarity. "
        )
    
    maple_si = fields.Float(
        string="Silicium",
        help="Maple syrup Silicium content. "
        )
    
    maple_ph = fields.Integer(
        string="pH",
        help="Maple syrup pH. "
        )
    
    maple_iodine = fields.Integer(
        string="Iodine",
        help="Maple syrup Iodine content. "
        )
    
    maple_na = fields.Integer(
        string="Sodium",
        help="Maple syrup Sodium content. "
        )
    
    maple_pb = fields.Integer(
        string="Lead",
        help="Maple syrup Lead content. "
        )
    
    maple_retained = fields.Boolean(
        string="Retained Barrel",
        help="Retained Barrel. "
        )
    
    maple_special_test = fields.Char(
        string="SpecialTest",
        help="SpecialTest. "
        )
    
    classif_revision = fields.Boolean(
        string="Classification under Revision",
        help="Classification under Revision. "
        )
    
    supervised = fields.Boolean(
        string="Supervised",
        help="Supervised. "
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
        compute="_compute_line_data",
        store=True,
        help="Weight Adjustment"
        )
    
    maple_adjust_price = fields.Float(
        string="Price Adjustment",
        compute="_compute_line_data",
        store=True,
        help="Price Adjustment"
        )
    
    location_dest_id = fields.Many2one(
        comodel_name='stock.location',
        string='Destination Location',
#        required=True, 
        help="Location where this container will be stocked after classification. "
        )
    
    product_code = fields.Char(
        string="Internal Product Code",
        compute="_compute_line_data",
        store=True,
        help="Find the corresponding internal product code. "
        )
          
    
    
    
    
    
    @api.depends('maple_light','maple_brix') # if these fields are changed, call method
    def _compute_line_data(self):
        for r in self:

#            Grade calculation based on light value
            if r.maple_light > 0:
                if r.maple_light <= 25 :
                    r.maple_grade = 'TF'
                elif r.maple_light < 50 :
                    r.maple_grade = 'FO'
                elif r.maple_light < 75 :
                    r.maple_grade = 'AM'
                else :
                    r.maple_grade = 'DO'
            else:
                r.maple_grade = ''

#            Weight and Price adjustments calculation based on Brix value
            if r.maple_brix:
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
#                    La pesanteur initiale du Produit en Baril est révisée à la hausse pour le Produit en Baril d'une densité supérieure à 67° Brix,
#                    de 0,15 % par dixième de degré Brix, jusqu'à un maximum de 68,999° Brix et est révisée à la baisse pour une densité inférieure à 66° Brix,
#                    de 0,15 % par dixième de degré Brix. Au surplus, pour le Produit dont la densité se situe entre 63,5° et 65,7° Brix, le prix est inférieur
#                    de 0,10 $/livre par classe selon la grille des prix minimums applicables. Pour le Produit en Baril dont la densité se situe entre 60,5° et 63,4° Brix,
#                    le prix est inférieur de 0,20 $/livre par classe selon la grille des prix par classe prévue à la Convention. Enfin, le Produit en Baril dont la densité
#                    est inférieure à 60,5° Brix est considéré (NC).

#            Net weight calculation
            if r.container_total_weight > 0 and r.tmp_tare > 0:
                r.maple_net_weight = r.container_total_weight - r.tmp_tare

#            Payable weight calculation    
            if r.maple_adjust_weight != 0:
                r.maple_payable_weight = r.maple_net_weight + r.maple_adjust_weight
            elif r.maple_net_weight > 0:
                r.maple_payable_weight = r.maple_net_weight

#            Sale Product code alculation                 
            if r.maple_grade:
                answer = ''
                answer += r.product_id.default_code[1] + r.maple_grade
                if not r.maple_flavor:
                    answer += '--'
                else:
                    if len(r.maple_flavor.name) == 2:
                        answer += r.maple_flavor.name[1]     
                    elif len(r.maple_flavor.name) > 2:
                        answer += "R"
                    if not r.maple_flaw:
                        answer += "0"
                    else:
                        if r.maple_flaw:
                            answer += r.maple_flaw.code
                if len(answer) == 5:
                    self.product_code = answer 
                    

    @api.multi
    def write(self, vals):
        if len(self) == 1:
            brix = self.maple_brix or vals.get('maple_brix')
            ctrl = self.controler.id or vals.get('controler')            

            if 'maple_seal_no' not in vals:
                if not self.maple_seal_no and brix and ctrl:
#                    if not self.maple_seal_no and (self.acer_seal_no or (brix and ctrl)):
                    employee = self.env['hr.employee'].browse([ctrl])
                    cpt = employee.barrelCnt + 1
                    employee.write({'barrelCnt':cpt})
                    vals['maple_seal_no'] = date.today().strftime('%y') + str(int(employee.inspectNb)).zfill(2) + "-" + str(cpt).zfill(5)       
            
            
            weighing_picking_type = self.env['stock.picking.type'].browse([42,48]) #se1 et senb (name) ilike (casse ou pas)
            weighing_move = self.history_ids.filtered(lambda m: m.picking_id.picking_type_id in weighing_picking_type) #[picking type = weight - identifier move de pesée dans histo quant
            if weighing_move and not ctrl and weighing_move.picking_id.tmp_controller:
                vals['controler'] = weighing_move.picking_id.tmp_controller.id
                vals['producer_present'] = weighing_move.picking_id.producer_present.id
                
                #donne acc;es au picking
#                move.picking_id #picking_id fu quant
#                étiquette
#                obj stock picking type créer objet pesée se1 et senb
            
            
            #quant > move > picking          
                    #        if vals.get('project_id'):
            #            project = self.env['project.project'].browse(vals.get('project_id'))
            #            vals['account_id'] = project.analytic_account_id.id
        return super(maple_control, self).write(vals)
#     @api.onchange('acer_seal_no','maple_brix') #barrelCnt, InspectNb
#     def _compute_seal(self):
#         employee_obj = self.env['hr.employee']
#         for r in self:
#             ctrl_code = r.maple_seal_no
#             if not ctrl_code:
#                 if r.acer_seal_no:
#                     r.maple_seal_no = r.acer_seal_no
#                 else:
#                     if r.controler and r.maple_brix != 0:
#                         employee = employee_obj.browse([self.controler.id])
#                         cpt = employee.barrelCnt + 1
#                         employee.write({'barrelCnt':cpt})
#                         ctrl_code = date.today().strftime('%y') + str(int(self.controler.inspectNb)).zfill(2) + "-" + str(cpt).zfill(5)                        
#                         r.maple_seal_no = ctrl_code
#             else:
#                 r.maple_seal_no = ctrl_code           
                

    @api.onchange('container_type') # if these fields are changed, call method
    def check_change_container_type(self):
        self.container_tar_weight = self.container_type.weight

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
    
    maple_product_type = fields.Char(
        string="Maple Syrup one-character Type",
        compute="_maple_type_onechar",
        help="Maple Syrup one-character Type (R:regular, B:biologique.) "
        )
    
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
        related='owner_id.name',
        readonly=False)
    
    producer_code = fields.Char(
        string='producer',
        related='owner_id.parent_id.ref',
        readonly=False)

    tmp_material = fields.Many2one(
        comodel_name='maple.container_material',
        string='Type', 
        readonly=False)
    
    tmp_material_code = fields.Char(
        string='One-char Container Material',
        help="Maple Syrup Container one-character Material",
        related='tmp_material.code'
        )
    
    tmp_owner = fields.Many2one(
        comodel_name='maple.container_owner_type',
        string='Owner', 
        readonly=False)
    
    tmp_tare = fields.Integer(
        string='Tare',
        readonly=False
        )

    buyer = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer', 
        readonly=False)
    
    buyer_code = fields.Char(
        string='Buyer',
        related='buyer.ref',
        readonly=False
        )
    
    class_site  = fields.Char(
        string='Classification Site', 
        compute="_compute_class_site",
        store=True
        )
    
    class_date  = fields.Date(
        string='Classification Date', 
        help=' Imported Classification Date',
        readonly=False
        )
    
    acer_report_no  = fields.Char(
        string='Acer Classification Report No.', 
        help='Imported Acer Classification Report No.',
        readonly=False
        )
    
    weighing_picking = fields.Many2one(
       comodel_name='stock.picking',
       string='Weighing picking', 
       compute="_compute_weighing_picking",
       store=True)
    
    weighing_no = fields.Integer(
       string='Weighing no', 
       compute="_compute_weighing_picking",
       store=True
       )
    
    acer_rule = fields.Boolean(
       string='Acer rule for Quebec', 
       compute="_compute_class_site",
       store=True)  
    
    origin = fields.Char(
       string='Origin of maple syrup', 
       related='producer.state_id.code',
       store=True)
    
    producer_contact = fields.Char(
        compute='_compute_contact',
        string="Contact",
        help="Name of producers's main contact displayed on weighing and classification forms"
        #store=True
        )
    
    @api.depends('product_id') # if these fields are changed, call method
    def _maple_type_onechar(self):
        for r in self:
            r.maple_product_type = r.product_id.default_code[1] #Second character of product_id's default code 
    
    @api.depends('producer') # if these fields are changed, call method
    def _compute_contact(self):
        for r in self:
            if r.producer.parent_id:
                contact = r.producer.parent_id.child_ids.filtered(lambda x: x.type=='contact')
            else:
                contact = r.producer.child_ids.filtered(lambda x: x.type=='contact')
            if contact:
                r.producer_contact = contact[0].name
            else:
                r.producer_contact = 'N/D'
        return

    @api.depends("container_total_weight")
    def _compute_weighing_picking(self): 
       for m in self.history_ids:
           if m.location_dest_id.name == u"Pesée":
               self.weighing_picking = m.picking_id
               self.weighing_no = int(m.picking_id.name[-5:])
    
    @api.depends("container_total_weight")
    def _compute_class_site(self):
        for r in self:
            if r.buyer_code == "SE":
                if r.location_id.location_id.name == "SENB":
                    r.class_site = "SENB"
                elif r.location_id.location_id.name == "SE1":
                    if r.producer.state_id.code == "QC":
                        r.class_site = "370"
                    else:   
                        r.class_site = "SE1"
                else:
                    if r.producer.state_id.code == "QC":
                        r.class_site = "177"
                    else:   
                        r.class_site = "SE3"
            else:
                if r.location_id.location_id.name == "SENB":
                    r.class_site = "LBNB"
                elif r.location_id.location_id.name == "SE1":
                    if r.producer.state_id.code == "QC":
                        r.class_site = "375"
                    else:   
                        r.class_site = "LB1"
                else:
                    if r.producer.state_id.code == "QC":
                        r.class_site = "298"
                    else:   
                        r.class_site = "LB3"
            r.acer_rule = r.owner_id.state_id.code == "QC"

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