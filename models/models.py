from odoo import models, fields, api


class Employee(models.Model):
    _name = 'employee'
    id_number = fields.Char()
    name = fields.Char(String='Name')
    surname = fields.Char(String='Surname')
    age = fields.Integer('Age')
    city = fields.Char(String='City')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True,
                              default='female')
    birthdate = fields.Date(string="Birthdate")
    date_of_card_creation = fields.Date(string="Date of card creation")
    card_validity_period = fields.Date(string='Card validity period')
    card_number = fields.Char("Card number")
    birth_place = fields.Char(string='Birthplace')
    card_issuing_organisation = fields.Char(string='Card issuing organization')
    signature = fields.Binary(string='Signature image')

    _sql_constraints = [
        ('id_unique', 'unique (id_number)','5569'),
        ('card_unique', 'unique (card_number)','12354')
    ]
