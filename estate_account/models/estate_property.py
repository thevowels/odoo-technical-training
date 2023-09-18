from odoo import Command, fields, models

class EstateProperty(models.Model):
    _inherit="estate.property"

    def sold(self):
        for record in self:
            print('inherited_sold method')
            self.env['account.move'].create({'partner_id': record.partner_id.id,
                                             'move_type': 'out_invoice',
                                             'invoice_line_ids':[
                                                 Command.create({
                                                     'name':'Down Payment',
                                                     'quantity':'1',
                                                     'price_unit': 0.06 * record.selling_price,
                                                 }),
                                                 Command.create({
                                                     'name': 'Administrative fees',
                                                     'quantity': '1',
                                                     'price_unit': 100.00,
                                                 }),
                                             ],
                                             })
        return super().sold()
