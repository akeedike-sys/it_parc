from odoo import models, fields, api


class ITAffectationWizard(models.TransientModel):
    _name = 'it.affectation.wizard'
    _description = 'Wizard de réaffectation d\'équipement'

    equipment_id = fields.Many2one('it.equipment', 'Équipement', required=True)
    new_employee_id = fields.Many2one('hr.employee', 'Nouvel employé', required=True)
    new_department_id = fields.Many2one('hr.department', 'Nouveau département')
    reason = fields.Text('Motif de la réaffectation')

    def action_reassign(self):
        self.ensure_one()
        # Créer une nouvelle affectation
        self.env['it.affectation'].create({
            'equipment_id': self.equipment_id.id,
            'employee_id': self.new_employee_id.id,
            'department_id': self.new_department_id.id,
            'reason': self.reason,
        })
        # Mettre à jour l'équipement
        self.equipment_id.employee_id = self.new_employee_id
        self.equipment_id.department_id = self.new_department_id
        self.equipment_id.state = 'assigned'
        return {'type': 'ir.actions.act_window_close'}
