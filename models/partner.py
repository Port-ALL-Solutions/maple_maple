# -*- coding: utf-8 -*-

from openerp import models, fields, api
from odoo.tools.yaml_tag import record_constructor
from datetime import date

# modifier le contact (partner) de Odoo pour inclure sa région et son numéro FPAQ
class Contact(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'
	
	fpaqCode = fields.Char(string="FPAQ")
	intCode = fields.Char(string="Internal Code")
	region = fields.Char(string="Region")
		
	maple_producer = fields.Boolean(string='Is a maple Producer',
		help="This contact is a maple producer.")
	
	maple_buyer = fields.Boolean(string='Is a maple Buyer',
		help="This contact is a maple buyer.")
	
	maple_region = fields.Many2one(	'maple.region', 
		string="Region", 
		help="Internal code of the region where maple syrup picking and empty barrels delivery are done.")
	
	default_owner_id = fields.Many2one('res.partner', 
		string="Default Buyer", 
		domain=[('maple_buyer', '=', True)],				
		help="Select the default buyer of this maple producer.")
	
	maple_organic_certification = fields.Boolean(string="Organic Cert.", 
		help="The maple syrup producer has obtain the Organic certification. ")
	
	maple_purity_certification = fields.Boolean(string="Purity Cert.", 
		help="The maple syrup producer has obtain the Purity certification. ")

	maple_pound_produced = fields.Integer(string='Pound Produced',
		help="Pounds of maple syrup produced this season.")

	maple_farm = fields.Boolean(string='Is a Maple Farm',
		help="This is the address of a maple farm where picking and delivery are done.",
		compute='_compute_maple_farm',
		store=True)
				
	maple_bio_check_on_order = fields.Boolean(string="Must Confirm", 
		help="The maple syrup producer must specify Organic or Regular Order. ")

	maple_bio = fields.Boolean(string='Certified Organic',
		help="Producer's organic certification or annual renewal is valid. ",
		compute='_compute_maple_id',
		store=True)

	maple_bio_state = fields.Selection([
		('N', 'None'),
		('P', 'Pending'),
		('V', 'Valide')],
		help="Producer's organic certification State. ",
		compute='_compute_maple_id',
		store=True)

	maple_bio_pending = fields.Boolean(string='Pending Cert. Org.',
		help="Producer's organic certification or annual renewal is pending. ",
		compute='_compute_maple_id',
		store=True)

	maple_pure = fields.Boolean(string='Certified Purity',
		help="The producer declared not having used any allergenic products this season. ",
		compute='_compute_maple_id',
		store=True)

	@api.depends('parent_id', 'type')
	def _compute_maple_farm(self):
		for record in self:
			record.maple_farm = record.parent_id.maple_producer and record.type == 'delivery'
		
	@api.depends('id_numbers')
	def _compute_maple_id(self):
		for record in self:
			 if record.id_numbers:
			 	record.maple_pure = False
			 	record.maple_bio = False
			 	record.maple_bio_pending = False
			 	record.maple_bio_state = "N"
#			 	identifications = self.env['res.partner.id_numbers'].browse(record.id_numbers)			 	
			 	for identification in record.id_numbers:
			 		if identification.category_id.code == "PURE":
			 			record.maple_pure = True
			 		if identification.category_id.code == "BIO":
			 			if identification.valid_until and identification.valid_until >= date.today:
						 	record.maple_bio = True
						 	record.maple_bio_pending = False
						 	record.maple_bio_state = "V"
			 			else:
						 	record.maple_bio = False
						 	record.maple_bio_pending = True
						 	record.maple_bio_state = "P"
