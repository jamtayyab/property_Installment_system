from odoo import models, fields, api


class Project(models.Model):
    _name = 'new.project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'New Project'

    name = fields.Char(string='Project Name', required=True)
    short_name = fields.Char(string='Project Short Name', required=True)