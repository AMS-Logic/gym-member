# -*- coding: utf-8 -*-
# Copyright (C) 2026 AMS Logic
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api
from datetime import timedelta

class GymMembership(models.Model):
    _name = 'gym.membership'
    _description = 'Gym Membership'

    name = fields.Char(string="Member Name", required=True)
    phone = fields.Char(string="Phone")
    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    end_date = fields.Date(string="End Date")
    email = fields.Char(string="Email")
    membership_type = fields.Selection([
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ], string="Membership Type", required=True, default='basic')
    active = fields.Boolean(string="Active", default=True, help="Manual override for membership status")
    is_active = fields.Boolean(string="Is Active?", compute="_compute_is_active", store=True)
    notes = fields.Text(string="Notes")
    payment_ids = fields.One2many('gym.payment', 'membership_id', string="Payments")

    @api.depends('active', 'end_date')
    def _compute_is_active(self):
        today = fields.Date.today()
        for record in self:
            record.is_active = record.active and (not record.end_date or record.end_date > today)

    def action_toggle_active(self):
        """Toggle the manual active flag."""
        for record in self:
            record.active = not record.active

    @api.model
    def deactivate_expired_memberships(self):
        """Deactivate memberships whose end_date has passed."""
        today = fields.Date.today()
        expired = self.search([
            ('active', '=', True),
            ('end_date', '!=', False),
            ('end_date', '<', today)
        ])
        expired.write({'active': False})
        # Send notification emails for expired memberships
        for member in expired:
            if member.email:
                template = self.env.ref('gym_member.email_template_expiry', raise_if_not_found=False)
                if template:
                    template.send_mail(member.id, force_send=True)
        return len(expired)