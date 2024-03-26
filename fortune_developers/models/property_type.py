from odoo import models, fields, api


class Property_Type(models.Model):
    _name = 'property.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'New Property Type'

    name = fields.Char(string='Property Name', required=True)
    short_name = fields.Char(string='Property Short Name', required=True)