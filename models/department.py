from odoo import models, fields, api


class Department(models.Model):
    _name = 'department'
    _description = 'swisscap.department'

    name = fields.Char(string='Name')
    description = fields.Char(string="description")
