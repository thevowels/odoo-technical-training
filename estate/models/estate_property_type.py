from odoo import fields, models

class EstateType(models.Model):
    _name="estate.property.type"
    _description="Estate Property Type Description"
    _order = "name"

    name= fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")

    _sql_constraints = [
        ('type_name_unique','UNIQUE(name)','Property types need to have unique name')
    ]