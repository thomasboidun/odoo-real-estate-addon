from odoo import models, fields

class RealEstateOwner(models.Model):
    _inherit = "res.users"
    property_ids = fields.One2many("realestate.properties", "owner_id", string = "Property name", readonly=True)