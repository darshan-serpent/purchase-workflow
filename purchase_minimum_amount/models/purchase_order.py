# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    po_block_id = fields.Many2one(
        comodel_name='purchase.block.reason',
        string='Purchase Block Reason',
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.\
        ref('purchase_minimum_amount.'\
            'purchase_minimum_value_block_reason'))

    minimum_po_amount = fields.Float(related='partner_id.minimum_po_amount',
                                     string="Minimum Purchase Value",
                                     store=False, readonly=True)

    po_amount_check = fields.Boolean(compute='_compute_po_amount_check',
                                     store=True)

    flag_check = fields.Boolean()

    @api.multi
    def _track_subtype(self, init_values):
        for rec in self:
            if rec.po_amount_check and not rec.flag_check:
                rec.flag_check = True
                return 'purchase_minimum_amount.'\
                    'mt_request_to_release'
        return super(PurchaseOrder, self)._track_subtype(init_values)

    @api.multi
    @api.depends('minimum_po_amount', 'amount_untaxed', 'po_block_id')
    def _compute_po_amount_check(self):
        po_amt_block = self.env.ref('purchase_minimum_amount.'
                                    'purchase_minimum_value_block_reason',
                                    raise_if_not_found=False)
        for order in self:
            if order.po_block_id == po_amt_block and\
                    order.minimum_po_amount <= order.amount_untaxed:
                order.po_amount_check = True
            else:
                order.po_amount_check = False

    @api.multi
    def _check_order_release(self):
        self.ensure_one()
        po_amt_block = self.env.ref('purchase_minimum_amount.'
                                    'purchase_minimum_value_block_reason')
        if self.po_block_id == po_amt_block and not self.\
                po_amount_check:
            return True
        elif self.po_block_id and self.po_block_id != po_amt_block:
            return True
