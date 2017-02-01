# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceProduct(models.Model):
    _name = "finance.product"
    _description = "Products"

    name = fields.Char("Product name")
    price = fields.Float("Product Price")
    store = fields.Many2one('finance.shop', "Store")
    is_non_food = fields.Boolean('Product is non food')
    type_food = fields.Many2one('finanace.type.food')
    type_non_food = fields.Many2one('finanace.type.non.food')

class TypeFoodProduct(models.Model):
    _name = 'finanace.type.food'
    _description = "Food types"

    name = fields.Char('Food type')


class TypeNonFoodProduct(models.Model):
    _name = 'finanace.type.non.food'
    _description = "Non food types"

    name = fields.Char('Non food type')

