# -*- coding: utf-8 -*-
from openerp import models, fields, api

class BarrelType(models.Model):
    _name = 'maple.barrel_type'
    _description = "Maple Barrel Type"
    
    name = fields.Char(
        string = 'Code',
        help = 'Code of maple syrup barrel type',
        required=True)

    description = fields.Char(
        string = 'Barrel type',
        help = 'Type of barrel of maple syrup',
        required=True,
        translate=True)
    
    default_tar = fields.Float(
        string = 'TAR Weight',
        digit = (3,1),
        help = 'Default Tar weight for maple syrup barrel',
        required=True)