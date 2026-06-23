# Module Odoo 18 Gestion de Parc Informatique it_parc

Vue d'ensemble

Le module it_parc est un module Odoo 18 personnalisé permettant une gestion complète et structurée du parc informatique d'une entreprise. Il s'intègre nativement à Odoo 18 et offre une visibilité totale sur les équipements, les interventions de maintenance, les contrats fournisseurs et les alertes automatiques.

Développé pour : TECHPARK CI - Abidjan, Côte d'Ivoire

Version : 18.0.1.0.0

License : AGPL-3

Caractéristiques principales

 Gestion centralisée des équipements

Enregistrement complet des équipements informatiques
Suivi des caractéristiques techniques (processeur, RAM, stockage, OS)
Numérotation unique par numéro de série
Historique complet des affectations et interventions
États d'équipement : Brouillon → Affecté → En maintenance → Retiré

 Traçabilité des affectations

Attribution des équipements aux employés et départements
Historique détaillé de toutes les mutations
Dates d'affectation et de retour automatisées
Wizard de réaffectation avec motif

 Suivi des interventions de maintenance

Enregistrement des interventions correctives et préventives
Calcul automatique de la durée
Coût par intervention
Rapports détaillés par technicien
État du ticket : Brouillon → En cours → Terminée

 Gestion des contrats fournisseurs

Suivi des contrats de maintenance, licence et support
Calcul automatique des jours restants
Alertes automatiques d'expiration (60 jours avant)
Wizard de renouvellement avec suggestions
Liaison avec les équipements couverts

 Système d'alertes automatiques

Alertes garantie (fin de garantie approchant)
Alertes contrats (expiration approchant)
Alertes maintenance préventive
Génération automatique via tâche planifiée (cron)
État : En attente → Prise en compte → Résolu

 Import en masse (CSV)

Wizard d'import d'inventaire CSV
Détection automatique de doublon par numéro de série
Rapport d'import détaillé
Création de catégories manquantes

 Rapports PDF (QWeb)

Fiche d'équipement : Détail complet d'un équipement
Rapport d'inventaire : Vue d'ensemble du parc complet
Historique des maintenances : Détails des interventions par période

 Tableau de bord personnalisé (OWL)

 KPIs principaux

Total d'équipements
Équipements affectés
Équipements sous garantie
Coût total de maintenance

Graphique et alertes

Distribution des équipements par catégorie
Affichage des alertes actives
Nombre d'équipements par état
Historique des 10 dernières interventions

Structure du module

it_parc/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── it_equipment.py
│   ├── it_affectation.py
│   ├── it_intervention.py
│   ├── it_contract.py
│   └── it_alert.py
├── views/
│   ├── it_menus.xml
│   ├── it_equipment_views.xml
│   ├── it_affectation_views.xml
│   ├── it_intervention_views.xml
│   ├── it_contract_views.xml
│   ├── it_alert_views.xml
│   └── it_dashboard_views.xml
├── wizards/
│   ├── __init__.py
│   ├── it_affectation_wizard.py
│   ├── it_affectation_wizard_views.xml
│   ├── it_import_wizard.py
│   ├── it_import_wizard_views.xml
│   ├── it_contract_renewal_wizard.py
│   └── it_contract_renewal_wizard_views.xml
├── report/
│   ├── it_equipment_report.xml
│   ├── it_inventory_report.xml
│   └── it_maintenance_report.xml
├── security/
│   ├── groups.xml
│   ├── ir.model.access.csv
│   └── ir_rules.xml
├── static/
│   └── src/
│       ├── css/
│       │   └── it_dashboard.css
│       └── js/
│           └── it_dashboard.js
└── data/
    └── it_parc_demo.xml

Installation

Prérequis

Odoo 8 Enterprise
Python 3.11+
PostgreSQL 12+ Déploiement du module

Installation dans Odoo

Via interface web :

Allez à Paramètres → Modules → Modules
Cliquez sur Mettre à jour la liste
Cherchez Gestion de Parc Informatique
Cliquez sur Installer

Via ligne de commande (Docker) :

bashdocker exec odoo odoo -d your_database --init it_parc -r odoo -w odoo --stop-after-init

 Configuration initiale

Les groupes de sécurité sont créés automatiquement :

IT Technicien : Accès lecture/création interventions
IT Manager : Accès complet (lecture/modification/suppression)

Allez à Paramètres → Utilisateurs et Sociétés → Utilisateurs pour assigner les groupes.

Utilisation

Accéder au module

Depuis le menu Odoo, vous verrez "Gestion Parc IT" contenant :

Gestion Parc IT
├── Tableau de bord
├── Équipements
│   ├── Liste des équipements
│   └── Catégories
├── Affectations
│   └── Historique des affectations
├── Interventions
│   └── Liste des interventions
├── Contrats
│   └── Liste des contrats
├── Alertes
│   └── Alertes
└── Outils
    └── Importer CSV

 Gestion des équipements

Créer un équipement :

Allez à Gestion Parc IT → Équipements → Liste des équipements
Cliquez sur Créer
Remplissez les champs :

Nom : Identifiant de l'équipement
Numéro de série : Identifiant unique
Catégorie : DESKTOP, LAPTOP, PRINTER, SERVER, NETWORK
Dates et garantie : Acquisition, fin de garantie

Cliquez sur Enregistrer

Affecter un équipement :

Depuis la fiche équipement, cliquez sur "Affecter"
L'équipement passe à l'état "Affecté"

 Interventions de maintenance

Créer une intervention :

Allez à Gestion Parc IT → Interventions
Cliquez sur Créer
Sélectionnez l'équipement et le type (Corrective/Préventive)
Assignez un technicien et entrez la description
Cliquez sur "Démarrer" pour commencer
Cliquez sur "Terminer" quand c'est fait

 Rapports PDF

Fiche d'équipement :

Ouvrez un équipement
Cliquez sur Imprimer → Fiche d'équipement

Rapport d'inventaire :

Allez à Gestion Parc IT → Équipements → Liste
Cliquez sur Imprimer → Rapport d'inventaire

Sécurité et accès

Groupes de sécurité

GroupeÉquipementsInterventionsContratsAlertesIT TechnicienLectureLecture + CréationLectureLecture + ModificationIT ManagerCRUDCRUDCRUDCRUD

Règles d'accès

Equipements : Tous (lecture) / Managers (CRUD)
Interventions : Techniciens ne peuvent modifier que leurs propres tickets
Contrats : Tous (lecture) / Managers (CRUD)
Alertes : Techniciens ne peuvent pas créer

Données de démonstration

Le module inclut :

10 Équipements : DELL, HP, ASUS, Lenovo, Cisco, Canon, Synology, Microsoft
3 Contrats : Dell Support, Microsoft Office 365, HP Maintenance
5 Interventions : Maintenances préventives et correctives
