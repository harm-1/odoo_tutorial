from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "The offers done on estate properties"

    price = fields.Float(required=True)
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_compute_validity")

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline =  record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline =  fields.Date.today() + relativedelta(days=record.validity)
                
    def _compute_validity(self):
        for record in self:
            delta = record.date_deadline - record.create_date.date()
            record.validity = delta.days
