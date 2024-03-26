from odoo import models, fields, api


class ReportWizard(models.TransientModel):
    _name = 'installment.report.wizard'
    _description = 'Installment Report Wizard'


    booking_ids = fields.Many2one('new.booking', string='Bookings')
    state = fields.Selection([
        ("booked", "Booking Bliss"),
        ("completed", "Hallelujah!")
    ])

    def action_report(self):
        company_data = self.env['company.profile'].search([])

        comp_name = company_data.name if company_data.name else '<COMPANY_NAME>'
        comp_email = company_data.email if company_data.email else '<EMAIL>'
        comp_contact = company_data.contact if company_data.contact else '<CONTACT>'
        comp_address = company_data.address if company_data.address else '<ADDRESS>'

        comp_data = {}
        if company_data:
            comp_data['name'] = company_data.name if company_data.name else '<COMPANY_NAME>'
            comp_data['email'] = company_data.email if company_data.email else '<EMAIL>'
            comp_data['contact'] = company_data.contact if company_data.contact else '<CONTACT>'
            comp_data['address'] = company_data.address if company_data.address else '<ADDRESS>'
        #     comp_data['logo'] = company_data.company_logo if company_data.company_logo else None
        data={
         'company_data' : comp_data,
        # 'comp_name' : comp_name,
        # 'comp_email' : comp_email,
        # 'comp_contact' : comp_contact,
        # 'comp_address' : comp_address,
        "data" : self.read()[0],
        'name' : 'Tayyab'
       }
        print(data)
        return self.env.ref('fortune_developers.installment_action_report').report_action(self, data=data)

 # print("record", record.booking_ids.cash_price)
            # print("record", record.booking_ids.customer_id.name)
            # print("record", record.booking_ids.customer_id.street)
            # print("record", record.booking_ids.customer_id.street2)
            # print("record", record.booking_ids.customer_id.city)
            # print("record", record.booking_ids.customer_id.country_id.name)
            # print("record", record.booking_ids.book_date)
