from odoo import models, fields, api
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError



class Payment_Temp(models.Model):
    _name = 'payment.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Payment Template'

    name = fields.Char(string='Template Name', required=True, tracking=True)
    months = fields.Integer(string='Total Months', required=True, tracking=True)
    down_payment = fields.Float(string='Down Payment', default=0.0, required=True)
    digging_payment = fields.Float(string='On Digging', default=0.0, required=True)
    biannual_payment = fields.Float(string='Bi Annual', default=0.0, required=True)
    monthly_payment = fields.Float(string='Monthly', default=0.0, required=True)
    possession_payment = fields.Float(string='On Possession', default=0.0, required=True)
    payment_temple_line_ids = fields.One2many('payment.template.line', 'payment_template_id', readonly=True, string='Payment Template Lines')

    @api.model_create_multi
    def create(self, vals):
        if round(sum([vals[0]['down_payment'], vals[0]['digging_payment'], vals[0]['biannual_payment'], vals[0]['monthly_payment'], vals[0]['possession_payment']]), 2) != 1.0:
            raise UserError('Total percentage should be equal to 100%')
        else:
            print(vals)
            vals[0]['payment_temple_line_ids'] = [(5, 0, 0)]
            vals[0]['payment_temple_line_ids'] = [(0, 0, {'payment_plan': 'Down Payment', 'plan_percentage': vals[0]['down_payment']})]
            vals[0]['payment_temple_line_ids'] += [(0, 0, {'payment_plan': 'On Digging', 'plan_percentage': vals[0]['digging_payment']})]
            vals[0]['payment_temple_line_ids'] += [(0, 0, {'payment_plan': 'Bi Annually', 'plan_percentage': vals[0]['biannual_payment']})]
            vals[0]['payment_temple_line_ids'] += [(0, 0, {'payment_plan': 'Monthly Installments', 'plan_percentage': vals[0]['monthly_payment']})]
            vals[0]['payment_temple_line_ids'] += [(0, 0, {'payment_plan': 'On Possession', 'plan_percentage': vals[0]['possession_payment']})]
            print(vals)
        return super().create(vals)

class Payment_Temp_Line(models.Model):
    _name = 'payment.template.line'
    _description = 'Payment Template Line'


    payment_template_id = fields.Many2one('payment.template', string='Payment Template')
    payment_plan = fields.Char( string='Payment Plans')
    plan_percentage = fields.Float(string='Percentage', required=True)
