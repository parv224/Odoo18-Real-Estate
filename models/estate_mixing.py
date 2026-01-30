from odoo import fields, models

class EstateMixing(models.Model):
    _name = "estate.mixing"

    name = fields.Char(required=True)