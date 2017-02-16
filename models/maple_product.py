# -*- coding: utf-8 -*-

from openerp import models, fields, api

# modifier le contact (partner) de Odoo pour inclure sa région et son numéro FPAQ
class mappleProduct(models.Model):
	_name = 'maple.product'
	_inherit = 'product.template'
	
	producer = fields.Many2one('res.partner', string="Producer", required=True)
	
	lumiere = fields.Integer(
		string="Lumières")

	brix = fields.Float(
		string="Brix")

	grade = fields.One2many('maple.grades','id')
	