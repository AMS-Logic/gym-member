# -*- coding: utf-8 -*-
# Copyright (C) 2026 AMS Logic
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api

class GymClass(models.Model):
    _name = 'gym.class'
    _description = 'Gym Class'
    _rec_name = 'name'

    name = fields.Char(string="Class Name", required=True)
    description = fields.Text(string="Description")
    instructor = fields.Char(string="Instructor", required=True)
    capacity = fields.Integer(string="Maximum Capacity", required=True, default=20)
    enrolled_count = fields.Integer(string="Enrolled", compute="_compute_enrolled_count", store=True)
    available_spots = fields.Integer(string="Available Spots", compute="_compute_enrolled_count", store=True)
    class_type = fields.Selection([
        ('yoga', 'Yoga'),
        ('pilates', 'Pilates'),
        ('spinning', 'Spinning'),
        ('zumba', 'Zumba'),
        ('hiit', 'HIIT'),
        ('boxing', 'Boxing')
    ], string="Class Type", required=True)
    schedule = fields.Selection([
        ('morning', 'Morning (6-9 AM)'),
        ('midday', 'Midday (10 AM-2 PM)'),
        ('evening', 'Evening (4-8 PM)')
    ], string="Schedule", required=True)
    days_of_week = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')
    ], string="Day of Week", required=True)
    start_time = fields.Float(string="Start Time (Hour)", required=True)
    duration = fields.Float(string="Duration (hours)", required=True, default=1.0)
    active = fields.Boolean(string="Active", default=True)
    member_ids = fields.Many2many('gym.membership', string="Enrolled Members")

    @api.depends('member_ids')
    def _compute_enrolled_count(self):
        for record in self:
            record.enrolled_count = len(record.member_ids)
            record.available_spots = record.capacity - record.enrolled_count

    def action_enroll_member(self, member_id):
        if self.enrolled_count < self.capacity and member_id not in self.member_ids.ids:
            self.write({'member_ids': [(4, member_id)]})
            return True
        return False

    def action_cancel_enrollment(self, member_id):
        if member_id in self.member_ids.ids:
            self.write({'member_ids': [(3, member_id)]})
            return True
        return False

    def toggle_active(self):
        """Toggle active state of the class."""
        self.active = not self.active