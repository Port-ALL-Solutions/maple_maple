# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Product(models.Model):
#	_name = 'maple.product'
	_inherit = 'product.template'
	
	order_create_serial = fields.Boolean(
		string="Serialize",
		help="Create a serial number for reception."
		)
		
	producer = fields.Many2one(
		'res.partner', 
		string="Producer",
		help="Partner which produced this product."
		)

	maple_syrup = fields.Boolean(
		string="Is maple syrup",
		help="This product is maple syrup."
		)
	
	maple_container = fields.Boolean(
		string="Is a maple syrup container",
		help="This product is a maple syrup container."
		)
		
	light = fields.Integer(
		string="Light",
		help="% of light transmission defining maple syrup color class"
		)

	brix = fields.Float(
		string="Brix",
		help="Sugar concentration of the maple syrup in degrees Brix - °Bx - defining its color class"
		)

	grade = fields.Many2one(
		'maple.grade', 
		string="Class",
		help="Maple syrup class"
		)

	maple_type = fields.Selection(
		[	('Bio', 'Organic Maple Syrup'),
			('Regular', 'Regular Maple Syrup')],
		string='Type',
		help="Maple Syrup Type. "
		)
	
	maple_state = fields.Selection(
		[	('received', 'received'), 
			('weighted', 'weighted'), 
			('rated', 'rated'), 
			('revised', 'revised'), 
			('rejected', 'rejected'), 
			('empty', 'empty'), 
			('transformed', 'transformed'), 
			('produced', 'produced')	], 
		default='received'
		)

	expected_weight = fields.Float(
		string='Expected weight',
		help='Expected weight of the product.'
		) 
	
	controlled_weight = fields.Float(
		string='Measured weight',
		help='Controlled weight of the product.'
		) 

	adjusted_weight = fields.Float(
		string='Adjusted weight',
		help='Computed weight of the product - based on controlled weight and degrees Brix.'
		)
	
	container_type = fields.Selection(
		[	('S', 'Stainless Steel Container'),
			('A', 'Other'),
			('G', 'Galvanized Steel Container'),
			('P', 'Plastic Container'),
			('C', 'CDL Plastic Container'),
			('U', 'Single-Use Container'),
			('R', 'Re-used Signle-use Container')	],
		string='Container Type',
		help="Maple Syrup Container Type. "
		)
	
	container_state = fields.Selection(
		[	('O', 'Good condition'),
			('L', 'Slightly bumped'),
			('B', 'Bumped'),
			('T', 'Very bumped'),
			('R', 'Rusty'),
			('P', 'Punctured'),
			('N', 'Non compliant')	],
		string='Container Type',
		help="Maple Syrup Container state. "
		)
	
	container_id = fields.Many2one(
		comodel_name='product.product', 
		string="Container",
		help="Container of maple syrup. "
		)

	container_valve = fields.Boolean(
		string="Valve",
		help="Check this box if this container have a valve. "
		)
	