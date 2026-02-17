# 🌟 HandiHelper - Plateforme d'Accompagnement pour Familles d'Enfants Handicapés

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data](https://img.shields.io/badge/Data-Open%20Data-orange.svg)](https://www.data.gouv.fr)

> **Une solution data-driven pour simplifier le parcours des familles d'enfants en situation de handicap en France**

---

## 📌 Contexte du Projet

En France, des milliers de familles d'enfants handicapés font face à :
- 🔍 Un **parcours du combattant administratif**
- 📄 Une **information dispersée** sur de multiples plateformes
- 😰 Un **isolement** face aux défis quotidiens
- ⏰ Une **charge mentale** énorme pour trouver les bonnes ressources

**HandiHelper** centralise toutes ces informations et utilise la data science pour personnaliser l'accompagnement.

---

## 🎯 Objectifs du Projet

### Objectif Principal
Créer une **chaîne complète de traitement de données** pour :
- ✅ **Collecter** des données hétérogènes (web scraping, API, open data)
- ✅ **Intégrer** et nettoyer ces données dans une base SQL
- ✅ **Analyser** et produire des indicateurs pertinents
- ✅ **Visualiser** les résultats via des dashboards interactifs
- ✅ **Exposer** les données via une API REST

### Impact Social
Aider les familles à :
- 🗺️ **Localiser** rapidement les établissements adaptés près de chez elles
- 💰 **Identifier** les aides financières disponibles
- 📊 **Comparer** les options selon leurs besoins spécifiques
- 🤝 **Connecter** avec d'autres familles

---

## 🛠️ Stack Technique

### Technologies Utilisées

| Domaine | Technologies |
|---------|-------------|
| **Web Scraping** | Python, BeautifulSoup, Selenium, Requests |
| **Data Processing** | Pandas, NumPy |
| **Base de Données** | MySQL / PostgreSQL |
| **API** | Flask / FastAPI |
| **Visualisation** | Plotly, Matplotlib, Seaborn, Folium |
| **Frontend** | HTML/CSS/JavaScript (optionnel) |

---

## 📊 Sources de Données

### 1. Open Data (data.gouv.fr)
- **FINESS** : 12 000+ établissements médico-sociaux
  - IME, SESSAD, ESAT, MAS, FAM, etc.
  - Coordonnées GPS pour géolocalisation
  - Capacités d'accueil et types de handicap

### 2. Web Scraping
- **Pages Jaunes** : Professionnels libéraux
  - Orthophonistes, psychomotriciens, ergothérapeutes
  - 500+ professionnels collectés
- **Sanitaire-Social.com** : Détails établissements spécialisés
- **Service-Public.fr** : Informations sur les aides financières
  - AAH, PCH, AEEH, MVA, etc.

### 3. APIs Publiques
- **API Adresse** (api.gouv.fr) : Géolocalisation
- **API Open Data** : Enrichissement des données

---

## 🏗️ Architecture du Projet

```
HandiHelper/
├── data/                          # Données brutes et traitées
│   ├── raw/                       # Données brutes
│   │   ├── finess_raw.csv
│   │   ├── pagesjaunes_raw.csv
│   │   └── aides_raw.csv
│   └── processed/                 # Données nettoyées
│       └── handhelper_clean.csv
│
├── scrapers/                      # Scripts de scraping
│   ├── finess_downloader.py       # Téléchargeur FINESS
│   ├── pagesjaunes_scraper.py     # Scraper Pages Jaunes
│   ├── sanitaire_scraper.py       # Scraper annuaires spécialisés
│   └── aides_scraper.py           # Scraper aides financières
│
├── database/                      # Scripts base de données
│   ├── schema.sql                 # Schéma SQL
│   ├── load_data.py               # Chargement des données
│   └── queries.sql                # Requêtes d'analyse
│
├── api/                           # API REST
│   ├── app.py                     # Application Flask/FastAPI
│   ├── routes.py                  # Endpoints API
│   └── models.py                  # Modèles de données
│
├── analysis/                      # Analyses et indicateurs
│   ├── indicators.py              # Calcul des KPIs
│   └── statistics.py              # Analyses statistiques
│
├── visualization/                 # Visualisations
│   ├── dashboard.py               # Dashboard interactif
│   ├── maps.py                    # Cartes géographiques
│   └── charts.py                  # Graphiques
│
├── docs/                          # Documentation
│   ├── technical_doc.md           # Documentation technique
│   └── user_guide.md              # Guide utilisateur
│
├── requirements.txt               # Dépendances Python
├── README.md                      # Ce fichier
└── LICENSE                        # Licence du projet
```

---

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.8+
- MySQL / PostgreSQL
- pip (gestionnaire de paquets Python)

### Installation

```bash
# 1. Cloner le repository
git clone https://github.com/votre-username/HandiHelper.git
cd HandiHelper

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Sur Windows:
venv\Scripts\activate
# Sur Mac/Linux:
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Configurer la base de données
mysql -u root -p < database/schema.sql
```

### Collecte des Données

```bash
# Télécharger FINESS (Open Data)
python scrapers/finess_downloader.py

# Scraper Pages Jaunes
python scrapers/pagesjaunes_scraper.py

# Scraper aides financières
python scrapers/aides_scraper.py
```

### Chargement en Base de Données

```bash
# Charger les données dans MySQL
python database/load_data.py
```

### Lancer l'API

```bash
# Démarrer l'API REST
python api/app.py

# L'API sera accessible sur http://localhost:5000
```

---

## 📊 Indicateurs Clés (KPIs)

### Couverture Territoriale
- **Nombre d'établissements par département**
- **Taux de couverture** (ratio population/structures)
- **Zones blanches** (départements sous-dotés)

### Accessibilité
- **Distance moyenne** au plus proche établissement
- **Temps de trajet** estimé
- **Disponibilité** des places

### Diversité de l'Offre
- **Types d'établissements** disponibles par région
- **Spécialisations** par type de handicap
- **Services complémentaires** (transport, restauration)

---

## 🌐 API REST - Endpoints

### Établissements

```http
GET /api/etablissements
```
Récupère tous les établissements

**Paramètres:**
- `type` : Type d'établissement (IME, SESSAD, etc.)
- `departement` : Code département (75, 69, etc.)
- `handicap` : Type de handicap
- `limit` : Nombre de résultats (défaut: 50)

**Exemple:**
```bash
curl "http://localhost:5000/api/etablissements?type=IME&departement=75&limit=10"
```

### Recherche Géographique

```http
GET /api/etablissements/nearby
```
Trouve les établissements à proximité

**Paramètres:**
- `lat` : Latitude
- `lon` : Longitude
- `radius` : Rayon en km (défaut: 10)

### Aides Financières

```http
GET /api/aides
```
Liste les aides disponibles

**Paramètres:**
- `age_enfant` : Âge de l'enfant
- `type_handicap` : Type de handicap

---

## 📈 Visualisations

### Carte Interactive
- 🗺️ **Carte de France** avec géolocalisation des établissements
- 📍 **Filtres** par type, département, disponibilité
- 🔍 **Zoom** sur une région spécifique

### Dashboards
- 📊 **Répartition** par type d'établissement
- 🌡️ **Heatmap** de densité territoriale
- 📈 **Évolution** temporelle des créations
- 🎯 **Indicateurs** de couverture par région

---

## 🧪 Exemples d'Utilisation

### Cas d'Usage 1 : Recherche d'un IME à Paris

```python
from api.client import HandiHelperClient

client = HandiHelperClient()

# Rechercher des IME à Paris
ime_paris = client.search_etablissements(
    type="IME",
    departement="75",
    limite=5
)

for etab in ime_paris:
    print(f"{etab['nom']} - {etab['adresse']}")
    print(f"Téléphone: {etab['telephone']}")
```

### Cas d'Usage 2 : Carte des SESSAD en Île-de-France

```python
from visualization.maps import create_map

# Créer une carte interactive
map_idf = create_map(
    type_etablissement="SESSAD",
    departements=["75", "92", "93", "94", "95", "77", "78", "91"]
)

map_idf.save("sessad_idf.html")
```

---

## 📊 Résultats du Projet

### Données Collectées
- ✅ **12 456** établissements handicap (FINESS)
- ✅ **847** professionnels libéraux (Pages Jaunes)
- ✅ **7** aides financières détaillées
- ✅ **101** départements couverts

### Indicateurs Produits
- 📊 **Taux de couverture** par département
- 🗺️ **Cartographie** complète de l'offre
- 📈 **Analyse** des zones sous-dotées
- 💰 **Simulateur** d'aides financières

### Impact Attendu
- ⏱️ **Réduction de 70%** du temps de recherche
- 🎯 **Meilleure orientation** vers les structures adaptées
- 💡 **Connaissance accrue** des droits et aides
- 🤝 **Désenclavement** des familles isolées

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment participer :

1. **Fork** le projet
2. Créez une **branche** pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. **Committez** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une **Pull Request**

---

## 📝 Licence

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- **data.gouv.fr** pour les données FINESS
- **Pages Jaunes** pour les annuaires professionnels
- **Service-Public.fr** pour les informations sur les aides
- **Communauté Open Source** pour les outils utilisés

---

## 🔮 Roadmap Future

### Phase 2 (Q2 2025)
- [ ] **Application mobile** (React Native)
- [ ] **Système de recommandation** avec ML
- [ ] **Communauté** d'entraide entre familles
- [ ] **Chatbot IA** pour accompagnement personnalisé

### Phase 3 (Q3 2025)
- [ ] **Partenariats** avec MDPH
- [ ] **Intégration** des délais d'attente
- [ ] **Système de notation** des établissements
- [ ] **Multilingue** (Anglais, Arabe, etc.)

---

<div align="center">

**⭐ Si ce projet vous aide, n'oubliez pas de mettre une étoile ! ⭐**

Made with ❤️ for families

</div>
