# -*- coding: utf-8 -*-
# Copyright (C) 2026 AMS Logic
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api
from datetime import datetime, timedelta

class GymAttendance(models.Model):
    _name = 'gym.attendance'
    _description = 'Gym Attendance'
    _rec_name = 'member_name'
    _order = 'check_in desc'

    member_id = fields.Many2one('gym.membership', string="Member", required=True)
    member_name = fields.Char(string="Member Name", related='member_id.name', store=True)
    check_in = fields.Datetime(string="Check In", required=True, default=fields.Datetime.now)
    check_out = fields.Datetime(string="Check Out")
    duration = fields.Float(string="Duration (hours)", compute="_compute_duration", store=True)
    location = fields.Selection([
        ('main', 'Main Gym'),
        ('studio', 'Studio'),
        ('pool', 'Pool'),
        ('cardio', 'Cardio Area')
    ], string="Location", required=True, default='main')
    notes = fields.Text(string="Notes")

    @api.depends('check_in', 'check_out')
    def _compute_duration(self):
        for record in self:
            if record.check_in and record.check_out:
                delta = record.check_out - record.check_in
                record.duration = delta.total_seconds() / 3600.0
            else:
                record.duration = 0.0

    def action_check_out(self):
        for record in self:
            record.check_out = fields.Datetime.now()

    @api.model
    def get_today_attendance(self):
        today = fields.Date.today()
        return self.search_count([
            ('check_in', '>=', today),
            ('check_in', '<', today + timedelta(days=1))
        ])

    @api.model
    def get_active_checkins(self):
        return self.search_count([('check_out', '=', False)])

    @api.model
    def get_attendance_by_date_range(self, date_from, date_to):
        """Return attendance records within date range for reporting."""
        return self.search([
            ('check_in', '>=', date_from),
            ('check_in', '<=', date_to)
        ])