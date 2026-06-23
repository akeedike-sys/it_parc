/** @odoo-module **/

import { registry } from '@web/core/registry';
import { Component } from '@odoo/owl';
import { useService } from '@web/core/utils/hooks';

export class ITDashboard extends Component {
    static template = 'it_parc.dashboard';

    setup() {
        this.rpc = useService('rpc');
        this.actionService = useService('action');
        this.loadDashboardData();
    }

    async loadDashboardData() {
        try {
            // Charger les données depuis les modèles
            const equipmentData = await this.rpc('/web/dataset/search_read', {
                model: 'it.equipment',
                fields: ['id', 'name', 'state', 'is_under_warranty', 'category_id', 'total_maintenance_cost'],
                domain: [],
            });

            const interventionData = await this.rpc('/web/dataset/search_read', {
                model: 'it.intervention',
                fields: ['id', 'name', 'equipment_id', 'intervention_type', 'technician_id', 'start_date', 'cost'],
                domain: [],
                order: 'start_date desc',
                limit: 10,
            });

            const alertData = await this.rpc('/web/dataset/search_read', {
                model: 'it.alert',
                fields: ['id', 'name', 'alert_type', 'target_date', 'state', 'days_before'],
                domain: [['state', '!=', 'resolved']],
            });

            // Calculer les KPIs
            this.updateKPIs(equipmentData);

            // Générer le graphique
            this.generateChart(equipmentData);

            // Afficher les alertes
            this.displayAlerts(alertData);

            // Afficher les états
            this.displayStatusGrid(equipmentData);

            // Afficher les interventions récentes
            this.displayRecentInterventions(interventionData);

        } catch (error) {
            console.error('Erreur lors du chargement du dashboard:', error);
        }
    }

    updateKPIs(equipmentData) {
        const total = equipmentData.length;
        const assigned = equipmentData.filter(e => e.state === 'assigned').length;
        const warranty = equipmentData.filter(e => e.is_under_warranty).length;
        const totalCost = equipmentData.reduce((sum, e) => sum + (e.total_maintenance_cost || 0), 0);

        document.getElementById('total_equipment').textContent = total;
        document.getElementById('assigned_equipment').textContent = assigned;
        document.getElementById('warranty_equipment').textContent = warranty;
        document.getElementById('total_maintenance_cost').textContent = this.formatCurrency(totalCost);
    }

    generateChart(equipmentData) {
        // Compter les équipements par catégorie
        const categoryMap = {};
        equipmentData.forEach(equipment => {
            const categoryName = equipment.category_id[1] || 'Sans catégorie';
            categoryMap[categoryName] = (categoryMap[categoryName] || 0) + 1;
        });

        const ctx = document.getElementById('categoryChart');
        if (!ctx) return;

        const labels = Object.keys(categoryMap);
        const data = Object.values(categoryMap);
        const colors = [
            '#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6',
            '#1abc9c', '#34495e', '#e67e22', '#95a5a6', '#16a085'
        ];

        // Utiliser Chart.js s'il est disponible
        if (typeof Chart !== 'undefined') {
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: colors.slice(0, labels.length),
                        borderColor: '#fff',
                        borderWidth: 2,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        }
                    }
                }
            });
        }
    }

    displayAlerts(alertData) {
        const container = document.getElementById('alerts_container');
        if (!container) return;

        if (alertData.length === 0) {
            container.innerHTML = '<div class="it-no-alerts">✓ Aucune alerte active</div>';
            return;
        }

        const alertsHTML = alertData.map(alert => {
            const days = alert.days_before || 0;
            const typeClass = alert.alert_type;
            const typeLabel = {
                'warranty': 'Garantie',
                'contract': 'Contrat',
                'maintenance': 'Maintenance'
            }[alert.alert_type] || alert.alert_type;

            return `
                <div class="it-alert-item ${typeClass}">
                    <div>
                        <div class="it-alert-type">${typeLabel}</div>
                        <div style="font-size: 12px; color: #7f8c8d; margin-top: 4px;">${alert.name}</div>
                    </div>
                    <div class="it-alert-days">${days}j</div>
                </div>
            `;
        }).join('');

        container.innerHTML = alertsHTML;
    }

    displayStatusGrid(equipmentData) {
        const container = document.getElementById('status_grid');
        if (!container) return;

        const states = {
            'draft': 'Brouillon',
            'assigned': 'Affecté',
            'maintenance': 'En maintenance',
            'retired': 'Retiré'
        };

        let html = '';
        Object.entries(states).forEach(([state, label]) => {
            const count = equipmentData.filter(e => e.state === state).length;
            html += `
                <div class="it-status-badge ${state}">
                    <div class="it-status-name">${label}</div>
                    <div class="it-status-count">${count}</div>
                </div>
            `;
        });

        container.innerHTML = html;
    }

    displayRecentInterventions(interventionData) {
        const tbody = document.querySelector('.it-recent-interventions tbody');
        if (!tbody) return;

        if (interventionData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="it-no-data">Aucune intervention enregistrée</td></tr>';
            return;
        }

        const rows = interventionData.map(intervention => {
            const typeLabel = {
                'corrective': 'Corrective',
                'preventive': 'Préventive'
            }[intervention.intervention_type] || intervention.intervention_type;

            const date = new Date(intervention.start_date);
            const formattedDate = date.toLocaleDateString('fr-FR');

            return `
                <tr>
                    <td>${intervention.equipment_id[1]}</td>
                    <td>${typeLabel}</td>
                    <td>${intervention.technician_id[1]}</td>
                    <td>${formattedDate}</td>
                    <td>${this.formatCurrency(intervention.cost)}</td>
                </tr>
            `;
        }).join('');

        tbody.innerHTML = rows;
    }

    formatCurrency(value) {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'XOF',
            minimumFractionDigits: 0,
        }).format(value);
    }
}

// Enregistrer le composant
registry.category('actions').add('it_dashboard', ITDashboard);
