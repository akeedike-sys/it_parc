from odoo import models, fields, api
from datetime import datetime, timedelta


class ITAlert(models.Model):
    _name = 'it.alert'
    _description = 'Alerte de maintenance'
    _inherit = ['mail.thread']

    name = fields.Char('Titre de l\'alerte', required=True)
    alert_type = fields.Selection([
        ('warranty', 'Fin de garantie'),
        ('contract', 'Expiration de contrat'),
        ('maintenance', 'Maintenance préventive'),
    ], 'Type d\'alerte', required=True)

    equipment_id = fields.Many2one('it.equipment', 'Équipement')
    contract_id = fields.Many2one('it.contract', 'Contrat')

    alert_date = fields.Date('Date de l\'alerte', default=fields.Date.today)
    target_date = fields.Date('Date cible', required=True)
    days_before = fields.Integer('Jours d\'alerte avant date', default=7)

    state = fields.Selection([
        ('pending', 'En attente'),
        ('acknowledged', 'Prise en compte'),
        ('resolved', 'Résolu'),
    ], 'État', default='pending', tracking=True)

    responsible_id = fields.Many2one('hr.employee', 'Responsable')
    description = fields.Text('Description')
    action_taken = fields.Text('Actions effectuées')

    def action_acknowledge(self):
        self.state = 'acknowledged'

    def action_resolve(self):
        self.state = 'resolved'

    @api.model
    def _generate_alerts(self):
        """Cron job pour générer les alertes automatiquement"""
        today = fields.Date.today()
        alert_days = 7  # Paramétrable

        # Alertes de fin de garantie
        equipments = self.env['it.equipment'].search([
            ('warranty_end_date', '!=', False),
            ('warranty_end_date', '>=', today),
            ('warranty_end_date', '<=', today + timedelta(days=alert_days)),
        ])
        for equipment in equipments:
            existing_alert = self.search([
                ('equipment_id', '=', equipment.id),
                ('alert_type', '=', 'warranty'),
                ('state', '!=', 'resolved'),
            ])
            if not existing_alert:
                self.create({
                    'name': f'Garantie expire bientôt : {equipment.name}',
                    'alert_type': 'warranty',
                    'equipment_id': equipment.id,
                    'target_date': equipment.warranty_end_date,
                })

        # Alertes d'expiration de contrats
        contracts = self.env['it.contract'].search([
            ('end_date', '!=', False),
            ('end_date', '>=', today),
            ('end_date', '<=', today + timedelta(days=alert_days)),
        ])
        for contract in contracts:
            existing_alert = self.search([
                ('contract_id', '=', contract.id),
                ('alert_type', '=', 'contract'),
                ('state', '!=', 'resolved'),
            ])
            if not existing_alert:
                self.create({
                    'name': f'Contrat expire bientôt : {contract.name}',
                    'alert_type': 'contract',
                    'contract_id': contract.id,
                    'target_date': contract.end_date,
                })
