from odoo import api,fields, models

class EstateType(models.Model):
    _name="estate.property.type"
    _description="Estate Property Type Description"
    _order = "sequence,name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence= fields.Integer(default=1)
    offer_ids = fields.One2many("estate.property.offer","property_type_id")
    offer_count=fields.Integer(compute="_compute_offer_count")


    _sql_constraints = [
        ('type_name_unique','UNIQUE(name)','Property types need to have unique name')
    ]

    api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids) or 0