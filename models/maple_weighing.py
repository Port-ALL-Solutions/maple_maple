# -*- coding: utf-8 -*-
from openerp import models, fields, api
#from datetime import date

class weighing_picking(models.Model):
    _name = 'maple.weighing_picking'
    _description = "Maple Syrup Weighing"

    maple_producer = fields.Many2one(
        comodel_name='res.partner',
        string= 'Producer',
        help="Producer. "
        )

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string= 'Employee',
        help="Employee. "
#ajouter domaine pour limiter aux inspecteurs
        )

    name = fields.Char(
        string='Weighing No.', 
        help='Weighing Number. ')
          
    total_weight = fields.Float(
        string='Total Weight', 
        help='Total Weight. ')      

    date_planned = fields.Date(
        string='Date planned',
        required=True,
        index=True,
        default=fields.Date.today,
        help='Date at which weighing is planned to be done. '
        )

    date_done = fields.Date(
        string='Date Done',
        required=True,
        index=True,
        default=fields.Date.today,
        help='Date at which weighing was done. '
        )        

    date_done = fields.Datetime(
        string='Date done',
        help='Date done. ')
 
    qty_todo = fields.Integer(
        string='Date done',
        help='Date done. ') 
 
    qty_done = fields.Integer(
        string='Date done',
        help='Date done. ') 
 
    weighing_lines = fields.One2many(           
        comodel_name='maple.weighing_picking_line', 
        inverse_name='weighing_picking_id',
        string="Weighing lines",
        help='Weighing lines. ')
    
    acer_lines = fields.One2many(           
        comodel_name='maple.import_acer', 
        inverse_name='weighing_picking_id',
        string="Weighing lines",
        help='Weighing lines. ')



class Import_acer(models.Model):
    _name = 'maple.import_acer'
    _description = "Maple Syrup Classification by ACER"

    maple_producer = fields.Many2one(
        comodel_name='res.partner',
        string= 'Producer',
        help="Producer"
        )

    weighing_picking_id = fields.Many2one(
        comodel_name='maple.weighing_picking',
        string="weighing picking id"
        )

    weighing_no = fields.Char(
        string = 'Imported Weighing No.',
        help = 'Imported Weighing Number from Acer')

    producer_fpaq = fields.Char(
        string = 'FPAQ No.',
        help = 'FPAQ Number of Quebec Producers')

    report_no = fields.Char(
        string = 'Report No.',
        help = 'Classification Report Number')

#Champ date ou char?
    classif_date = fields.Date(
        string = 'Classificiation Date',
        help = 'Classificiation Date')

    producer_name = fields.Char(
        string = 'Name of the Producer',
        help = 'Name of the Producer')

    producer_city = fields.Char(
        string = 'City',
        help = 'city of the Producer')

    producer_zip = fields.Char(
        string = 'Zip Code',
        help = 'Zip Code of the Producer')

    producer_phone = fields.Char(
        string = 'Phone',
        help = 'Phone Number of the Producer')

    container_owner = fields.Char(
        string = 'Container Owner',
        help = 'Owner of the container: Producer (P) ou Buyer (A)')

    site = fields.Many2one(
        comodel_name = 'maple.weighing_classif_site',
        string = 'Classification Site No.',
        help = 'Classification Site Number')

        #Déterminé dès l'achat:
        #(No site: Acheteur, Destination, provenance sirop)
        #298 = LB SE3 QC
        #375 = LB SE1 QC
        #LB1 = LB SE1 Hors QC
        #LB3 = LB SE3 Hors QC
        #LBNB = LB NB Hors QC
        #370 = SE SE1 QC
        #177 = SE SE3 QC
        #SE1 = SE SE1 Hors QC
        #SE3 = SE SE3 Hors QC
        #SENB = SE NB Hors QC

    site_no = fields.Char(
        string = 'Imported Site No.',
        help = 'Classification Site Number imported from Acer. ')

    fpaqContact_name = fields.Char(
        string = 'Name',
        help = 'FPAQ Contact Name')
        #nom (contact FPAQ)

    fpaqContact_address = fields.Char(
        string = 'Address',
        help = 'FPAQ Contact Address')
        #adresse (contact FPAQ)

    fpaqContact_city = fields.Char(
        string = 'City',
        help = 'FPAQ Contact City')
        #ville (contact FPAQ)

    fpaqContact_state = fields.Char(
        string = 'State',
        help = 'FPAQ Contact State')
        #province (contact FPAQ)
        
    fpaqContact_zip = fields.Char(
        string = 'State',
        help = 'FPAQ Contact State')

    fpaqContact_phone = fields.Char(
        string = 'Phone',
        help = 'FPAQ Contact Phone')
        #téléphone

    supervised = fields.Boolean(
        string = 'Supervised',
        help = 'Supervised')
        #supervisé

    inspector = fields.Char(
        string = 'Inspector',
        help = 'Inspector Name')
        #Inspecteur

    seal_no = fields.Char(
        string = 'Seal No.',
        help = 'Seal Number')
        #No de scellé

    container_no = fields.Char(
        string = 'Container No.',
        help = 'Container Number')
        #No de baril

    gross_weight = fields.Integer(
        string = 'Gross Weight',
        help = 'Gross Weight')
        #poids brut

    tare = fields.Integer(
        string = 'Tare',
        help = 'Gross Weight')

    net_weight = fields.Integer(
        string = 'Net Weight',
        help = 'Net Weight')

    container_state = fields.Char(
        string = 'Container State',
        help = 'Container State')
        #état du baril
        
    weight_adjust = fields.Integer(
        string = 'Weight Adjustment',
        help = 'Weight Adjustment')
        #ajustement

    maple_grade = fields.Char(
        string = 'Grade',
        help = 'Maple Syrup Grade')
        #grade
        
    maple_type = fields.Char(
        string = 'Maple Type',
        help = 'Maple Syrup Type')
        #type

    maple_brix = fields.Float(
        string = 'Brix',
        help = 'Maple Syrup Density in Brix degrees')
        #brix

    maple_light = fields.Integer(
        string = 'Light',
        help = 'Maple Syrup Light Transmission Percentage')
        #lumière

    maple_flaw = fields.Char(
        string = 'Flaw',
        help = 'Maple Syrup Flaw')
        #défaut

    maple_flavor = fields.Integer(
        string = 'Flavor',
        help = 'Maple Syrup Type')
        #saveur

    maple_clarity = fields.Char(
        string = 'Type',
        help = 'Maple Syrup Type')
        #limpidité

    maple_si = fields.Float(
        string = 'Si',
        help = 'Silica Content')
        #silice
        
    maple_ph = fields.Float(
        string = 'pH',
        help = 'pH')
        
    maple_iodine = fields.Float(
        string = 'Iodine',
        help = 'Iodine Content')
        #iode
        
    maple_na = fields.Float(
        string = 'Na',
        help = 'Sodium Content')

    maple_pb = fields.Float(
        string = 'Pb',
        help = 'Lead Content')
        
    maple_held = fields.Boolean(
        string = 'Held',
        help = 'Held Container')
        #retenu
        
    maple_specialTest = fields.Float(
        string = 'Special Test',
        help = 'Special Test')
        #test spécial

    classif_revision = fields.Boolean(
        string = 'Revision',
        help = 'Classification Revision Request')
        #révision

    weighing_order = fields.Integer(
        string = 'Order',
        help = 'Weighing Order')
        #Ordre à la pesée
        
    container_type = fields.Char(
        string = 'Container Type',
        help = 'Weighing Order')
        #Genre de contenant

class weighing_classif_site(models.Model):
    _name = 'maple.weighing_classif_site'
    _description = "Maple Syrup Weighing Classification Site"
    
    name = fields.Char(
        string='Site ID', 
        help='Classification Site Identification. ')
    
    description = fields.Char(
        string='Site Description', 
        help='Classification Site Description. ')

   
class weighing_picking_line(models.Model):
    _name = 'maple.weighing_picking_line'
    _description = "Maple Syrup Weighing Line"

    weighing_picking_id = fields.Many2one(
        comodel_name='maple.weighing_picking',
        string="weighing picking id"
        )

    stock_quant_id = fields.Float(
        string='Total Weight', 
        help='Total Weight. ')
    
    classif_site_no = fields.Char(
        string='Classification Site No.', 
        help='Classification Site Number. ')