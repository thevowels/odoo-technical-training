from odoo import models, Command
from odoo.tools import float_utils
class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_action(self):
        print("######## Overwrited Sold Action ###############")
        for record in self:
            #print(type(record.buyer_id.id))
            #values['partner_id'] = record.buyer_id.id
            self.env['account.move'].create({
                'move_type':'out_invoice',
                'partner_id': record.buyer_id.id,
                'line_ids':[
                    Command.create({
                        "name":record.name,
                        "quantity":1,
                        "price_unit":float_utils.float_round(record.selling_price * 0.06 ,0)
                    }),
                    Command.create({
                        "name":"Administrative fees",
                        "quantity":1,
                        "price_unit":1000
                    })
                    
                ]
            })
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        return super().sold_action()