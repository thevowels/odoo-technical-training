from odoo import api,fields, models
from odoo.tools import date_utils
class EstateOffer(models.Model):
    _name="estate.property.offer"
    _description = "Estate Property Offers"

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

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = date_utils.add(fields.Date.to_date(record.create_date or fields.Date.today()), days=record.validity)
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date( record.create_date or fields.Date.today())).days

# Computes