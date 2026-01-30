from dateutil.relativedelta import relativedelta

from odoo import models,fields, api, _
from odoo.exceptions import UserError


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer made for real estates"

    price = fields.Float()

    state = fields.Selection(
        [
            ("new", "New"),
            ("sold", "Sold"),
            ("cancel", "Cancelled"),
        ]
    )

    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", ondelete="cascade", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # @api.depends("price")
    # def _onchange_price(self):
    #     for state in self:
    #

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept(self):
        self.ensure_one()
        for offer in self:
            # if offer.status == "accepted":
            #     raise UserError(_("Offer is accepted"))
            if offer.state == "refused":
                raise UserError(_("Offer is already accepted"))

        accepted_offer = self.property_id.offer_ids.filtered(
            lambda o: o.status == 'accepted' and o.id != self.id
        )
        if accepted_offer:
            raise UserError(_("Only one offer can be accepted for a property"))

        other_offers = self.property_id.offer_ids.filtered(
            lambda o: o.id != self.id
        )

        other_offers.write({'status': 'refused'})

        self.status = "accepted"
        self.property_id.state = "offer_accepted"
        self.property_id.buyer_ids = self.partner_id
        self.property_id.selling_price = self.price

    def action_refuse(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError(_("Offer is accepted"))
            if offer.state == 'sold':
                raise UserError(_("Property is already sold."))
            if offer.state == "cancelled":
                raise UserError(_("Property Cancelled"))
            offer.status = "refused"

    @api.model
    def create(self, vals):
        # Prevent creating new offers
        property_id = vals.get('property_id')

        if property_id:
            property_rec = self.env['estate.property'].browse(property_id)
            if property_rec.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError(
                    _("You cannot create new offers once an offer has been accepted.")
                )

        return super().create(vals)

    def write(self, vals):
        # Prevent modifying offers
        for offer in self:
            accepted_offer = offer.property_id.offer_ids.filtered(
                lambda o: o.status == 'accepted'
            )

            if accepted_offer and not (
                    offer.status == 'accepted' and set(vals.keys()) <= {'status'}
            ):
                raise UserError(
                    _("You cannot modify offers once an offer has been accepted.")
                )

        return super().write(vals)