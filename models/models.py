from datetime import datetime
from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _name = 'employee'
    id_number = fields.Char(required='True')
    name = fields.Char(String='Name', required='True')
    surname = fields.Char(String='Surname', required='True')
    age = fields.Integer(String='Age', compute='compute_person_age', required='True')
    city = fields.Char(String='City', required='True')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True,
                              default='female', required='True')
    birthdate = fields.Date(string="Birthdate", required='True')
    date_of_card_creation = fields.Date(string="Date of card creation", required='True')
    card_validity_period = fields.Date(string='Card validity period', required='True')
    card_number = fields.Char(string="Card number", required='True')
    birth_place = fields.Char(string='Birthplace', required='True')
    card_issuing_organisation = fields.Char(string='Card issuing organization', required='True')
    signature = fields.Binary(string='Signature image')
    fullname = fields.Char(String='Fullname', compute='compute_fullname')
    department = fields.Many2one('department', string='Department')

    _sql_constraints = [
        ('id_unique', 'unique (id_number)', 'id number must be unique'),
        ('card_unique', 'unique (card_number)', 'card number must be unique')
    ]

    @api.constrains('birthdate')
    def check_age(self):
        for rec in self:
            today = date.today()
            birthdate = datetime.strptime(rec.birthdate, '%Y-%m-%d').date()
            if rec.birthdate:
                rec.age = str(int((today - birthdate).days / 365))
            else:
                rec.age = 0

            if rec.age < 18:
                raise ValidationError(('მომხმარებელი არ არის სრულწლოვანი!'))

    @api.constrains('date_of_card_creation', 'card_validity_period')
    def card_creation_restrictions(self):
        for rec in self:
            today = date.today()
            print(rec.date_of_card_creation, rec.card_validity_period)
            date_of_card_creation = datetime.strptime(rec.date_of_card_creation, '%Y-%m-%d').date()
            card_validity_period = datetime.strptime(rec.card_validity_period, '%Y-%m-%d').date()
            if (today - date_of_card_creation).days > 3652.5:
                raise ValidationError(('ბარათის მოქმედების ვადა გაუვიდა!'))
            if (card_validity_period - date_of_card_creation).days < 3652.5:
                raise ValidationError(('ბარათის შექმნის თარიღს  და ბარათის მოქმედების ვადასა შორის არ არის 10 წელი!'))

    @api.multi
    def compute_person_age(self):
        for rec in self:
            today = date.today()
            if rec.birthdate:
                print(rec.birthdate)
                birthdate = datetime.strptime(str(rec.birthdate), '%Y-%m-%d').date()
                rec.age = str(int((today - birthdate).days / 365))
            else:
                age = rec.age

    @api.multi
    def compute_fullname(self):
        for rec in self:
            print(rec.name, rec.surname)
            rec.fullname = rec.name + " " + rec.surname

    @api.constrains
    def check_id(self):
        for rec in self:
            print(rec.id_number)
            if len(rec.id_number) == 11:
                pass
            else:
                raise ValidationError(('ჩანაწერი არ ემთხვევა პირადი ნომრის ფორმატს'))
