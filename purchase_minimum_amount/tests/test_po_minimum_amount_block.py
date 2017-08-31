# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.purchase_order_block.tests.test_purchase_order_block import TestPurchaseOrderBlock
from odoo.exceptions import ValidationError


class TestPoAmountBlock(TestPurchaseOrderBlock):

    def test_po_amount_block(self):
        "Test PO Block for Minimum Threshold Vendor Amount"
        self.partner1.write({'minimum_po_amount': 1500.00})
        amount_block = self.env.ref('minimum_purchase_order_value_per_vendor.'
                                    'purchase_minimum_value_block_reason')
        self.purchase1.write({'po_block_id': amount_block.id})
        self.assertGreater(self.partner1.minimum_po_amount,
                           self.purchase1.amount_untaxed)
        # Will raise an error as the PO total value does not surpass
        # to that of the minimum amount threshold for the Vendor specified
        with self.assertRaises(ValidationError):
            self.purchase1.sudo(self.user1_id).button_confirm()
        # Surpass the threshold amount to automatically release the block on PO
        self.purchase1.order_line[0].write({'product_qty': 3.0})
        self.assertLess(self.partner1.minimum_po_amount,
                        self.purchase1.amount_untaxed)
        self.purchase1.sudo(self.user2_id).button_confirm()
