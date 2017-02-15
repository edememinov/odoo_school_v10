# -*- coding: utf-8 -*-
from odoo import api, fields, models
import datetime
from dateutil.relativedelta import relativedelta



class FinanceBank(models.Model):
    _name = "finance.bank"
    _description = "Bank"
    _order = 'date'

    name = fields.Char('Name', required=True)
    computed_total_expense = fields.Float(compute='compute_total_expense', store=True, string="Total expense")
    computed_total_income = fields.Float(compute='compute_total_income', store=True, string="Total income")
    computed_total = fields.Float(compute='compute_total', store=True, string="Left over")
    income_id = fields.Many2many('finance.income', compute='compute_income')
    expense_id = fields.Many2many('finance.expense', compute='compute_expenses')
    date = fields.Date('Date', required=True)
    products = fields.Many2many('finance.product', compute='products_in_expense', readonly=True, store=True)

    @api.one
    def compute_expenses(self):
        date = datetime.datetime.strptime(self.date, '%Y-%m-%d')
        date_begin = date - relativedelta(months=1)
        date_end = date + relativedelta(months=1)
        print(date_begin)
        print(date_end)
        self.expense_id = self.env['finance.expense'].search([('date', '>', date_begin), ('date', '<', date_end)])

    @api.one
    def compute_income(self):
        date = datetime.datetime.strptime(self.date, '%Y-%m-%d')
        date_begin = date - relativedelta(months=1)
        date_end = date + relativedelta(months=1)
        print(date)
        self.income_id = self.env['finance.income'].search([('date', '>', date_begin), ('date', '<', date_end)])

    @api.one
    @api.depends('expense_id.expenseline.product_id')
    def products_in_expense(self):
        self.ensure_one()
        for banks in self:
            for expenses in banks.expense_id:
                for expenselines in expenses.expenseline:
                    for products in expenselines.product_id:
                        banks.products += products

    @api.one
    @api.depends('expense_id')
    def compute_total_expense(self):
        self.ensure_one()
        for x in self:
            for expense in x.expense_id:
                x.computed_total_expense += expense.total_price


    @api.one
    @api.depends('income_id')
    def compute_total_income(self):
        self.ensure_one()
        for z in self:
            for income in z.income_id:
                z.computed_total_income += income.amount_received

    @api.one
    @api.depends('computed_total_expense', 'computed_total_income')
    def compute_total(self):
        self.ensure_one()
        for x in self:
           x.computed_total =  x.computed_total_income - x.computed_total_expense



class FinanceBankCal(models.Model):
    _name = "finance.bank.cal"

    name = fields.Char('Name')
    date = fields.Date("Date")
    bank = fields.Many2many('finance.bank', compute='compute_bank')
    amount = fields.Float('Current Amount', compute='compute_bank_amount')

    @api.depends('name','date')
    @api.one
    def compute_bank(self):
        self.bank = self.env['finance.bank'].search([(True,'=',True)])

    @api.one
    def compute_bank_amount(self):
        for bank in self.bank:
            for banks in bank:
                self.amount += banks.computed_total




