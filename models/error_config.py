# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
from datetime import date
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)
from odoo.tools import pycompat
import pytz

_log = logging.getLogger(__name__)
class ErrorTrackerConfig(models.TransientModel):

    _inherit = 'res.config.settings'

    error_field = fields.Boolean(string="Error",  )
    info_field = fields.Boolean(string="Info", )
    warning_field = fields.Boolean(string="Warning", )
    critical_field = fields.Boolean(string="Critical", )
    last_line_field = fields.Integer(string="Last line", required=False,default=0 )
    send_field = fields.Boolean(string="Send mail nofication", required=False, default=False)

    def set_values(self):
        super(ErrorTrackerConfig, self).set_values()
        set_param = self.env['ir.config_parameter'].set_param
        set_param('error_field', (self.error_field or False))
        set_param('info_field', (self.info_field or False))
        set_param('warning_field', (self.warning_field or False))
        set_param('critical_field', (self.critical_field or False))
        set_param('send_field', (self.send_field or False))


    @api.model
    def get_values(self):
        res = super(ErrorTrackerConfig, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            error_field=get_param('error_field', default=False),
            info_field=get_param('info_field', default=False),
            warning_field=get_param('warning_field', default=False),
            critical_field=get_param('critical_field', default=False),
            send_field=get_param('send_field', default=False),
        )
        return res