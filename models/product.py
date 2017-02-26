# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Product(models.Model):
#	_name = 'maple.product'
	_inherit = 'product.template'
	
	producer = fields.Many2one(
		'res.partner', 
		string="Producer",
		help="The partner producing this product")

	maple_syrup = fields.Boolean(
		string="Is maple syrup",
		help="Check this box if this product is maple syrup. ")
	
	maple_container = fields.Boolean(
		string="Is maple syrup container",
		help="Check this box if this product is maple syrup container. ")
		
	light = fields.Integer(
		string="Light",
		help="% of light transmission, use to define grade")

	brix = fields.Float(
		string="Brix")

	grade = fields.Many2one(
		'maple.grade', 
		string="Grade",
		help="Grade of this maple syrup")

	expected_weight = fields.Float(
		string='Expected weight',
		help='Expected weight of the product. ') 
	
	controled_weight = fields.Float(
		string='Measure weight',
		help='Controled weight of the product. ') 

	adjusted_weight = fields.Float(
		string='Expected weight',
		help='Automated Adjusted weight of the product base on controled weight and brix values. ')
	
	container_type = fields.Selection([
		('S', 'Stainless Steel Container'),
		('A', 'Other'),
		('G', 'Galvanized Steel Container'),
		('P', 'Platic Container'),
		('C', 'CDL Container'),
		('U', 'Unique used Container'),
		('R', 'Re-used unique used Container')],
		'Container Type',
		help="Maple Syrup Container Type")
	
	container_state = fields.Selection([
		('O', 'Good condition'),
		('L', 'Slightly bumped'),
		('B', 'Bumped'),
		('T', 'Very bumped'),
		('R', 'Rusty'),
		('P', 'Punctured'),
		('N', 'Non compliant')],
		'Container Type',
		help="Maple Syrup Container Type")
	
	container_id = fields.Many2one(
		'product.product', 
		string="Container",
		help="Container of maple syrup")

	container_valve = fields.Boolean(
		string="Valve",
		help="Check this box if this container have a valve. ")
	
