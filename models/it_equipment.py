from odoo import models, fields, api
from datetime import datetime, timedelta


class ITEquipment(models.Model):
    _name = 'it.equipment'
    _description = 'Équipement Informatique'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Nom de l\'équipement', required=True, tracking=True)
    category_id = fields.Many2one('it.equipment.category', 'Catégorie', required=True, tracking=True)
    serial_number = fields.Char('Numéro de série', unique=True, required=True, tracking=True)
    model = fields.Char('Modèle')
    manufacturer = fields.Char('Fabricant')
    acquisition_date = fields.Date('Date d\'acquisition', required=True, tracking=True)
    purchase_value = fields.Float('Valeur d\'achat (FCFA)', tracking=True)
    warranty_end_date = fields.Date('Fin de garantie', tracking=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('assigned', 'Affecté'),
        ('maintenance', 'En maintenance'),
        ('retired', 'Retiré'),
    ], 'État', default='draft', tracking=True)

    employee_id = fields.Many2one('hr.employee', 'Employé affecté', tracking=True)
    department_id = fields.Many2one('hr.department', 'Département', tracking=True)
    location = fields.Char('Localisation')

    is_under_warranty = fields.Boolean('Sous garantie?', compute='_compute_warranty_status')
    days_until_warranty_end = fields.Integer('Jours avant fin de garantie', compute='_compute_warranty_status')

    equipment_type = fields.Char('Type d\'équipement')
    processor = fields.Char('Processeur')
    ram_gb = fields.Integer('RAM (GB)')
    storage_gb = fields.Integer('Stockage (GB)')
    os = fields.Char('Système d\'exploitation')

    affectation_ids = fields.One2many('it.affectation', 'equipment_id', 'Historique d\'affectations')
    intervention_ids = fields.One2many('it.intervention', 'equipment_id', 'Interventions')
    contract_ids = fields.Many2many('it.contract', 'it_equipment_contract_rel', 'equipment_id', 'contract_id', 'Contrats')

    total_maintenance_cost = fields.Float('Coût total de maintenance', compute='_compute_maintenance_cost')
    maintenance_count = fields.Integer('Nombre d\'interventions', compute='_compute_maintenance_count')

    notes = fields.Text('Notes')

    @api.depends('warranty_end_date')
    def _compute_warranty_status(self):
        today = fields.Date.today()
        for record in self:
            if record.warranty_end_date:
                days_left = (record.warranty_end_date - today).days
                record.days_until_warranty_end = days_left
                record.is_under_warranty = days_left > 0
            else:
                record.is_under_warranty = False
                record.days_until_warranty_end = 0

    @api.depends('intervention_ids')
    def _compute_maintenance_cost(self):
        for record in self:
            record.total_maintenance_cost = sum(record.intervention_ids.mapped('cost'))

    @api.depends('intervention_ids')
    def _compute_maintenance_count(self):
        for record in self:
            record.maintenance_count = len(record.intervention_ids)

    def action_assign(self):
        self.state = 'assigned'

    def action_maintenance(self):
        self.state = 'maintenance'

    def action_retire(self):
        self.state = 'retired'

    def action_back_to_draft(self):
        self.state = 'draft'


class ITEquipmentCategory(models.Model):
    _name = 'it.equipment.category'
    _description = 'Catégorie d\'équipement'

    name = fields.Char('Nom', required=True)
    code = fields.Char('Code')
    description = fields.Text('Description')
