from odoo import models, fields, api

class Payment_Plans(models.Model):
    _name = 'payment.plans'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'New Payment Plans'

    name = fields.Char(string='Plan Name', required=True)
