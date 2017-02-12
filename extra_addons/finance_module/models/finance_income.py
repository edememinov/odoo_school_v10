# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceIncome(models.Model):

    _name = "finance.income"
    _description = "Income"
    _inherit = 'finance.share'

    date = fields.Date("Date")
    amount_received = fields.Float("Amount received")
    received_from = fields.Char("Received from")


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





