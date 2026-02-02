from odoo import models,fields, api, _

class PropertyType(models.Model):
    _name = "estate.property.type"
    # _inherit = "estate.mixing"
    _description = "Test of Real Estate Model"
    _order = "sequence desc"

    sequence = fields.Integer(default=1)
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    property_count = fields.Integer(compute="_compute_property_count")

    @api.depends("property_ids")
    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)

    def action_open_property_ids(self):
        return {
            "name": _("Related Properties"),
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "estate.property",
            "target": "current",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id},
        }

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for vals in vals_list:
            self.env["estate.property.tags"].create(
                {
                    "name": vals.get("name"),
                }
            )
        return super().create(vals_list)

    def unlink(self):
        self.property_ids.state == "cancelled"
        return super().unlink()

