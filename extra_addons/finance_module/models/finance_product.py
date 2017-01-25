# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceProduct(models.Model):
    _name = "finance.product"
    _description = "Products"

    name = fields.Char("Product name")
    price = fields.Float("Product Price")
    store = fields.Many2one('finance.shop', "Store")
    type = fields.Selection([('vegetables', 'Vegetables'), ('fruits', 'Fruits'), ('drinks','Drinks'), ('snacks','Snacks'), ('meat','Meat'), ('alcohol','Alcohol'), ('candy','Candy')])



