# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Grade(models.Model):
    _name = 'maple.grade'
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