# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 vitraining.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    "name": "Human Resources: Leaves summary",
    "version": "1.0",
    "author": "viTraining",
    "category": "Human Resources",
    "website": "www.vitraining.com",
    "description": """
    * summary slip
   
""",
    "depends": ["hr","resource","hr_payroll","hr_holidays",'vit_overtime_hress'],
    "data":[
        "views/slip_summary.xml",
        # "views/payslip.xml",
        # "views/pph21_grossup.xml",
        # "data/data.xml",
        # "security/group.xml",
        "security/ir.model.access.csv",
        ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

