# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceIncome(models.Model):

    _name = "finance.income"
    _description = "Income"

    date = fields.Date("Date")
    amount_received = fields.Float("Amount received")
    received_from = fields.Char("Received from")
    private_list = fields.Boolean('Private')
    user = fields.Many2one('res.users', string='User ID', compute='compute_current_user')
    user_id = fields.Integer(compute='compute_user_id')
    creator_id = fields.Integer(compute='compute_creator_id',string='TEST')
    inv = fields.Boolean('invisible', compute='compute_invisible')

    @api.onchange('user')
    @api.one
    def compute_invisible(self):
        if self.amount_received != False:
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
        if self.amount_received != False:
            self.creator_id = self.create_uid
            print(self.creator_id)

    @api.one
    def compute_user_id(self):
        self.user_id = self.user.id
        print(self.user_id)





