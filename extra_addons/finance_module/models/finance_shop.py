# -*- coding: utf-8 -*-
from odoo import api, fields, models
class FinanceShop(models.Model):
    _name = "finance.shop"
    _description = "Shops"

    name = fields.Char("Shop name")
    shop_type = fields.Selection([('food', 'Food'), ('clothing', 'Clothing'), ('electronic','Electronic'), ('furniture','Furniture'), ('rest','Rest')])
