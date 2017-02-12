# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceExpense(models.Model):
    _name = "finance.expense"
    _description = "Expenses"

    name = fields.Char('Name of the expense')
    date = fields.Date("Date", required=True)
    food_price = fields.Float(compute='_compute_food_price')
    expenseline = fields.One2many('finance.expense.line', 'order_id', "Specific Products", store=True)
    total_price = fields.Float(string="Total amount paid for products", compute='compute_total_price_product')
    private_list = fields.Boolean('Private')
    user = fields.Many2one('res.users', string='User ID', compute='compute_current_user')
    user_id = fields.Integer(compute='compute_user_id')
    creator_id = fields.Integer(compute='compute_creator_id')
    inv = fields.Boolean('invisible', compute='compute_invisible')
    is_product = fields.Boolean(string="Specific product")
    amout_junkfood = fields.Float(string='Amount spend on specific food', compute="compute_junkfood")
    percentage_junkfood = fields.Float(compute='compute_percentage', string="Percentage spent on specific products")
    calculate_per_product = fields.Boolean('Calculate total amount per product')
    total_price_input = fields.Float("Total amount paid for products")


    @api.one
    @api.depends('expenseline.product_price')
    def compute_junkfood(self):
        self.ensure_one()
        if self.is_product == True:
            for x in self:
                for line in x.expenseline:
                    x.amout_junkfood += line.product_price

    @api.one
    def compute_total_price_product(self):
        if self.is_product == True:
            self.total_price = self.amout_junkfood
        else:
            self.total_price = self.total_price_input



    @api.one
    def compute_percentage(self):
        if self.is_product == True:
            x = self.amout_junkfood / self.total_price
            self.percentage_junkfood = x * 100

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
    def _compute_food_price(self):
        self.ensure_one()
        if self.is_product == True:
            if self.calculate_per_product == False:
                self.food_price = self.total_price_input - self.amout_junkfood
            else:
                self.food_price = self.total_price - self.amout_junkfood




class FinanceExpenseLine(models.Model):
    _name = "finance.expense.line"
    _description = "Expenses Line"

    product_id = fields.Many2one('finance.product', store=True)
    order_id = fields.Many2one('finance.expense')
    price_per_product = fields.Float("Price for product", related='product_id.price', readonly=True, store=True)
    product_price = fields.Float("Total product price", compute='_compute_total_product_price', readonly=True, store=True)
    amount = fields.Integer('Amount', default=1)
    product_is_food = fields.Boolean(related='product_id.is_non_food', store=True)
    product_food_type = fields.Many2one(related='product_id.type_food', store=True)
    product_food_non_food = fields.Many2one(related='product_id.type_non_food', store=True)
    discount = fields.Integer('Discount')
    is_discount = fields.Boolean('Theres a discount for this product')
    discount_total = fields.Float('Total discount', readonly=True)



    @api.one
    @api.depends('amount', 'price_per_product')
    def _compute_total_product_price(self):
        self.ensure_one()
        for x in self:
            x.product_price = x.amount * x.price_per_product

        else:
            discount = 100.0 - self.discount
            print(discount)
            self.discount_total = discount/100.0
            print(self.discount_total)
            for x in self:
                total_discount_price = x.price_per_product * self.discount_total
                x.product_price = x.amount * total_discount_price
                print(total_discount_price)

