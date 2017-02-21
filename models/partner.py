# -*- coding: utf-8 -*-

from openerp import models, fields, api

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
		
	owner_id = fields.Many2one( 'res.partner', 
		string="Buyer", 
		domain=[('maple_buyer', '=', True)],				
		help="Maple syrup buyer for that producer. ")

#	maple_purity_certification = fields.Boolean(string="Purity certification", 
#		help="The maple syrup producer has obtain the Purity certification. ")
	
#	maple_pound_produced = fields.Integer(string='Pound Produced',
#		help="Pound produced during current year. ")
