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
        string='Purchase Block Reason')

    released = fields.Boolean(copy=False, readonly=True)

    @api.model
    def create(self, vals):
        po = super(PurchaseOrder, self).create(vals)
        po.message_post(body=_('Order \"%s\" blocked with'
                               ' \"%s\"') % (po.name,
                                             po.po_block_id.name))
        return po

    @api.multi
    def button_release_block(self):
        for order in self:
            order.\
                message_post(body=_('Order \"%s\" with block \"%s\" has now '
                                    'released') % (order.name,
                                                   order.po_block_id.name))
            order.released = True

    @api.multi
    def _check_order_release(self):
        self.ensure_one()
        if self.po_block_id and not self.released:
            return True

    @api.multi
    def button_confirm(self):
        for order in self:
            if order._check_order_release():
                raise ValidationError(
                    _('The RFQ is blocked, due to \'%s\'. You will need to'
                      ' request it to be released by an authorized user.')
                                      % order.po_block_id.name)
        return super(PurchaseOrder, self).button_confirm()
