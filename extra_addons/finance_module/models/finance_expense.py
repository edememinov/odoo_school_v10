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

    @api.onchange('user')
    @api.one
    def compute_invisible(self):
        if self.expenseline != False:
            if self.user_id == self.creator_id:
                print(self.user_id == self.creator_id)
                self.inv = False
            else:
                self.inv = True

    @api.one
    def compute_current_user(self):
        self.user = self.env.user
        print(self.user)

    @api.one
    def compute_creator_id(self):
        if self.expenseline != False:
            self.creator_id = self.create_uid
            print(self.creator_id)

    @api.one
    def compute_user_id(self):
        self.user_id = self.user.id
        print(self.user_id)



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
    price_per_product = fields.Float("Price for product", related='product_id.price', readonly=True, store=True)
    product_price = fields.Float(compute='_compute_total_product_price', readonly=True, store=True)
    amount = fields.Integer('Amount', default=1)
    product_is_food = fields.Boolean(related='product_id.is_non_food', store=True)
    product_food_type = fields.Many2one(related='product_id.type_food', store=True)
    product_food_non_food = fields.Many2one(related='product_id.type_non_food', store=True)



    @api.one
    @api.depends('amount', 'price_per_product')
    def _compute_total_product_price(self):
        self.ensure_one()
        for x in self:
            x.product_price = x.amount * x.price_per_product
