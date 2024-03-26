from odoo import models, fields, api

class Company_Profile(models.Model):
    _name = 'company.profile'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Company Profile'

    name = fields.Char(string='Company Name', required=True)
    email = fields.Char(string='Company Email', required=True)
    address = fields.Text(string='Company Address', required=True)
    contact = fields.Char(string='Company Contact', required=True)
    company_logo = fields.Image(string='Company Logo', required=True)




