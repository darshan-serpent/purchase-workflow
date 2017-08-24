# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    po_block_id = fields.Many2one(
        comodel_name='purchase.block.reason', track_visibility='always',
        string='Purchase Block Reason',
        default=lambda self: self.env.\
        ref('minimum_purchase_order_value_per_vendor.'
            'purchase_minimum_value_block_reason'))

    minimum_po_amount = fields.Float(related='partner_id.minimum_po_amount',
                                     string="Minimum Purchase Value",
                                     store=False, readonly=True)

    po_amount_check = fields.Boolean(compute='_compute_po_amount_check',
                                     store=True)

    @api.multi
    @api.depends('minimum_po_amount', 'amount_untaxed', 'po_block_id')
    def _compute_po_amount_check(self):
        min_po_amount = self.env.ref('minimum_purchase_order_value_per_vendor.'
                                     'purchase_minimum_value_block_reason')
        for order in self:
            if order.po_block_id == min_po_amount and\
                    order.minimum_po_amount < order.amount_untaxed:
                order.po_amount_check = True
            else:
                order.po_amount_check = False

    @api.multi
    def _check_order_release(self):
        self.ensure_one()
        min_po_amount = self.env.ref('minimum_purchase_order_value_per_vendor.'
                                     'purchase_minimum_value_block_reason')
        if self.po_block_id == min_po_amount and not self.\
                po_amount_check:
            return True
        elif self.po_block_id and self.po_block_id != min_po_amount and not\
                self.released:
            return True
