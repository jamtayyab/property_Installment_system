from odoo import models, fields, api


class Property_Files(models.Model):
    _name = 'property.files'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Property Files'

    name = fields.Char(string='File Number', required=True, tracking=True)
    property_number = fields.Char(string='Property Number', required=True, tracking=True)
    project = fields.Many2one('new.project', string='Project', required=True, tracking=True)
    phase = fields.Many2one('new.phase', string='Phase', required=True, tracking=True)
    floor = fields.Many2one('new.floor', string='Floor', required=True, tracking=True)
    property_marla = fields.Many2one('property.marlas', string='Property Marla', required=True, tracking=True)
    property_type = fields.Many2one('property.type', string='Property Type', required=True, tracking=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, store=True)
    cash_price = fields.Monetary(string='Cash Price', currency_field='currency_id', tracking=True, required=True)
    status = fields.Selection([('available','Available'),('booked','Booked')], default='available', string='Status',  tracking=True, required=True)
    dealer = fields.Many2one('res.partner', string='Dealer', tracking=True)
    customer = fields.Many2one('res.partner', string='Customer', tracking=True)
