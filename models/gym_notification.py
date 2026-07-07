# -*- coding: utf-8 -*-
# Copyright (C) 2026 AMS Logic
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class GymNotification(models.Model):
    _name = 'gym.notification'
    _description = 'Gym Notification'
    _rec_name = 'subject'
    _order = 'create_date desc'

    subject = fields.Char(string="Subject", required=True)
    body = fields.Html(string="Body", required=True)
    notification_type = fields.Selection([
        ('expiring', 'Membership Expiring'),
        ('expired', 'Membership Expired'),
        ('payment_due', 'Payment Due'),
        ('promotion', 'Promotion'),
        ('announcement', 'Announcement'),
        ('class_reminder', 'Class Reminder')
    ], string="Type", required=True)
    recipient_ids = fields.Many2many('gym.membership', string="Recipients")
    send_date = fields.Datetime(string="Send Date", required=True, default=fields.Datetime.now)
    sent = fields.Boolean(string="Sent", default=False)

    def action_send_now(self):
        """Send email to all recipients immediately."""
        for notification in self:
            for member in notification.recipient_ids:
                if member.email:
                    template = self.env.ref('gym_member.email_template_notification')
                    if template:
                        template.send_mail(notification.id, force_send=True)
            notification.sent = True

    @api.model
    def send_expiry_notifications(self):
        """Cron job: send expiry notifications to members whose membership expires in 7 days."""
        today = fields.Date.today()
        expiring_date = today + timedelta(days=7)

        expiring_members = self.env['gym.membership'].search([
            ('end_date', '=', expiring_date),
            ('active', '=', True)  # using active flag
        ])

        for member in expiring_members:
            # Avoid duplicate notifications for same member and type within a short period
            existing = self.search([
                ('notification_type', '=', 'expiring'),
                ('recipient_ids', 'in', member.id),
                ('create_date', '>=', fields.Datetime.now() - timedelta(hours=24))
            ], limit=1)
            if existing:
                continue

            # Create notification record
            notification = self.create({
                'subject': _('Membership Expiring Soon'),
                'body': _(f'Dear {member.name},<br/>Your membership will expire on {member.end_date}. Please renew to continue enjoying our services.'),
                'notification_type': 'expiring',
                'recipient_ids': [(4, member.id)],
                'send_date': fields.Datetime.now()
            })
            # Send immediately
            if member.email:
                template = self.env.ref('gym_member.email_template_expiry', raise_if_not_found=False)
                if template:
                    template.send_mail(member.id, force_send=True)
            notification.sent = True

        return len(expiring_members)