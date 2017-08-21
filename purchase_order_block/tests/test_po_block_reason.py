# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.purchase_order_block.tests.test_purchase_order_block import TestPurchaseOrderBlock
from odoo.exceptions import ValidationError


class TestPoBlock(TestPurchaseOrderBlock):

    def test_po_block(self):
        "Confirming the Blocked PO"
        with self.assertRaises(ValidationError):
            self.purchase1.sudo(self.user1_id).button_confirm()
        # Released the block PO and then confirming
        self.purchase1.sudo(self.user1_id).button_release_block()
        self.purchase1.sudo(self.user2_id).button_confirm()
