# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceIncome(models.Model):

    _name = "finance.income"
    _description = "Income"

    date = fields.Date("Date")
    amount_received = fields.Float("Amount received")
    received_from = fields.Char("Received from")


