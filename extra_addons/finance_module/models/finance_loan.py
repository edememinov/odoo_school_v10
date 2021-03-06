# -*- coding: utf-8 -*-
from odoo import api, fields, models
import datetime
from dateutil.relativedelta import relativedelta



class FinanceLoan(models.Model):
    _name = "finance.loan"
    _description = "Loan"
    _order = 'date'

    name = fields.Char('Name', required=True)
    computed_total_expense = fields.Float(compute='compute_total_expense', store=True, string="Amount paid back")
    computed_total_income = fields.Float(compute='compute_total_income', store=True, string="Amount that has to be paid back")
    computed_total = fields.Float(compute='compute_total', store=True, string="Amount left to pay back")
    income_id = fields.Many2many('finance.income', store=True, string='Debt paid back')
    expense_id = fields.Many2many('finance.expense', store=True, string='Debt')
    date = fields.Date('Date', required=True)
    products = fields.Many2many('finance.product', compute='products_in_expense', readonly=True, store=True)

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


