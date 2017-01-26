# -*- coding: utf-8 -*-
from odoo import api, fields, models
class FinanceShop(models.Model):
    _name = "finance.shop"
    _description = "Shops"

    name = fields.Char("Shop name")

