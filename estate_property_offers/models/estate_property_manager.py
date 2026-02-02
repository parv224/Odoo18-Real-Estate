from odoo import models, fields

class EstatePropertyManager(models.Model):
    _name = "estate.property.manager"
    _description = "Estate Property Manager"

    name = fields.Char(name="Manager Name")