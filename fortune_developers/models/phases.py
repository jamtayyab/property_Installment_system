from odoo import models, fields, api


class Phase(models.Model):
    _name = 'new.phase'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'New Phase'

    name = fields.Char(string='Phase Name', required=True)
    short_name = fields.Char(string='Phase Short Name', required=True)