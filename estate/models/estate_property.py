from odoo import models, fields

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
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
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