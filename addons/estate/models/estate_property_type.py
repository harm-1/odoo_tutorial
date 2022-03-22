from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The types of estate properties"

    name = fields.Char(string="Type", required=True)

    _sql_constraints = [
                        ('field_unique', 
                        'unique(name)',
                        'Choose another value - it has to be unique!')
    ]
