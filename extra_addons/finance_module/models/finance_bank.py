# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceBank(models.Model):
    _name = "finance.bank"
    _description = "Bank"

    computed_total_expense = fields.Float(compute='compute_total_expense')
    computed_total_income = fields.Float(compute='compute_total_income')
    computed_total = fields.Float(compute='compute_total')
    income_id = fields.Many2many('finance.income', 'bank_id')
    expense_id = fields.Many2many('finance.expense', 'bank_id')
    date = fields.Date('Date')
    by = fields.Many2many('res.partner','Owner', help="Edem or Dominika")



    @api.one
    @api.depends('expense_id.total_price')
    def compute_total_expense(self):
        self.ensure_one()
        for x in self:
            for expense in x.expense_id:
                self.computed_total_expense += expense.total_price


    @api.one
    @api.depends('income_id.amount_received')
    def compute_total_income(self):
        self.ensure_one()
        for z in self:
            for income in z.income_id:
                self.computed_total_income += income.amount_received

    @api.one
    @api.depends('computed_total_expense', 'computed_total_income')
    def compute_total(self):
        self.ensure_one()
        for x in self:
           x.computed_total =  x.computed_total_income - x.computed_total_expense


