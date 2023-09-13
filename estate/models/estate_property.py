from odoo import models,fields

class EstateProperty(models.Model):
    _name = "estate_property"
    _description= "Model for estate property"

    active =fields.Boolean(default=True)

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default = lambda self: fields.Date.today())
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden_area =fields.Integer()
    garden_orientation = fields.Selection(
        [('North','North'),
         ('South','South'),
         ('East','East'),
         ('West','West')]
    )
    state = fields.Selection(
        [
            ('new','New'),
            ('received','Offer Received'),
            ('accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled'),

        ],default='new'
    )