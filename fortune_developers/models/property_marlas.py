from odoo import models, fields, api


class Property_Marlas(models.Model):
    _name = 'property.marlas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'New Property Marla'

    name = fields.Char(string='Marlas', required=True)