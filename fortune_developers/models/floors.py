from odoo import models, fields, api


class Floor(models.Model):
    _name = 'new.floor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'New Floor'

    name = fields.Char(string='Floor Name', required=True)
    short_name = fields.Char(string='Floor Short Name', required=True)