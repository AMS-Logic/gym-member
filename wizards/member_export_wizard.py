# -*- coding: utf-8 -*-
# Copyright (C) 2026 AMS Logic
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api
import base64
import csv
import json
from io import StringIO

class MemberExportWizard(models.TransientModel):
    _name = 'member.export.wizard'
    _description = 'Member Export Wizard'

    export_format = fields.Selection([
        ('csv', 'CSV'),
        ('json', 'JSON')
    ], string="Export Format", required=True, default='csv')
    include_inactive = fields.Boolean(string="Include Inactive Members", default=False)
    membership_type_filter = fields.Selection([
        ('all', 'All Types'),
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ], string="Membership Type", default='all')

    def action_export(self):
        # Build domain
        domain = []
        if not self.include_inactive:
            domain.append(('is_active', '=', True))
        if self.membership_type_filter != 'all':
            domain.append(('membership_type', '=', self.membership_type_filter))

        members = self.env['gym.membership'].search(domain)

        if self.export_format == 'csv':
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(['Name', 'Phone', 'Email', 'Membership Type', 'Start Date', 'End Date', 'Active'])
            for member in members:
                writer.writerow([
                    member.name,
                    member.phone or '',
                    member.email or '',
                    member.membership_type,
                    member.start_date,
                    member.end_date or '',
                    'Yes' if member.is_active else 'No'
                ])
            data = output.getvalue().encode('utf-8')
            filename = f'members_export_{fields.Datetime.now()}.csv'
        else:  # json
            data = json.dumps([{
                'name': m.name,
                'phone': m.phone,
                'email': m.email,
                'membership_type': m.membership_type,
                'start_date': str(m.start_date),
                'end_date': str(m.end_date) if m.end_date else None,
                'is_active': m.is_active
            } for m in members], indent=2).encode('utf-8')
            filename = f'members_export_{fields.Datetime.now()}.json'

        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'datas': base64.b64encode(data),
            'type': 'binary'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }