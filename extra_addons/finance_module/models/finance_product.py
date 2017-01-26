# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceProduct(models.Model):
    _name = "finance.product"
    _description = "Products"

    name = fields.Char("Product name")
    price = fields.Float("Product Price")
    store = fields.Many2one('finance.shop', "Store")
    is_non_food = fields.Boolean('Product is non food')
    type_food = fields.Selection([('vegetables', 'Vegetables'), ('fruits', 'Fruits'), ('drinks','Drinks'), ('snacks','Snacks'), ('meat','Meat'), ('alcohol','Alcohol'), ('candy','Candy')])
    type_non_food = fields.Selection([('hygene', 'Hygene'), ('phone', 'Phone Bill'), ('rent','Rent'), ('water','Water Bill'), ('gas','Gas Bill'), ('internet','Internet Bill'), ('electricity','Electricity Bill'), ('househole','Household objects'), ('electronics','Electronics'), ('games','Games')])



