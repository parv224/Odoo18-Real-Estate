from dateutil.relativedelta import relativedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _rec_name = "name"
    _order = "name"

    name = fields.Char(required=True, default="House")
    active = fields.Boolean(default=True)

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        required=True,
    )

    price = fields.Float(required=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_offer = fields.Float()
    color = fields.Integer(string="Color")


    postcode = fields.Char(required=True)
    date_availability = fields.Date(default=fields.Date.today,copy=False)

    # DETAILS
    description = fields.Text(required=True)
    bedrooms = fields.Integer(default=2,required=True)
    living_area = fields.Integer(string="Living Area (sqm)",required=True)
    facades = fields.Integer(required=True)

    garage = fields.Boolean(required=True)
    garden = fields.Boolean(required=True)
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )

    property_type_id = fields.Many2one("estate.property.type", required=True)
    buyer_ids = fields.Many2one("res.partner", copy=False)

    partner_id = fields.Many2one('res.partner', ondelete='restrict')
    salesperson_ids = fields.Many2one("res.users",default=lambda self: self.env.user)

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    tags_ids = fields.Many2many("estate.property.tags", string="Tags")
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Integer(compute="_compute_best_offer")

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped('price')) if property.offer_ids else 0

    @api.depends("living_area","garden","garden_area")
    def _compute_total_area(self):
        for property in self:
            if property.garden:
                property.total_area = property.living_area +property.garden_area
            else:
                property.total_area = property.living_area


    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for property in self:
            property.data_deadline = fields.Date.today() + relativedelta(days=property.validity)

    def _inverse_date_deadline(self):
        for property in self:
            property.validity = (property.date_deadline - fields.date.today()).days()

    @api.onchange("garden")
    def _onchange_garden(self):
        for estate in self:
            if not estate.garden:
                estate.garden_area = 0
                estate.garden_orientation = False

    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        for estate in self:
            return {
                Warning: {
                    "title":_("Warning"),
                    "message":_("My Message")
                }
            }

    @api.constrains("selling_price","best_offer")
    def _check_constraints(self):
        for estate in self:
            if estate.selling_price < 0.9*estate.expected_price:
                raise ValidationError(_("Price should not be less than 90% of expected price."))

    @api.onchange("offer_ids")
    def _onchange_offer(self):
        for estate in self:
            if estate.state == "sold":
                raise UserError(_("A property already Sold "))
            if estate.state == "cancelled":
                raise UserError(_("A property already Cancelled"))
            for offer in estate.offer_ids:
                if offer.price < 0.9 * estate.expected_price:
                    raise ValidationError(_("Price must not be less than 90% of the expected price"))
            # if estate.state == "accepted":
            #     raise UserError(_("Offer already accepted"))
            if len(estate.offer_ids) > 0:
                estate.state = "offer_received"

    def action_sold(self):
        for estate in self:
            if estate.state == "cancelled":
                raise UserError(_("A cancelled property cannot be sold"))
            elif estate.state == "sold":
                raise UserError(_("A property already sold "))
            elif estate.state == "offer_received":
                raise UserError(_("No offer accepted yet"))
            elif estate.state == "new":
                raise UserError(_("No offers have been made yet"))
            else:
                estate.state = "sold"

            # estate.selling_price = estate.best_offer

    def action_cancel(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError(_("A cancelled property cannot be cancelled."))
        self.state = "cancelled"










    #python odoo-bin -c custom/estate/odoo.conf -u estate





