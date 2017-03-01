# -*- coding: utf-8 -*-

from openerp import models, fields, api
from odoo.tools.yaml_tag import record_constructor
from datetime import date

# modifier le contact (partner) de Odoo pour inclure sa région et son numéro FPAQ
class Contact(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'
	
	fpaqNum = fields.Char(string="FPAQ num")
	siteNum = fields.Char(string="Site num")
	region = fields.Char(string="Region")
		
	maple_producer = fields.Boolean(string='Is a Maple Producer',
		help="Check this box if this contact is a mapple producer. ")
	
	maple_buyer = fields.Boolean(string='Is a Maple Buyer',
		help="Check this box if this contact is a maple buyer. ")
	
	maple_region = fields.Many2one(	'maple.region', 
		string="Region", 
		help="Maple Region")
	
	maple_organic_certification = fields.Boolean(string="Organic certification", 
		help="The maple syrup producer has obtain the Organic certification. ")
		
	default_owner_id = fields.Many2one( 'res.partner', 
		string="Default Buyer", 
		domain=[('maple_buyer', '=', True)],				
		help="Maple syrup buyer for that producer. ")

	maple_purity_certification = fields.Boolean(string="Purity certification", 
		help="The maple syrup producer has obtain the Purity certification. ")
	
	maple_pound_produced = fields.Integer(string='Pound Produced',
		help="Pound produced during current year. ")

	maple_farm = fields.Boolean(string='Is a Maple Farm',
		help="Check this box if this mapple farm address. ",
		compute='_compute_maple_farm',
		store=True)
				
	maple_bio_waiting = fields.Boolean(string='Organic awaiting',
		help="Check this box if this producer is waiting a valid Organic certification. ",
		compute='_compute_maple_id',
		store=True)

	maple_bio = fields.Boolean(string='Organic certified',
		help="Check this box if this producer has a valid Organic certification. ",
		compute='_compute_maple_id',
		store=True)

	maple_pure = fields.Boolean(string='Purity certified',
		help="Check this box if this producer has a valid Putity certification. ",
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
			 	maple_bio_waiting = False
#			 	identifications = self.env['res.partner.id_numbers'].browse(record.id_numbers)			 	
			 	for identification in record.id_numbers:
			 		if identification.category_id.code == "PURE":
			 			record.maple_pure = True
			 		if identification.category_id.code == "BIO":
			 			if identification.valid_until and identification.valid_until >= date.today:
			 				record.maple_bio = True
			 				record.maple_bio_waiting = False
			 			else:
			 				record.maple_bio = False
		 					record.maple_bio_waiting = True
