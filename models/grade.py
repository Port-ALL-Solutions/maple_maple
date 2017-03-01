# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Grade(models.Model):
    _name = 'maple.grade'
    _description = "Maple Syrup Classification"
    
    name = fields.Char(
        string = 'Class',
        help = 'Class of maple syrup',
        required=True,
        translate=True)

    code = fields.Char(
        string = 'Class code',
        size = 2,
        help = 'Class code',
        required=True,
        translate=True)
    
    minLight = fields.Float(
        string = 'Minimum light',
        digit = (3,1),
        help = 'Minimum light required by this class',
        required=True)

    taste = fields.Char(
        string = 'Taste',
        help = 'Maple taste or flavor characterizing this color class',
        required=True,
        translate=True)