# -*- coding: utf-8 -*-

import re
from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import timedelta

class realEstate(models.Model):
    _name = "realestate.properties"
    _description = ""

    name = fields.Char(string="Titre", default="Nouvelle Propriété")
    description = fields.Text(string="Description")
    post_code = fields.Char(string="Code Postal", default="33000")
    photo = fields.Binary(string="Photo", attachment=True)


    active = fields.Boolean(string="Active", default=True)
    status = fields.Selection(
        string="Statut",
        selection=[
            ("new", "Nouveau"),
            ("offer_received", "Offre reçue"),
            ("offer_accepted", "Offre acceptée"),
            ("sold", "Vendu"),
            ("canceled", "Annulée")
        ]
    )

    available_from = fields.Date(string="Disponible à partir de", default=fields.datetime.now())
    deadline = fields.Date(string="Délais (en jour)", inverse="_inverse_total")

    sqm_price = fields.Float(string="Prix du m²", default=4628.00)
    expected_price = fields.Float(string="Prix attendu")
    selling_price = fields.Float(string="Prix estimé", read_only=True, copy=False, compute="_calc_total_area_and_selling_price")

    living_area = fields.Integer(string="Surface habitable (m²)", default=100)
    bedrooms = fields.Integer(string="Nombre de chambre", default=1)

    facades = fields.Integer(string="Nombre de facades", default=4)

    garage = fields.Boolean(string="Garage")

    garden = fields.Boolean(string="Jardin")
    garden_area = fields.Integer(string="Surface du jardin (m²)")
    garden_orientation = fields.Selection(
        string='Orientation du jardin',
        selection=[
            ('north', 'Nord'),
            ('south', 'Sud'),
            ('east', 'Est'),
            ('west', 'Ouest')
        ]
    )

    total_area = fields.Float(string="Surface Totale (m²)", read_only=True, compute="_calc_total_area_and_selling_price")

    _inherits = {'res.users':'owner_id'}
    owner_id = fields.Many2one("res.users", string="Chargée de la vente")

    _sql_constraints = [
        ('expected_price_constraint', 'CHECK(expected_price >= 0)', 'Le prix attendu doit être positif et supérieur à 0.'),
        ('living_area_constraint', 'CHECK(living_area > 0)', 'La surface habitable doit être positive et supérieure à 0.'),
    ]

    @api.constrains('garden', 'garden_area')         
    def _garden_area_constraint(self):
        for record in self:
            if record.garden == True and record.garden_area <= 0:
                raise ValidationError("La surface du jardin doit être supérieure à 0.")

    @api.depends("living_area", "garden", "garden_area", "selling_price", "available_from")
    def _calc_total_area_and_selling_price(self):
        for record in self:
            if record.garden == False:
                record.garden_area = 0
                record.total_area = record.living_area
                record.selling_price = record.total_area * record.sqm_price
            else:
                record.total_area = record.living_area + record.garden_area
                record.selling_price = record.total_area * record.sqm_price

    def _inverse_total(self):
        for record in self:
            record.deadline = record.available_from + timedelta(days=10)

    @api.depends("expected_price")
    def _calc_expected_price(self):
        for record in self:
            if record.expected_price == 0:
                record.expected_price = record.selling_price
