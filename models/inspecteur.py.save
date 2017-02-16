# -*- coding: utf-8 -*-

from openerp import models, fields, api

# On modifie l'employé, spécifiquement pour l'inspecteur.  Chaque inspecteur a un numéro.  Chaque
# inspecteur doit garder un
# décompte de barils inspectés dans l'année.  Lorsqu'on change d'année, il faudrait remettre
# le décompte à 000...
class Inspecteur(models.Model):
	_name = 'hr.employee'
	_inherit = 'hr.employee'
	barrelCnt = fields.Integer(string="Barrel Count", default=1)
	inspectNb = fields.Integer(string="Inspector No", default=0)
		# Lorsqu'on accède l'Inspecteur, si l'année courante est différente de barrelCntYear
		# on remet le barrelCnt à 1, et on met l'année courante dans barrelCntYear
	barrelCntYear = fields.Integer(string="Barrel Count Year", default=999999
