from odoo import models, fields, api
from datetime import datetime


class ITIntervention(models.Model):
    _name = 'it.intervention'
    _description = 'Intervention de maintenance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('N° d\'intervention', default='/', copy=False)
    equipment_id = fields.Many2one('it.equipment', 'Équipement', required=True, ondelete='cascade', tracking=True)
    intervention_type = fields.Selection([
        ('corrective', 'Corrective'),
        ('preventive', 'Préventive'),
    ], 'Type d\'intervention', required=True, tracking=True)

    technician_id = fields.Many2one('hr.employee', 'Technicien', required=True, tracking=True)
    start_date = fields.Datetime('Date de début', required=True, tracking=True)
    end_date = fields.Datetime('Date de fin', tracking=True)
    duration_hours = fields.Float('Durée (heures)', compute='_compute_duration', store=True)

    description = fields.Text('Description du problème', required=True)
    intervention_report = fields.Text('Rapport d\'intervention', tracking=True)
    cost = fields.Float('Coût (FCFA)', tracking=True)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
    ], 'État', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('it.intervention') or '/'
        return super().create(vals)

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                record.duration_hours = delta.total_seconds() / 3600
            else:
                record.duration_hours = 0

    def action_start(self):
        self.state = 'in_progress'

    def action_complete(self):
        self.state = 'completed'
        self.end_date = fields.Datetime.now()

    def action_cancel(self):
        self.state = 'cancelled'
