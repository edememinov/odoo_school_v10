# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceExpense(models.Model):
    _name = "finance.expense"
    _description = "Expenses"

    name = fields.Char('Name of the expense')
    date = fields.Date("Date")
    total_price = fields.Float(compute='_compute_total_price')
    expenseline = fields.One2many('finance.expense.line', 'order_id', "Products", store=True)
    private_list = fields.Boolean('Private')
    user = fields.Many2one('res.users', string='User ID', compute='compute_current_user')
    user_id = fields.Integer(compute='compute_user_id')
    creator_id = fields.Integer(compute='compute_creator_id',string='TEST')
    inv = fields.Boolean('invisible', compute='compute_invisible')

    @api.one
    def compute_invisible(self):
        if self.user_id == self.creator_id:
            self.inv = False
        else:
            self.inv = True

    @api.one
    def compute_current_user(self):
        self.user = self.env.user


    @api.one
    def compute_creator_id(self):
        self.creator_id = self.create_uid

    @api.one
    def compute_user_id(self):
        self.user_id = self.user.id




    @api.one
    @api.depends('expenseline.product_price')
    def _compute_total_price(self):
        self.ensure_one()
        for x in self:
            for line in x.expenseline:
                x.total_price += line.product_price



class FinanceExpenseLine(models.Model):
    _name = "finance.expense.line"
    _description = "Expenses Line"

    product_id = fields.Many2one('finance.product', store=True)
    order_id = fields.Many2one('finance.expense')
    price_per_product = fields.Float("Total price for products", related='product_id.price', readonly=True, store=True)
    product_price = fields.Float(compute='_compute_total_product_price', readonly=True, store=True)
    amount = fields.Integer('Amount', default=1)
    product_is_food = fields.Boolean(related='product_id.is_non_food', store=True)
    product_food_type = fields.Many2one(related='product_id.type_food', store=True)
    product_food_non_food = fields.Many2one(related='product_id.type_non_food', store=True)
    discount = fields.Integer('Discount', compute='compute_discount_price')
    is_discount = fields.Boolean('Theres a discount for this product')



    @api.one
    @api.depends('amount', 'price_per_product')
    def _compute_total_product_price(self):
        self.ensure_one()
        if self.is_discount == False:
            for x in self:
                x.product_price = x.amount * x.price_per_product
        else:
            discount = 100 - self.discount
            discount_total = discount/100
            for x in self:
                x.product_price = x.amount * (x.price_per_product * discount_total)

