# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Region(models.Model):
    _name = 'maple.region'
    _description = "Maple Region"
    
    description = fields.Char(
        string = 'Region',
        help = 'Name of the region maple region',
        required=True,
        translate=True)

    name = fields.Char(
        string = 'Code',
        size = 2,
        help = 'Maple Syrup region codes',
        required=True)
    