# -*- coding: utf-8 -*-
# Copyright (C) 2026 AMS Logic
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api, _

class BulkEmailWizard(models.TransientModel):
    _name = 'bulk.email.wizard'
    _description = 'Bulk Email Wizard'

    subject = fields.Char(string="Subject", required=True)
    body = fields.Html(string="Body", required=True)
    recipient_filter = fields.Selection([
        ('all', 'All Members'),
        ('active', 'Active Members Only'),
        ('inactive', 'Inactive Members Only')
    ], string="Recipients", required=True, default='active')
    membership_type_filter = fields.Selection([
        ('all', 'All Types'),
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ], string="Membership Type", default='all')

    def action_send(self):
        # Build domain
        domain = []

        if self.recipient_filter == 'active':
            domain.append(('is_active', '=', True))
        elif self.recipient_filter == 'inactive':
            domain.append(('is_active', '=', False))

        if self.membership_type_filter != 'all':
            domain.append(('membership_type', '=', self.membership_type_filter))

        members = self.env['gym.membership'].search(domain)
        emails_sent = 0

        for member in members:
            if member.email:
                # Create and send mail
                mail = self.env['mail.mail'].create({
                    'subject': self.subject,
                    'body_html': self.body,
                    'email_to': member.email,
                    'author_id': self.env.user.partner_id.id,
                })
                mail.send()
                emails_sent += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Emails Sent'),
                'message': _(f'Sent {emails_sent} emails successfully!'),
                'type': 'success',
                'sticky': False,
            }
        }