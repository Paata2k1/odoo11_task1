import smtplib
from datetime import date
from datetime import datetime
from smtplib import SMTP
from docutils.nodes import row

from addons.stock.models.stock_traceability import rec
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import psycopg2
import psycopg2.extras

db_host = "localhost"
db_port = 5432
db_user = "odoo11"
db_password = "admin"
db_name = "Test"


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
    email_id = fields.Char(string='Email')
    comment = fields.Text(string="Comment")

    _sql_constraints = [
        ('id_unique', 'unique (id_number)', 'id number must be unique'),
        ('card_unique', 'unique (card_number)', 'card number must be unique')
    ]

    @api.model
    def test_cron_mail(self):
        print('N')
        today = date.today()
        employees = self.env['employee'].search([])
        # print('employees', self.dbase)
        for rec in employees:
            print(rec.birthdate, rec.email_id)

        today = datetime.today()
        birthdate = datetime.strptime(rec.birthdate, '%Y-%m-%d').date()
        x = birthdate
        print(today.month, today.day)
        if today.month == x.month and today.day == x.day:
            msg = 'happybday'
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login('kharashvili20@gmail.com', 'gmailapp_password')
            s.sendmail('kharashvili20@gmail.com', rec.email_id, msg)

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
                raise ValidationError('მომხმარებელი არ არის სრულწლოვანი!')

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
            # else:
            #     age = rec.age

    @api.multi
    def compute_fullname(self):
        for rec in self:
            print(rec.name, rec.surname)
            rec.fullname = rec.name + " " + rec.surname

    @api.constrains
    def check_id(self):
        for rec in self:
            print(rec.id_number)
            if len(rec.id_number) != 11:
                raise ValidationError('ჩანაწერი არ ემთხვევა პირადი ნომრის ფორმატს')

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('employee') or ('New')
        result = super(Employee, self).create(vals)
        return result

    # @api.model
    # def dbase(self):
    #     # conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password, dbport=db_port)
    #     #
    #     # cur = conn.cursor()
    #     query = "select * from employee"
    #     rows = self.env.cr.execute(query)
    #     print(rows)
    #     # cur.close()

