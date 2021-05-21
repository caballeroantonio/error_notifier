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


class ErrorTracker(models.Model):
    _name = "error.tracker"
    _order = 'line_number desc'

    error_date = fields.Datetime(string='Date')
    level = fields.Selection([('INFO', 'Info'), ('WARNING', 'Warning'), ('ERROR', 'Error'), ('CRITICAL', 'Critical')],
                             string="Level")
    database = fields.Char(string="Database")
    error_class = fields.Char(string="Class")
    class_error = fields.Char(string="Class Error")
    error_content = fields.Text(string="Error Content")
    line_number = fields.Integer(string="Line Number")

    @api.model
    def read_local_log(self):
        #_logger.error("Comenzar")
        line_number = 0
        continuar = True
        log_entry = None
        eviar_correo = False
        parametros = self.env['res.config.settings'].sudo().get_values()
        #_logger.error(parametros)
        #_logger.error(parametros['error_field'])
        #log_path = "D:/Odoo/Modulos11/salon_produccion/odoo-server.log"
        log_path = "/var/log/odoo/odoo-server.log"
        last_record = self.env['error.tracker'].search([], limit=1)
        if last_record:
            if last_record.line_number > 0:
                line_number = last_record.line_number
                eviar_correo = True
            else:
                line_number = 0
        with open(log_path, encoding="utf8") as f:
            lines = f.readlines()
        error_content = ""
        for line in lines[line_number:]:
            line_number += 1
            if parametros['error_field'] and " ERROR " in line:
                continuar = False
            if parametros['info_field'] and " INFO " in line:
                continuar = False
            if parametros['warning_field'] and " WARNING " in line:
                continuar = False
            if parametros['critical_field'] and " CRITICAL " in line:
                continuar = False

            if continuar == True:
                error_content += line

                continue
            if " INFO " in line or " WARNING " in line or " ERROR " in line or " CRITICAL " in line:
                if error_content != "" and log_entry:
                    log_entry.error_content = error_content.replace('\x00', '')
                    error_content = ""

                error_date = line.split(' ')[0] + " " + line.split(' ')[1].split(",")[0]
                level = line.split(' ')[3]
                database = line.split(' ')[4]
                error_class = line.split(' ')[5][:-1]
                class_error = line.split(":")[3]
                if eviar_correo and parametros['send_field']:
                    mail_values = {
                        'subject': level,
                        'body_html': "   Line Number :" + str(line_number) + "\n" +
                                     "    Error_date :" + error_date + "\n" +
                                     "    Level :" + level + "\n" +
                                     "    Database :" + database+ "\n" +
                                     "    Error_class :" + error_class + "\n" +
                                     "    Class_error :" + class_error,

                        'email_to': self.env['res.company'].sudo().search([], limit=1).email,
                        'email_from': self.env['res.company'].sudo().search([], limit=1).email,
                    }
                    mail_mail_obj = self.env['mail.mail']
                    msg_id = self.env['mail.mail'].create(mail_values)
                    if msg_id:
                        mail_mail_obj.sudo().send(msg_id)
                        mail_mail_obj.sudo().process_email_queue()
                continuar = True
                log_entry = self.env['error.tracker'].create(
                    {'line_number': line_number, 'error_date': error_date, 'level': level, 'database': database,
                     'error_class': error_class, 'class_error': class_error})

            else:
                error_content += line
