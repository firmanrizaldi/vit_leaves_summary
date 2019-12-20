from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import logging
import pdb
import babel
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from pytz import timezone
_logger = logging.getLogger(__name__)

class purchase(models.Model):
    _name = 'hr.payslip'
    _inherit = 'hr.payslip'


    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=False, related='employee_id.department_id')
