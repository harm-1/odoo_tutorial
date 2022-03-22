from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Test Model"

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    seller_id = fields.Many2one('res.users', string='Salerperson', default=lambda self: self.env.user)

    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, 
        default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')]
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold '), ('canceled', 'Canceled')], 
        required=True, 
        copy=False,
        default='new'
    )

    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price may must be positive'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price may must be positive'),
    ]

    def unlink(self):
        if self.state not in ['new', 'canceled']:
            raise UserError('cant delete a record that is sold or canceled')
        for offer in self.offer_ids:
            offer.unlink()
        return super().unlink()

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best(self):
        for record in self:
            all_offers = record.offer_ids.mapped('price')
            record.best_price = 0
            if all_offers:
                record.best_price = max(all_offers)
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None
    
    @api.constrains('selling_price')
    def set_lower_limit(self):
        for record in self:
            if record.state in ['offer_received', 'offer_accepted', 'sold'] and \
                record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("Toooo low")
    
    def set_state_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("can't sell a canceled property")
                return False

            best_offer = record.offer_ids.sorted('price')[-1]
            best_offer.status = 'accepted'
            record.selling_price = best_offer.price
            record.buyer_id = best_offer.partner_id
            record.state = "sold"
        return True

    def set_state_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("can't cancel a sold property")
                return False
            
            record.state = "canceled"
        return True