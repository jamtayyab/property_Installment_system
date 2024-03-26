from odoo import models, fields, api
import uuid
import logging
import math
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)

STATES = [
            ("sketchy", "Sketchy Scheme"),
            ("booked", "Booking Bliss"),
            ("completed", "Hallelujah!"),
        ]


class Booking(models.Model):
    _name = 'new.booking'
    _rec_name = 'booking_code'
    _rec_name_search = ['name', "book_date", 'booking_code', "property_file_id", "customer_id", "dealer_id"]
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'New Booking'

    customer_picture = fields.Image(max_width=200, max_height=200, store=True)
    name = fields.Char(string='Booking ID', readonly=True, default='000000', tracking=True)
    booking_code = fields.Char(string='Booking Code', readonly=True, default='NEW', store=True)
    book_date = fields.Date(string='Booking Date', tracking=True, required=True)
    property_file_id = fields.Many2one('property.files', string='Property File', tracking=True, required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', tracking=True, required=True)
    dealer_id = fields.Many2one('res.partner', string='Dealer', tracking=True, required=True)
    commission = fields.Float(string='Commission', default=0.0, required=True)
    dealer_commission = fields.Monetary(string='Dealer Commission', currency_field='currency_id', compute='_compute_dealer_commission', store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, store=True)
    cash_price = fields.Monetary(string='Cash Price', related='property_file_id.cash_price', currency_field='currency_id', store=True, tracking=True)
    file_processing_fee = fields.Monetary(string='Processing Fee', currency_field = 'currency_id', store=True, tracking=True)
    payment_template_id = fields.Many2one('payment.template', string='Payment Template', tracking=True, required=True)
    installment_line_ids = fields.One2many('installment.lines', 'booking_id', string='Installment Lines')
    installment_start_date = fields.Date(string='Installment Starts', tracking=True, required=True)
    due_date = fields.Integer(string='Fix Due Date',  default=10 , tracking=True)
    remaining_amount = fields.Monetary(string='Remaining Amount', currency_field='currency_id', readonly=True)
    paid_amount = fields.Monetary(string='Paid Amount', currency_field='currency_id', readonly=True)
    state = fields.Selection(STATES, string="State", default="sketchy", tracking=True,required=True,
                             group_expand="_expand_states", )

    _sql_constraints = [
        ('booking_unique', 'unique (name)', 'The Booking ID must be unique!')
    ]
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    @api.onchange("installment_line_ids")
    def _onchange_line_ids(self):
        self.onchange_installment_line_ids()
    def onchange_installment_line_ids(self):
        paid_amount = 0
        for data in self.installment_line_ids:
            if data.payment_status == 'paid':
                paid_amount += data.paid_amount

        self.paid_amount = paid_amount
        self.remaining_amount = self.cash_price - paid_amount





    @api.onchange("due_date")
    def _due_date(self):
        if self.due_date > 28:
            self.due_date = False
            raise UserError('Date Should be less than 28')



    @api.depends('commission','cash_price')
    def _compute_dealer_commission(self):
        for record in self:
            record.dealer_commission =  record.cash_price * record.commission

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            while True:
                # will check it later
                booking_id = str(uuid.uuid4())[:6].upper()
                existing_booking = self.env['new.booking'].search([('name', '=', booking_id)])
                if not existing_booking:
                    break
            vals['name'] = booking_id
            vals['booking_code'] = self.env['ir.sequence'].next_by_code('booking.sequence')
        return super().create(vals)

    @api.onchange('due_date')
    def _compute_installment_line_ids(self):
        for record in self:
            if record.payment_template_id:
                counter = 1
                installment_line = []
                bi_increment = record.payment_template_id.months // 6
                record.installment_line_ids = [(5, 0, 0)]

                if record.payment_template_id.down_payment:
                    installment_line.append(
                        (0, 0, {'installment_amount': math.ceil(record.payment_template_id.down_payment * record.cash_price),
                                'payment_status': 'unpaid',
                                'payment_type': 'Down Payment',
                                'installment_date': record.installment_start_date}))

                if record.payment_template_id.digging_payment:
                    installment_line.append(
                        (0, 0, {'installment_amount': math.ceil(record.payment_template_id.digging_payment * record.cash_price),
                                'payment_status': 'unpaid',
                                'payment_type': 'Digging Payment',
                                'installment_date': record.installment_start_date}))

                if record.payment_template_id.monthly_payment:
                    monthly_installment = math.ceil((record.payment_template_id.monthly_payment * record.cash_price) / record.payment_template_id.months)

                    for i in range(record.payment_template_id.months):
                        if counter < 6:
                            installment_line.append((0, 0, {'installment_amount': monthly_installment,
                                                            'payment_status': 'unpaid',
                                                            'payment_type': f'Monthly Payment-{i+1}',
                                                            'installment_date': record.installment_start_date + relativedelta(
                                                                months=i, day=record.due_date)}))
                            counter += 1
                        elif counter == 6:
                            if record.payment_template_id.biannual_payment:
                                installment_line.append((0, 0, {
                                    'installment_amount': math.ceil(((record.payment_template_id.biannual_payment * record.cash_price) / bi_increment) + monthly_installment),
                                    'payment_status': 'unpaid', 'payment_type': f'Bi-Annual Payment-{i+1}',
                                    'installment_date': record.installment_start_date + relativedelta(months=i,
                                                                                                      day=record.due_date)}))
                            else:
                                installment_line.append((0, 0, {
                                    'installment_amount':  monthly_installment,
                                    'payment_status': 'unpaid', 'payment_type':  f'Monthly Payment-{i+1}',
                                    'installment_date': record.installment_start_date + relativedelta(months=i,
                                                                                                      day=record.due_date)}))
                            counter = 1

                if record.payment_template_id.possession_payment:
                    installment_line.append(
                        (0, 0, {'installment_amount': math.ceil(record.payment_template_id.possession_payment * record.cash_price),
                                'payment_status': 'unpaid',
                                'payment_type': 'Possession Payment',
                                'installment_date': record.installment_start_date}))

                record.installment_line_ids = installment_line
                record.remaining_amount = False
                record.paid_amount = False
                record.onchange_installment_line_ids()


    def action_set_stage(self):
        for record in self:
            if record.state == 'sketchy':
                record.state = 'booked'
            elif record.state == 'booked':
                for data  in record.installment_line_ids:
                    if data.payment_status == 'unpaid':
                        raise ValidationError('Please collect all remaining payments before moving to next stage')
                    else:
                        record.state = 'completed'

    def action_reset_stage(self):
        for record in self:
            if record.state == 'booked':
                record.state = 'sketchy'
            elif record.state == 'completed':
                record.state = 'booked'


class InstallmentLines(models.Model):
    _name = 'installment.lines'
    _description = 'Installment Lines'

    booking_id = fields.Many2one('new.booking', string='Booking')
    installment_date = fields.Date(string='Installment Date', required=True)
    paid_date = fields.Date(string='Paid On')
    payment_type = fields.Char(string='Payment Type', default='', required=True)
    payment_status = fields.Selection([('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid', string='Status',
                                      readonly=True, required=True)
    payment_mode = fields.Selection([('cash', 'Cash'), ('cheque', 'Cheque'), ('online', 'Online')], default='cash')
    receiving_note = fields.Text(string='Receiving Note')
    challan_number = fields.Char(string='Challan Number')
    paid_amount = fields.Monetary(string ='Amount Paid', currency_field='currency_id')
    upload_attachment = fields.Binary(string='Uploaded Screenshot', store=True)
    file_name = fields.Char(string='File Name')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, store=True)
    installment_amount = fields.Monetary(string='Installment Amount', currency_field='currency_id', store=True,
                                         required=True)
    indicator = fields.Text(string='Indicator' ,store=True)
    message = fields.Text(string='Message')

    @api.onchange('paid_amount')
    def onchange_paid_amount(self):
        if self.paid_amount > self.installment_amount:
            self.indicator = '▲'
            self.message = 'Paid Amount is greater than Installment Amount! '

        elif self.paid_amount < self.installment_amount:
            self.indicator = '▼'
            self.message = 'Paid Amount is less than Installment Amount!'
        else:
            self.indicator = ''
            self.message = False



    def action_paid(self):
        if not self.challan_number or not self.receiving_note or not self.paid_amount:
            raise UserError('Recheck Challan Number, Receiving Note and Amount Paid. May be some fields are missing. Open the record and fill all the fields')
        elif self.booking_id.state == 'booked':
            self.paid_date = fields.Date.today()
            self.payment_status = 'paid'
            self.booking_id.onchange_installment_line_ids()
        else:
             raise UserError('You can not mark this as paid\n'
                            'Stage of booking is not "Booking Bliss"')

