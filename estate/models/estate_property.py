from odoo import api, fields, models
from  odoo.tools import date_utils

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Model for estate property"

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", copy=False, default=lambda self: fields.Date.today())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price= fields.Float("Best Offer", default=0, compute='_compute_best_price')
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area", readonly=True, store=True)
    garden_orientation = fields.Selection(
        [('North', 'North'),
         ('South', 'South'),
         ('East', 'East'),
         ('West', 'West')]
    )
    state = fields.Selection(
        [
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),

        ],
        default='new'
    )
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    user_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user,)
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)

    offer_ids = fields.One2many('estate.property.offer', 'property_id', "Offers")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = None

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"

    name = fields.Char(required=True)

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"

    price = fields.Float()
    status = fields.Selection(
        [('accepted', 'Accepted'),
         ('refused', 'Refused'),
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date( compute="_compute_deadline", inverse="_inverse_deadline", store=True)

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = date_utils.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = date_utils.add(fields.Date.today(), days=record.validity)
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date(record.create_date or fields.Date.today())).days