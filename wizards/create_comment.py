from odoo import models, fields, api


class Createcomment(models.TransientModel):
    _name = 'create.comment'

    employee_id = fields.Many2one('employee', string="Employee")
    comment = fields.Text(string="Comment", related='employee_id.comment')

    def create_comment(self):
        vals = {
            'employee_id': self.employee_id.id,
            'comment': self.comment,
            'notes': 'Created from Wizard'

        }

        # def create_comment(self):
        #     vals = {
        #         'create_comment': self.create_comment,
        #         'notes': 'Created From The Wizard/Code'
        #     }
        #     self.env['employee'].create(vals)

        # self.employee_id.message_post(body="Comment Created Successfully", subject="Comment Creation")
        # self.env['employee'].create(vals)
