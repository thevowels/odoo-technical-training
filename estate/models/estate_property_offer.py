from odoo import api,fields, models
from odoo.tools import date_utils
class EstateOffer(models.Model):
    _name="estate.property.offer"
    _description = "Estate Property Offers"
    _order = "price desc"
    price = fields.Float(default=50000)
    status = fields.Selection(
        selection = [ ('accepted','Accepted'), ('refused','Refused')],
        copy = False
    )


    partner_id = fields.Many2one('res.partner',string='Partner', required = True)
    property_id = fields.Many2one('estate.property', string='Property', required = True)

# Computes
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse = "_inverse_deadline")
    # date_deadline = fields.Date()

    # ----------------------------------
    #----------CONSTRAINTS--------------
    #-----------------------------------

    _sql_constraints = [
        ('price_must_positive', 'CHECK(price >= 0)', 'Price must be positive you ***')
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = date_utils.add(fields.Date.to_date(record.create_date or fields.Date.today()), days=record.validity)
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date( record.create_date or fields.Date.today())).days

# Computes

    #----------------------------------------
    # Actions
    #----------------------------------------

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            print(record.property_id)
        return True

    def action_refuse(self):
        for record in self:
            record.status="refused"
        return True