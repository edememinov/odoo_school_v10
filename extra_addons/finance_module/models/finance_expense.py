# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceExpense(models.Model):
    _name = "finance.expense"
    _description = "Expenses"

    date = fields.Date("Date")
    total_price = fields.Float(compute='_compute_total_price')
    expenseline = fields.One2many('finance.expense.line', 'order_id', "Products")
    bank_id = fields.Many2one('finance.bank')

    @api.depends('expenseline.product_price')
    def _compute_total_price(self):
        for x in self:
            for line in x.expenseline:
                self.total_price += line.product_price



class FinanceExpenseLine(models.Model):
    _name = "finance.expense.line"
    _description = "Expenses Line"

    name = fields.Char("Name of product", related='product_id.name')
    product_id = fields.Many2one('finance.product')
    order_id = fields.Many2one('finance.expense')
    product_price = fields.Float("Price for product", related='product_id.price')

