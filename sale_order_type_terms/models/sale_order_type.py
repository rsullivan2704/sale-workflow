# © 2017 Robert J Sullivan
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderType(models.Model):
    _inherit = 'sale.order.type'

    sale_note = fields.Text(
        string="Terms and Conditions *", 
        translate=True, 
        help=("If defined this will override the Default Terms and Conditions"
        " set in Sales Settings for Sales Orders of this type."))
