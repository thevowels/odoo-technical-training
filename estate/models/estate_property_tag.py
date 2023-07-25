from odoo import fields, models

class EstateTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Description"
    _order = "sequence,name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    color = fields.Integer()


    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'Property tags must have unique names')
    ]