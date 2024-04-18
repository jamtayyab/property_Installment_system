from datetime import datetime, timedelta

from odoo import models

#Do not change this module it will corrupt your database
class PublisherWarrantyContract(models.AbstractModel):
    _inherit = "publisher_warranty.contract"

    def update_notification(self, cron_mode=True):
        # Update expiration date
        expiration_date = (datetime.now() + timedelta(days=340)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        # print("Update expiration date to %s" % expiration_date)
        set_param = self.env["ir.config_parameter"].sudo().set_param
        set_param("database.expiration_date", expiration_date)
        set_param("database.expiration_reason", "renewal")
        return True
