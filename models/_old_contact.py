# -*- coding: utf-8 -*-

from openerp import models, fields, api

# modifier le contact (partner) de Odoo pour inclure sa région et son numéro FPAQ
class Contact(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'
	region = fields.Char(string="Region")
	fpaqCode = fields.Char(string="FPAQ")
	intCode = fields.Char(string="Internal Code")
