from odoo import api, fields, models
from datetime import date, timedelta,datetime
from num2words import num2words






class ransientmodel(models.TransientModel):
    _inherit = 'res.config.settings'

    dollar_today = fields.Float(string="Dollar In Bank",config_parameter='lebnon_vat.dollar_today')
    dollar_today_t = fields.Float(string="Dollar Out Bank",config_parameter='lebnon_vat.dollar_today_t')

class lebnonvat(models.Model):
    _inherit = 'purchase.order.line'

    new_sub = fields.Monetary(string=" New Subtotal",  required=False,compute="subtotal_test" )
    new_sub_with_tax = fields.Monetary(string="Subtotal With Tax",  required=False,compute="subtotal_tax" )
    new_field = fields.Float(string="vvjefbvje",  required=False, compute='vjvwewe' )
    new_field2 = fields.Float(string="gggyu",  required=False, compute='vjvwewe2' )

    def vjvwewe2(self):
        for rec in self:
            rec.new_field2 = rec.new_field*rec.dollar_2day

    def vjvwewe(self):
        for rec in self:
            rec.new_field=(rec.price_unit * rec.taxes_id.amount /100) +rec.price_unit


    def subtotal_tax(self):
        for rec in self:
            if rec.price_unit:
                rec.new_sub_with_tax = (rec.price_unit * rec.taxes_id.amount) + rec.price_unit  *(rec.dollar_2day)


    def subtotal_test(self):
        for rec in self:
            if rec.price_unit:
                rec.new_sub= rec.price_unit * rec.dollar_out_bank


    def testIss_fun(self):
        y = self.env['ir.config_parameter'].sudo().get_param('lebnon_vat.dollar_today')
        return y

    dollar_2day = fields.Monetary(string="Dollar Today Bank",default= testIss_fun)


    def doolar_fun(self):
        dollar = self.env['ir.config_parameter'].sudo().get_param('lebnon_vat.dollar_today_t')
        return dollar
    dollar_out_bank = fields.Monetary(string="Dollar Out Bank",default= doolar_fun)



    # def _prepare_account_move_line(self, move=False):
    #     self.ensure_one()
    #     aml_currency = move and move.currency_id or self.currency_id
    #     date = move and move.date or fields.Date.today()
    #     res = {
    #         'display_type': self.display_type,
    #         'sequence': self.sequence,
    #         'name': '%s: %s' % (self.order_id.name, self.name),
    #         'product_id': self.product_id.id,
    #         'product_uom_id': self.product_uom.id,
    #         'quantity': self.qty_to_invoice,
    #         'price_unit': self.currency_id._convert(self.price_unit, aml_currency, self.company_id, date, round=False),
    #         'tax_ids': [(6, 0, self.taxes_id.ids)],
    #         'analytic_account_id': self.account_analytic_id.id,
    #         'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
    #         'purchase_line_id': self.id,
    #         're_new_sub': self.new_sub,
    #         're_new_sub_with_tax': self.new_sub_with_tax,
    #     }
    #     if not move:
    #         return res
    #
    #     if self.currency_id == move.company_id.currency_id:
    #         currency = False
    #     else:
    #         currency = move.currency_id
    #
    #     res.update({
    #         'move_id': move.id,
    #         'currency_id': currency and currency.id or False,
    #         'date_maturity': move.invoice_date_due,
    #         'partner_id': move.partner_id.id,
    #     })
    #     return res




class accmove(models.Model):
    _inherit = 'account.move.line'

    re_new_sub = fields.Monetary(string="New Subtotal",  required=False, )
    re_new_sub_with_tax = fields.Monetary(string="Subtotal With Tax",  required=False, )


class NewModule(models.Model):
    _inherit = 'purchase.order'
    total_vat = fields.Monetary(string="بالليرة",  required=False,compute='shipping_one_r')
    untaxtotal_vat = fields.Monetary(string="باليرة",  required=False,compute='untaxtotal_amount')
    totallebnon_vat = fields.Monetary(string="Total",  required=False,compute='total_lebnon_vat')

    totallebnon_vat_new = fields.Monetary(string="Total",  required=False,compute='total_lebnon_vat_new')
    amount_taxes = fields.Monetary(string=" بالليرة", required=False, compute="usssyy_sjs")


    text_amount = fields.Char(string="المبلغ بالليرة", required=False, compute="amount_to_text")
    text_amount_two = fields.Char(string=" بالليرة", required=False, compute="amount_kwwk")
    text_amount_three = fields.Char(string=" بالليرة", required=False, compute="amount_schjc")
    text_amount_klhoh = fields.Char(string=" بالليرة", required=False, compute="amount_to_text_uuu")

    @api.depends('amount_taxes')
    def amount_to_text_uuu(self):
        for line in self:
            lang = self.env.user.lang
            print(lang)
            line.text_amount_klhoh = num2words(abs(line.amount_taxes), lang='ar_001')+" " +"ليرة"

    @api.depends('totallebnon_vat')
    def amount_to_text(self):
        for line in self:
            lang = self.env.user.lang
            print(lang)
            line.text_amount = num2words(abs(line.totallebnon_vat), lang='ar_001')+ " " +"ليرة"

    @api.depends('total_vat')
    def amount_kwwk(self):
        for line in self:
            lang = self.env.user.lang
            print(lang)
            line.text_amount_two = num2words(abs(line.total_vat), lang='ar_001')+ " " +"ليرة"

    @api.depends('untaxtotal_vat')
    def amount_schjc(self):
        for line in self:
            lang = self.env.user.lang
            print(lang)
            line.text_amount_three = num2words(abs(line.untaxtotal_vat), lang='ar_001') + " " +"ليرة"

    @api.depends('amount_taxes')
    def usssyy_sjs(self):
        for rec in self:
            if rec.order_line:
                for line in rec.order_line:
                       rec.amount_taxes += line.new_field2

            else:
                rec.total_vat = 0


    @api.depends('totallebnon_vat_new')
    def total_lebnon_vat_new(self):
        for rec in self:
            if rec.order_line:
                for line in rec.order_line:
                    rec.totallebnon_vat_new += line.new_sub_with_tax

            else:
                rec.total_vat = 0

    @api.depends('total_vat')
    def shipping_one_r(self):
        for rec in self:
            if rec.order_line:
                for line in rec.order_line:
                    rec.total_vat += line.new_sub_with_tax

            else:rec.total_vat=0

    @api.depends('untaxtotal_vat')
    def untaxtotal_amount(self):
        for rec in self:
            if rec.order_line:
                for line in rec.order_line:
                    rec.untaxtotal_vat += line.new_sub

            else:
                rec.untaxtotal_vat = 0


    def total_lebnon_vat(self):
        for rec in self:
            rec.totallebnon_vat = rec.amount_taxes + rec.untaxtotal_vat
