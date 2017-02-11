# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceProduct(models.Model):
    _name = "finance.product"
    _description = "Products"

    name = fields.Char("Product name", compute='compute_product_name', readonly=True)
    product_name = fields.Char('Name of the product')
    price = fields.Float("Product Price")
    store = fields.Many2one('finance.shop', "Store")
    is_non_food = fields.Boolean('Product is non food')
    type_food = fields.Many2one('finanace.type.food')
    type_non_food = fields.Many2one('finanace.type.non.food')
    private_list = fields.Boolean('Private')
    user = fields.Many2one('res.users', string='User ID', compute='compute_current_user')
    user_id = fields.Integer(compute='compute_user_id')
    creator_id = fields.Integer(compute='compute_creator_id',string='TEST')
    inv = fields.Boolean('invisible', compute='compute_invisible')
    barcode = fields.Char('Barcode')


    @api.one
    def compute_product_name(self):
        for products in self:
            products.name = products.product_name + "[" + products.barcode + "]" + "Shop: " + products.store

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


class TypeFoodProduct(models.Model):
    _name = 'finanace.type.food'
    _description = "Food types"

    name = fields.Char('Food type')


class TypeNonFoodProduct(models.Model):
    _name = 'finanace.type.non.food'
    _description = "Non food types"

    name = fields.Char('Non food type')

