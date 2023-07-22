from odoo import fields, models

class EstateTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Description"
    _order = "name"
    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'Property tags must have unique names')
    ]