from odoo import fields, models

class EstateType(models.Model):
    _name="estate.property.type"
    _description="Estate Property Type Description"

    name= fields.Char(required=True)
    