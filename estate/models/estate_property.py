from odoo import api, fields, models
from odoo.tools import date_utils, float_utils
from odoo.exceptions import UserError, ValidationError
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Model for estate property"
    _order = "id desc"

    _sql_constraints=[('check_prices','CHECK(expected_price>=0 and selling_price>=0)','Expected and Selling Prices need to be positive')]

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
    garden = fields.Boolean(default=False)
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

    def sold(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'sold'
            else:
                raise UserError("Cancelled properties can't be sold.")
        return True

    def cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancelled'
            else:
                raise UserError("Sold properties can't be cancelled.")

        return True


    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_utils.float_compare(record.selling_price, (record.expected_price * 0.9),precision_digits=3) == -1:
                raise ValidationError('Selling Price must be at least 90% of expected_price')

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"
    _sql_constraints=[('unique_type_name','UNIQUE(name)','Property Types need to have unique names')]

    name = fields.Char(required=True)
    sequence= fields.Integer('Sequence',default=1,help='helps to maintain order.')
    property_ids = fields.One2many("estate.property", "type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer("", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids) or 0
class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order = "name"

    _sql_constraints = [('unique_tag_name', 'UNIQUE(name)', 'Property Tag names need to be unique')]

    name = fields.Char(required=True)
    color = fields.Integer()

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = "price desc"

    _sql_constraints = [('check_price', 'CHECK (price >= 0)','Offers need to have a positive price.')]

    price = fields.Float()
    status = fields.Selection(
        [('accepted', 'Accepted'),
         ('refused', 'Refused'),
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one('estate.property.type',string='Property Type', related='property_id.type_id',store=True)
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


    def action_accept(self):
        for record in self:
            if record.status == 'refused':
                raise UserError('Refused offer')
            else:
                record.status = 'accepted'
                record.property_id.partner_id = record.partner_id
                record.property_id.selling_price = record.price

        return True

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError('Accepted Offer')
            else:
                record.status = 'refused'

        return True

    @api.constrains('date_deadline')
    def _check_date_deadline(self):
        for record in self:
            if record.date_deadline < fields.Date.today():
                raise ValidationError("The deadline cannot be set in the past.")

