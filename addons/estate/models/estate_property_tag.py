from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "The tags of estate properties"

    name = fields.Char(string="Type", required=True)

    _sql_constraints = [
                        ('field_unique', 
                        'unique(name)',
                        'Choose another value - it has to be unique!')
    ]
