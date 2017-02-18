# -*- coding: utf-8 -*-

from openerp import models, fields, api

class mapleGrade(models.Model):
	_name = 'maple.product.grade'
	_description = "Maple Syrup Type"
	
	name = fields.Char(
		string = 'Grade',
		help = 'Grade for maple syrup',
		required=True,
		translate=True)

	code = fields.Char(
		string = 'Grade code',
		size = 2,
		help = 'Grade code for maple syrup',
		required=True,
		translate=True)
	
	minLight = fields.Float(
		string = 'Minimum light',
		digit = (3,1),
		help = 'Minimum light to get the maple grade',
		required=True)

	taste = fields.Char(
		string = 'Taste',
		help = 'Taste of maple syrup',
		required=True,
		translate=True)

class mappleProduct(models.Model):
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
		'maple.product.grade', 
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
