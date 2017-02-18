# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Product(models.Model):
#	_name = 'maple.product'
	_inherit = 'product.template'
	
	producer = fields.Many2one(
		'res.partner', 
		string="Producer",
		help="The partner producing this product")
	
	light = fields.Integer(
		string="Light",
		help="% of light transmission, use to define grade")

	brix = fields.Float(
		string="Brix")

	grade = fields.Many2one(
		'maple.grade', 
		string="Grade",
		help="Grade of this maple syrup")

	maple_syrup = fields.Boolean(
		string="Is maple syrup",
		help="Check this box if this product is maple syrup. ")
	
	expected_weight = fields.Float(
		string='Expected weight',
		help='Expected weight of the product. ') 
	
	controled_weight = fields.Float(
		string='Measure weight',
		help='Controled weight of the product. ') 

	adjusted_weight = fields.Float(
		string='Expected weight',
		help='Automated Adjusted weight of the product base on controled weight and brix values. ') 
