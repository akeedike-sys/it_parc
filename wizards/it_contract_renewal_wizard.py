from odoo import models, fields, api
from datetime import timedelta


class ITContractRenewalWizard(models.TransientModel):
    _name = 'it.contract.renewal.wizard'
    _description = 'Wizard de renouvellement de contrat'

    contract_id = fields.Many2one('it.contract', 'Contrat', required=True)
    new_start_date = fields.Date('Nouvelle date de début', required=True)
    new_end_date = fields.Date('Nouvelle date de fin', required=True)
    new_amount = fields.Float('Nouveau montant (FCFA)', required=True)
    notes = fields.Text('Notes de renouvellement')

    @api.onchange('contract_id')
    def _onchange_contract_id(self):
        if self.contract_id:
            # Suggérer une date de début le lendemain de la fin du contrat actuel
            self.new_start_date = self.contract_id.end_date + timedelta(days=1)
            # Suggérer une fin d'un an plus tard
            self.new_end_date = self.new_start_date + timedelta(days=365)
            self.new_amount = self.contract_id.amount

    def action_renew(self):
        self.ensure_one()
        # Créer un nouveau contrat
        new_contract = self.env['it.contract'].create({
            'name': f'{self.contract_id.name} - Renouvelé',
            'vendor_id': self.contract_id.vendor_id.id,
            'contract_type': self.contract_id.contract_type,
            'start_date': self.new_start_date,
            'end_date': self.new_end_date,
            'amount': self.new_amount,
            'notes': self.notes,
        })
        # Lier les mêmes équipements au nouveau contrat
        new_contract.equipment_ids = self.contract_id.equipment_ids
        return {'type': 'ir.actions.act_window_close'}
