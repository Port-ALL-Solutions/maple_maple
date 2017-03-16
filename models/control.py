# -*- coding: utf-8 -*-
from openerp import models, fields, api

class maple_control(models.Model):
    _name = 'maple.control'
    
    light = fields.Integer(
        string="Light",
        help="% of light transmission defining maple syrup color class"
        )
    
    brix = fields.Float(
        string="Brix",
        help="Sugar concentration of the maple syrup in degrees Brix - °Bx - defining its color class"
        )    
    
    controler = fields.Many2one('hr.employee', string="Controled by")
    