# © 2017 Robert J Sullivan
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    @api.onchange('type_id')
    def onchange_type_id(self):
        super(SaleOrder, self).onchange_type_id()
        for order in self:
            if order.type_id.sale_note:
                order.note = order.type_id.sale_note
            else:
                order.note = self.env['sale.order']._default_note()
