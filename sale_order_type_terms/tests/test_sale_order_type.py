# © 2017 Robert J Sullivan
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.tests.common as common


class TestSaleOrderType(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderType, self).setUp()
        self.sale_type_model = self.env['sale.order.type']
        self.sale_order_model = self.env['sale.order']
        self.partner = self.env.ref('base.res_partner_1')
        self.sequence = self.env['ir.sequence'].create({
            'name': 'Test Sales Order',
            'code': 'sale.order',
            'prefix': 'TSO',
            'padding': 3,
        })
        self.product = self.env.ref('product.product_product_4')
        self.sale_type_empty_note = self.sale_type_model.create({
            'name': 'Test Default Sale Order Type'
        })
        self.sale_type_custom_note = self.sale_type_model.create({
            'name': 'Test Custom Sale Order Type',
            'sale_note': 'These are custom terms and conditions.'
        })
        self.partner.sale_type = self.sale_type_empty_note

    def get_sale_order_vals(self):
        sale_line_dict = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 1.0,
            'price_unit': self.product.lst_price,
        }
        return {
            'partner_id': self.partner.id,
            'order_line': [(0, 0, sale_line_dict)]
        }

    def test_sale_order_type_terms(self):
        order_vals = self.get_sale_order_vals()
        order = self.sale_order_model.create(order_vals)

        # check if setting the order.type_id results in the
        # order.note matching the sale_order_type.sale_note
        order.type_id = self.sale_type_empty_note
        order.onchange_type_id()
        self.assertTrue(order.note == '')

        # check to see if after setting the default sale note for
        # the company it matches the order.note
        self.env['ir.config_parameter'].sudo().set_param(
            'sale.use_sale_note', True)
        self.env.user.company_id.sale_note = ('These are default '
                                              'terms and conditions.')
        order.onchange_type_id()
        self.assertTrue(order.note == ('These are default '
                                       'terms and conditions.'))

        # check if the order.note picks up the
        # custom sale_order_type.sale_note
        order.type_id = self.sale_type_custom_note
        order.onchange_type_id()
        self.assertTrue(
            order.note == 'These are custom terms and conditions.')
