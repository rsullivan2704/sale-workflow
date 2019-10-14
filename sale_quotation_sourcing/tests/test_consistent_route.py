#    Author: Leonardo Pistone
#    Copyright 2014 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from odoo.tests.common import TransactionCase

from datetime import datetime


class TestConsistentRoute(TransactionCase):
    def test_dropshipping_route_purchase_to_customer_passes(self):
        self.dropship_sale_line.route_id = self.dropship
        self.assertIs(True, self.dropship_sale_line.has_consistent_route())

    def test_dropshipping_route_purchase_to_internal_fails(self):
        self.internal_sale_line.route_id = self.dropship
        self.assertIs(False, self.internal_sale_line.has_consistent_route())

    def test_mto_route_purchase_to_customer_fails(self):
        self.dropship_sale_line.route_id = self.mto
        self.assertIs(False, self.dropship_sale_line.has_consistent_route())

    def test_mto_route_purchase_to_internal_passes(self):
        self.internal_sale_line.route_id = self.mto
        self.assertIs(True, self.internal_sale_line.has_consistent_route())

    def test_no_route_passes(self):
        self.assertIs(True, self.sale_line.has_consistent_route())

    def setUp(self):
        super(TestConsistentRoute, self).setUp()
        self.dropship = self.env.ref('stock_dropshipping.route_drop_shipping')
        self.mto = self.env.ref('stock.route_warehouse0_mto')
        internal_location = self.env['stock.location'].create({
            'name': 'interanal location',  # required
            'usage': 'internal',  # required
        })
        dropship_picking_type = self.env['stock.picking.type'].create({
            'name': 'dropship picking',  # required
            'sequence_id': self.env.ref('stock.seq_picking_internal').id,  # required
            'code': 'incoming',  # required
            'default_location_dest_id': self.env.ref('stock.stock_location_8').id,
        })
        internal_picking_type = self.env['stock.picking.type'].create({
            'name': 'internal picking',  # required
            'sequence_id': self.env.ref('stock.seq_picking_internal').id,  # required
            'code': 'internal',  # required
            'default_location_dest_id': internal_location.id,
        })
        dropship_po = self.env['purchase.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,  # required
            'picking_type_id': dropship_picking_type.id,
        })
        internal_po = self.env['purchase.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,  # required
            'picking_type_id': internal_picking_type.id,
        })
        sale_order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_2').id,  # required
        })
        self.dropship_purchase_line = self.env['purchase.order.line'].create({
            'name': 'dropship line',
            'date_planned': datetime.now(),  # required
            'product_uom': self.env.ref('product.product_uom_unit').id,  # required
            'product_id': self.env.ref('product.product_product_4').id,  # required
            'price_unit': 0.00,  # required
            'product_qty': 1.0,  # required
            'order_id': dropship_po.id,  # required
        })
        self.interal_purchase_line = self.env['purchase.order.line'].create({
            'name': 'internal line',  # required
            'date_planned': datetime.now(),  # required
            'product_uom': self.env.ref('product.product_uom_unit').id,  # required
            'product_id': self.env.ref('product.product_product_4').id,  # required
            'price_unit': 0.00,  # required
            'product_qty': 1.0,  # required
            'order_id': internal_po.id,  # required
        })
        self.sale_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'name': 'sale line',  # required
            'product_uom': self.env.ref('product.product_uom_unit').id,  # required
            'product_id': self.env.ref('product.product_product_4').id,  # required
            'price_unit': 0.00,  # required
            'product_uom_qty': 1.0,  # required
            'sourced_by': self.dropship_purchase_line.id,
        })
        self.dropship_sale_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'name': 'dropship sale line',  # required
            'product_uom': self.env.ref('product.product_uom_unit').id,  # required
            'product_id': self.env.ref('product.product_product_4').id,  # required
            'price_unit': 0.00,  # required
            'product_uom_qty': 1.0,  # required
            'sourced_by': self.dropship_purchase_line.id,
        })
        self.internal_sale_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'name': 'internal sale line',  # required
            'product_uom': self.env.ref('product.product_uom_unit').id,  # required
            'product_id': self.env.ref('product.product_product_4').id,  # required
            'price_unit': 0.00,  # required
            'product_uom_qty': 1.0,  # required
            'sourced_by': self.interal_purchase_line.id,
        })
