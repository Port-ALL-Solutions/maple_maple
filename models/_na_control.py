# -*- coding: utf-8 -*-
from openerp import models, fields, api

class maple_control(models.Model):
    _name = 'maple.control'
    
    sequence = fields.Integer(
        string="Sequence",
        help="The successive order of barrels planned"
        )
        #Permettre de glisser les articles pour en changer l'ordre

#Nom du producteur (devrait être considéré propriétaire [champ présent dans stock.quant tant que pas classifié conforme)
#    warehouse = fields.related(
#        string="Warehouse",
#        help="Warehouse where "
#        )

#        Emplacement: inutile considérant la gestion des mouvements d'inventaire
#    warehouse = fields.Char(
#        string="Warehouse",
#        help="Warehouse where the product is stocked"
#        )

#    row = fields.Char(
#        string="Row",
#        help="Row of the warehouse where the product is stocked (if applicable)"
#        )

    sequence = fields.Integer(
        string="Sequence",
        help="The successive order of barrels planned"
        )
        #Permettre de glisser les articles pour en changer l'ordre
        
    light = fields.Integer(
        string="Light",
        help="% of light transmission defining maple syrup color class"
        )
    
    brix = fields.Float(
        string="Brix",
        help="Sugar concentration of the maple syrup in degrees Brix - °Bx - defining its color class"
        )    
    
    controler = fields.Many2one('hr.employee', string="Classified by")
    
    date = fields.Date(
        string="Classified on",
        help="Date of classification"
        )
    
#    sealNum = field.Compute

    flaw = fields.Char(
        string="Flaw",
        help="Flaw: VR, NC, Crochet"
        )
    
    flavor = fields.Integer(
        string="Flavor",
        help="Flavor: 1-2-3-4-5-6"
        )
    
#    Grade = fields.Compute(
#        string="Flavor",
#        help="Color: DO-lignt>=75, 50<=AM<75, 25FO, TF-light<=25"
#        )

# pour la saisie ajouter les champs: Sequence
# pour la saisie cacher les champs: Product, Owner
    