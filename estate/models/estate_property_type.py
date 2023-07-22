from odoo import fields, models

class EstateType(models.Model):
    _name="estate.property.type"
    _description="Estate Property Type Description"

    name= fields.Char(required=True)

    _sql_constraints = [
        ('type_name_unique','UNIQUE(name)','Property types need to have unique name')
    ]