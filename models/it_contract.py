from odoo import models, fields, api
from datetime import datetime, timedelta


class ITContract(models.Model):
    _name = 'it.contract'
    _description = 'Contrat fournisseur'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Référence contrat', required=True, tracking=True)
    vendor_id = fields.Many2one('res.partner', 'Fournisseur', required=True, tracking=True)
    contract_type = fields.Selection([
        ('maintenance', 'Maintenance'),
        ('license', 'Licence'),
        ('support', 'Support'),
    ], 'Type de contrat', required=True, tracking=True)

    start_date = fields.Date('Date de début', required=True, tracking=True)
    end_date = fields.Date('Date de fin', required=True, tracking=True)
    amount = fields.Float('Montant (FCFA)', required=True, tracking=True)

    equipment_ids = fields.Many2many('it.equipment', 'it_equipment_contract_rel', 'contract_id', 'equipment_id', 'Équipements couverts')

    is_active = fields.Boolean('Actif?', compute='_compute_is_active')
    days_until_expiration = fields.Integer('Jours avant expiration', compute='_compute_expiration')
    is_expiring_soon = fields.Boolean('Expire bientôt?', compute='_compute_expiring_soon')

    renewal_date = fields.Date('Date de renouvellement suggérée', compute='_compute_renewal_date')

    notes = fields.Text('Notes')

    @api.depends('end_date')
    def _compute_is_active(self):
        today = fields.Date.today()
        for record in self:
            record.is_active = record.end_date >= today

    @api.depends('end_date')
    def _compute_expiration(self):
        today = fields.Date.today()
        for record in self:
            if record.end_date:
                days_left = (record.end_date - today).days
                record.days_until_expiration = max(0, days_left)
            else:
                record.days_until_expiration = 0

    @api.depends('is_active', 'days_until_expiration')
    def _compute_expiring_soon(self):
        for record in self:
            record.is_expiring_soon = record.is_active and record.days_until_expiration <= 60

    @api.depends('end_date')
    def _compute_renewal_date(self):
        for record in self:
            if record.end_date:
                record.renewal_date = record.end_date - timedelta(days=30)
            else:
                record.renewal_date = False
