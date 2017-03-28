# -*- coding: utf-8 -*-
from openerp import models, fields, api

class BarrelType(models.Model):
    _name = 'maple.barrel_type'
    _description = "Maple syrup Barrel Type"
    
    name = fields.Char(
        string = 'Code',
        help = 'Code of maple syrup barrel type',
        required=True)

    description = fields.Char(
        string = 'Barrel type',
        help = 'Type of barrel',
        required=True,
        translate=True)
    
    default_tare = fields.Float(
        string = 'Tare',
        digit = (3,1),
        help = 'Default weight for this barrel type',
        required=True)