from odoo import models, fields, api
from io import StringIO
import csv
import base64


class ITImportWizard(models.TransientModel):
    _name = 'it.import.wizard'
    _description = 'Wizard d\'import d\'équipements'

    csv_file = fields.Binary('Fichier CSV', required=True)
    filename = fields.Char('Nom du fichier')
    import_report = fields.Text('Rapport d\'import', readonly=True)

    def action_import(self):
        self.ensure_one()
        try:
            csv_data = base64.b64decode(self.csv_file).decode('utf-8')
            csv_reader = csv.DictReader(StringIO(csv_data), delimiter=',')

            created = 0
            skipped = 0
            errors = []

            for row in csv_reader:
                try:
                    # Vérifier si l'équipement existe déjà
                    existing = self.env['it.equipment'].search([
                        ('serial_number', '=', row.get('serial_number', ''))
                    ])
                    if existing:
                        skipped += 1
                        continue

                    # Créer l'équipement
                    category = self.env['it.equipment.category'].search([
                        ('name', '=', row.get('category', 'Autre'))
                    ], limit=1)
                    if not category:
                        category = self.env['it.equipment.category'].create({
                            'name': row.get('category', 'Autre'),
                        })

                    self.env['it.equipment'].create({
                        'name': row.get('name', 'Équipement sans nom'),
                        'serial_number': row.get('serial_number', ''),
                        'category_id': category.id,
                        'manufacturer': row.get('manufacturer', ''),
                        'model': row.get('model', ''),
                        'acquisition_date': row.get('acquisition_date', fields.Date.today()),
                        'purchase_value': float(row.get('purchase_value', 0)),
                        'state': 'draft',
                    })
                    created += 1
                except Exception as e:
                    errors.append(f"Erreur ligne {csv_reader.line_num}: {str(e)}")

            report = f"""
Rapport d'import CSV
====================
Fichier: {self.filename}
Total lignes traitées: {created + skipped + len(errors)}

Équipements créés: {created}
Équipements ignorés (doublon): {skipped}
Erreurs: {len(errors)}

"""
            if errors:
                report += "Détails des erreurs:\n" + "\n".join(errors)

            self.import_report = report
        except Exception as e:
            self.import_report = f"Erreur lors de l'import: {str(e)}"

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'it.import.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
