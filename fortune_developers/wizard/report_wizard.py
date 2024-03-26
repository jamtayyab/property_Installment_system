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
        data = {}
        for record in self:
            data["uuid"] = record.booking_ids.name
            data["file"] = record.booking_ids.property_file_id.name
            print("record", record.booking_ids.cash_price)
            print("record", record.booking_ids.customer_id.name)
            print("record", record.booking_ids.customer_id.street)
            print("record", record.booking_ids.customer_id.street2)
            print("record", record.booking_ids.customer_id.city)
            print("record", record.booking_ids.customer_id.country_id.name)
            print("record", record.booking_ids.book_date)
        return self.env.ref('fortune_developers.installment_action_report').report_action(self, data=data)

