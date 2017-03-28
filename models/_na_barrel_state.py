# -*- coding: utf-8 -*-
from openerp import models, fields, api

class BarrelState(models.Model):
    _name = 'maple.barrel_state'
    _description = "Maple Barrel state"
    
    name = fields.Char(
        string = 'Code',
        help = 'Code of the maple syrup barrel state',
        required=True)

    description = fields.Char(
        string = 'Barrel state',
        help = 'State of barrel of maple syrup',
        required=True,
        translate=True)
    