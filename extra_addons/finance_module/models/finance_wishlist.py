# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FinanceWishlist(models.Model):
    _name = "finance.wishlist"
    _description = "Wishlist"

    name = fields.Char('Name of the wishlist')
    total_price = fields.Float(compute='_compute_total_price')
    wishlistline = fields.One2many('finance.wishlist.line', 'order_id', "Products", store=True)
    private_list = fields.Boolean('Private')
    user_uid = fields.Integer(compute='user_uid_search')


    @api.one
    @api.depends('wishlistline.product_price')
    def _compute_total_price(self):
        self.ensure_one()
        for x in self:
            for line in x.wishlistline:
                x.total_price += line.product_price

    @api.multi
    def user_uid_search(self, cr, uid, context, ids):
        users = self.pool.get('res.users')
        current_user = users.browse(cr, uid, ids, context=context)
        for uid in current_user:
            for x in self:
                x.user_uid = uid.id


class FinanceWishListLine(models.Model):
    _name = "finance.wishlist.line"
    _description = "Wishlist Line"

    product_id = fields.Many2one('finance.product', store=True)
    order_id = fields.Many2one('finance.wishlist')
    price_per_product = fields.Float("Price for product", related='product_id.price', readonly=True, store=True)
    product_price = fields.Float(compute='_compute_total_product_price', readonly=True, store=True)
    amount = fields.Integer('Amount', default=1)
    product_is_food = fields.Boolean(related='product_id.is_non_food', store=True)
    product_food_type = fields.Many2one(related='product_id.type_food', store=True)
    product_food_non_food = fields.Many2one(related='product_id.type_non_food', store=True)
    bought = fields.Boolean('Product is bought')



    @api.one
    @api.depends('amount', 'price_per_product')
    def _compute_total_product_price(self):
        self.ensure_one()
        for x in self:
            x.product_price = x.amount * x.price_per_product
