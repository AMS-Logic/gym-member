# -*- coding: utf-8 -*-
# Copyright (C) 2026 AMS Logic
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api

class GymPayment(models.Model):
    _name = 'gym.payment'
    _description = 'Gym Payment'
    _rec_name = 'payment_reference'
    _order = 'payment_date desc'

    payment_reference = fields.Char(
        string="Reference",
        readonly=True,
        required=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('gym.payment')
    )
    membership_id = fields.Many2one('gym.membership', string="Member", required=True)
    member_name = fields.Char(string="Member Name", related='membership_id.name', store=True)
    amount = fields.Float(string="Amount", required=True)
    payment_date = fields.Date(string="Payment Date", required=True, default=fields.Date.today)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Credit Card'),
        ('bank', 'Bank Transfer')
    ], string="Payment Method", required=True, default='cash')
    notes = fields.Text(string="Notes")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft')

    def action_confirm(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'confirmed'

    def action_cancel(self):
        for record in self:
            if record.state == 'confirmed':
                record.state = 'cancelled'