# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceExpense(models.Model):
    _name = "finance.expense"
    _description = "Expenses"

    date = fields.Date("Date")
    total_price = fields.Float(compute='_compute_total_price', readonly=True)
    expenseline = fields.One2many('finance.expense.line', 'order_id', "Products")

    @api.one
    @api.depends('expenseline.product_price')
    def _compute_total_price(self):
        self.ensure_one()
        for x in self:
            for line in x.expenseline:
                self.total_price += line.product_price




class FinanceExpenseLine(models.Model):
    _name = "finance.expense.line"
    _description = "Expenses Line"

    name = fields.Char("Name of product", related='product.product_name', readonly=True)
    product = fields.Many2one('finance.product', 'Product')
    order_id = fields.Many2one('finance.expense', readonly=True)
    price_per_product = fields.Float("Price for product", related='product.price', readonly=True)
    product_price = fields.Float(compute='_compute_total_product_price', readonly=True)
    amount = fields.Int('Amount')

    @api.one
    @api.depends('amount', 'product_price')
    def _compute_total_price(self):
        self.ensure_one()
        for x in self:
            x.product_price = x.amount * x.price_per_product

