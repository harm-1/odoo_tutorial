from odoo import models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def set_state_sold(self):
        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        self.env["account.move"].create(
            {
                "partner_id":self.buyer_id, 
                "move_type": 'out_invoice', 
                "journal_id": journal.id,
                'invoice_line_ids': [
                    (0, 0, {
                        'name': 'administration_fee',
                        'quantity': 1,
                        'price_unit': 100,
                        }
                    ),
                    (0, 0, {
                        'name': 'percentage_price_6',
                        'quantity': 1,
                        'price_unit': self.selling_price*0.06,
                        }
                    )
                ]
            })
        return super().set_state_sold()