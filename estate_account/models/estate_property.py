from odoo import fields, models

class EstateProperty(models.Model):
    _inherit="estate.property"

    def sold(self):
        print('inherited_sold method')
        # account_move = self.env['account.move'].create({'partner_id':'',
        #                                                 'move_type':'',
        #                                                 'journal_id':''})
        return super().sold()
