from odoo import api, fields, models, _
import time
from datetime import datetime, timedelta
import dateutil.parser
from odoo.exceptions import UserError, ValidationError
import base64
import xlwt
from io import BytesIO
from xlrd import open_workbook
import pdb
import logging
_logger = logging.getLogger(__name__)

SESSION_STATES =[('draft','Draft'),('confirm','Waiting Manager Approval'),('confirm_manager','Waiting HRD Approval'),("refuse","Refused"),("validate", "Approved"),("cancel", "Cancelled")]

class leaves_summary(models.Model):
    _name = "leaves.summary"
    _description = "leaves Summary"



    summary_detail_ids      = fields.One2many("leaves.summary.detail", "leaves_summary_id", "leaves Detail",)
    state                   = fields.Selection(string="State", 
                                        selection=SESSION_STATES,
                                        required=True,
                                        readonly=True,
                                        default=SESSION_STATES[0][0])
    is_compute              = fields.Boolean('is compute',default=False)
    name                    = fields.Char('Name',)
    department_id           = fields.Many2one("hr.department", "Department", readonly=True, states={"draft":[("readonly",False)]})
    holiday_status_id       = fields.Many2one("hr.leave.type", string="Leave Type", required=True, readonly=True, 
                                states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, 
                                domain=[('valid', '=', True)])
    name_txt_file           = fields.Char('File Name', readonly=True)
    export_data             = fields.Binary("Export File")
    export_data_txt         = fields.Binary("Export File")

    @api.multi
    def action_draft(self):
        self.state = SESSION_STATES[0][0]

    @api.multi
    def action_confirm(self):
        self.state = SESSION_STATES[1][0]

    @api.multi
    def action_validate(self):
        self.state = SESSION_STATES[4][0]

    @api.multi
    def action_nominal(self):
        # pdb.set_trace()
        cr=self.env.cr
        sql = "delete from leaves_summary_detail where leaves_summary_id=%s"
        cr.execute(sql, (self.id,) ) 
        aloc = []
        sql = """select em.id, em.name, sum(al.number_of_days) as aloc from hr_employee em
                    left join hr_leave_allocation al on al.employee_id = em.id 
                    where al.holiday_status_id = %s and state = 'validate' and em.department_id = %s
                    group by em.id, em.name"""%(self.holiday_status_id.id, self.department_id.id)
        cr.execute(sql)
        aloc = cr.fetchall()
        
        leave = []
        sql = """select em.id, em.name, sum(le.number_of_days) as leave from hr_employee em
                    left join hr_leave le on le.employee_id = em.id 
                    where le.holiday_status_id = %s and state = 'validate' and em.department_id = %s
                    group by em.id, em.name"""%(self.holiday_status_id.id, self.department_id.id)
        cr.execute(sql)
        leave = cr.fetchall()
        final = dict()
        final1 = dict()
        for z in aloc:
            final.setdefault(z[0], []).append(z)
        for x in leave:
            final1.setdefault(x[0], []).append(x)
        for header, value in final.items():
            for head, val in final1.items():
                if header == head:
                    line_data = [(0,0,{
                            'name'      : value[0][1],
                            'alokasi'   : value[0][2],
                            'sudah_approved' : val[0][2],
                            'sisa'      : value[0][2] - val[0][2],
                            })]

                    self.write({'summary_detail_ids' : line_data})
        self.is_compute = True

    @api.multi
    def export(self):
        # pdb.set_trace()
        obj_emp  = self.env['hr.employee'].search([('active', '=', True)])


        header_name = [
            'No',
            'NAME',
            'ALOKASI',
            'SUDAH APPROVED',
            'SISA',
        ]

        workbook = xlwt.Workbook()
        for record in self:
            final_data = []
            line_data = []
            worksheet = workbook.add_sheet('Report Leaves', cell_overwrite_ok=True)
            final_data.append(header_name)
            sql =   "select name, alokasi, sudah_approved, sisa from leaves_summary_detail "
            cr=self.env.cr
            cr.execute(sql)
            res = cr.fetchall()
            # pdb.set_trace()
            no = 0
            for z in res:
                no += 1
                line_data = [no,
                            z[0],
                            z[1],
                            z[2],
                            z[3],
                            ]
                final_data.append(line_data)

            for row in range(0, len(final_data)):
                for col in range(0, len(final_data[row])):
                    value = final_data[row][col]
                    worksheet.write(row, col, value)

        output = BytesIO()
        workbook.save(output)
        output.seek(0)
        self.export_data = base64.b64encode(output.getvalue())
        self.name_txt_file = "%s%s" % ('Report Leaves', '.xls')

        output.close()


class leaves_summary_detail(models.Model):
    _name = "leaves.summary.detail"
    _description = "leaves Summary Detail"



    leaves_summary_id     = fields.Many2one("leaves.summary", "leaves_summary_id", ondelete="cascade")
    name                  = fields.Char("Name")
    alokasi               = fields.Float("Alokasi")
    sudah_approved        = fields.Float("Sudah Approved")
    sisa                  = fields.Float("Sisa")