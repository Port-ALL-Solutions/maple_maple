# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Region(models.Model):
    _name = 'maple.region'
    _description = "Maple Region"
    
    name = fields.Char(
        string = 'Region',
        help = 'Name of the region maple region',
        required=True,
        translate=True)

    code = fields.Char(
        string = 'Code',
        size = 2,
        help = 'Maple Syrup region codes',
        required=True)
    