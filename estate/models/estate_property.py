from odoo import api, fields, models

class Estate(models.Model):
    _name = "estate.property"
    _description = "Estate property Description"

    name = fields.Char(required=True)
    description = fields.Text()
    # having text field makes the **default UI** Ugly and I don't know how to overcome this yet.
    postcode = fields.Char()
    date_availability = fields.Date("Availability Date",copy=False, default = fields.Date.add(fields.Date.today(),months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [('North','North'), ('South', 'South'), ('East','East'), ('West','West')]
    )
    state = fields.Selection(
        selection = [ ('new','New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold','Sold'),('canceled','Canceled')],
        copy=False,
        default='new'
    )
    active = fields.Boolean(default=True)

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
# Add a state field to the estate.property model. Five values are possible: New, Offer Received, Offer Accepted, Sold and Canceled. It must be required, should not be copied and should have its default value set to ‘New’.
#
# Make sure to use the correct type!

    buyer_id = fields.Many2one("res.partner",string="Buyer",copy=False)
    salesperson_id = fields.Many2one("res.users",string="Salesperson",default = lambda self: self.env.uid)

    tag_ids = fields.Many2many("estate.property.tag",string="Tags")

    offer_ids = fields.One2many("estate.property.offer", 'property_id', string='Offers')

# Compute fields and Onchanges


    # Local dependence
    total_area = fields.Integer(compute="_compute_area")

    @api.depends("living_area","garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # Relational Dependence
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            # if record.offer_ids.mapped('price'):
            record.best_price = max(record.offer_ids.mapped('price') or [0])

# Compute fields and Onchanges

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'North'

                
            else:
                record.garden_area = None
                record.garden_orientation = None
