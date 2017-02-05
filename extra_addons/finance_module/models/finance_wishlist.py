# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceWishlist(models.Model):
    _name = "finance.wishlist"
    _description = "Expenses"

    name = fields.Char('Name of the expense')
    date = fields.Date("Date")
    total_price = fields.Float(compute='_compute_total_price')
    expenseline = fields.One2many('finance.expense.line', 'order_id', "Products", store=True)
    share_with_everyone = fields.Boolean('Share this wishlist')

    @api.one
    @api.depends('expenseline.product_price')
    def _compute_total_price(self):
        self.ensure_one()
        for x in self:
            for line in x.expenseline:
                x.total_price += line.product_price



class FinanceWishListLine(models.Model):
    _name = "finance.wishlist.line"
    _description = "Expenses Line"

    product_id = fields.Many2one('finance.product', store=True)
    order_id = fields.Many2one('finance.expense')
    price_per_product = fields.Float("Price for product", related='product_id.price', readonly=True, store=True)
    product_price = fields.Float(compute='_compute_total_product_price', readonly=True, store=True)
    amount = fields.Integer('Amount', default=1)
    product_is_food = fields.Boolean(related='product_id.is_non_food', store=True)
    product_food_type = fields.Many2one(related='product_id.type_food', store=True)
    product_food_non_food = fields.Many2one(related='product_id.type_non_food', store=True)
    bought = fields.Boolean('Product is bought')



    @api.one
    @api.depends('amount', 'price_per_product')
    def _compute_total_product_price(self):
        self.ensure_one()
        for x in self:
            x.product_price = x.amount * x.price_per_product