# E-Commerce Scraper - Plateforme de Veille Produits Tendances

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Plateforme web complète de veille e-commerce pour identifier les produits tendances avec scraping multi-sources, analyse de données en temps réel, et dashboard analytique.

## 🚀 Fonctionnalités

### Scraping Multi-Sources
- ✅ **Amazon** - Bestsellers, prix, reviews, ASIN
- ✅ **AliExpress** - Produits tendances, volumes de commandes, évaluations
- ✅ **eBay** - Articles vendus, trending searches
- ✅ **Shopify** - Détection de stores en croissance
- 🔄 **TikTok/Pinterest** - Détection produits viraux (à venir)

### Dashboard Analytique
- 📊 Top 100 produits tendances par catégorie
- 📈 Graphiques d'évolution des prix (30/60/90 jours)
- 💰 Calcul automatique du potentiel de profit
- 🎯 Score de saturation du marché
- 📉 Analyse de la concurrence
- 🔮 Prédictions de tendances

### Automatisation
- ⏰ Scraping quotidien automatique (2h du matin)
- 🔄 Mise à jour des prix toutes les 6h
- 📊 Calcul des tendances quotidien
- 🔔 Alertes Telegram/Email
- 📥 Export CSV/Excel hebdomadaire

## 🛠️ Stack Technique

### Backend
- **FastAPI** - API REST performante
- **PostgreSQL** - Base de données relationnelle
- **Redis** - Cache et files d'attente
- **Celery** - Tâches asynchrones
- **Playwright** - Scraping JavaScript
- **BeautifulSoup** - Parsing HTML

### Frontend
- **Next.js 14** - Framework React avec App Router
- **TypeScript** - Typage statique
- **Tailwind CSS** - Styling minimaliste
- **React-Admin** - Dashboard components
- **Recharts** - Graphiques interactifs

### Infrastructure
- **Docker** - Containerisation
- **Nginx** - Reverse proxy
- **Celery Beat** - Planification des tâches

## 📦 Installation

### Prérequis
- Docker & Docker Compose
- Node.js 20+ (pour développement frontend local)
- Python 3.11+ (pour développement backend local)

### Démarrage Rapide

1. **Cloner le repository**
\`\`\`bash
git clone <repo-url>
cd web-scrapper
\`\`\`

2. **Configuration des variables d'environnement**
\`\`\`bash
cp backend/.env.example backend/.env
# Éditer backend/.env avec vos clés API
\`\`\`

3. **Lancer avec Docker Compose**
\`\`\`bash
docker-compose up -d
\`\`\`

4. **Accéder à l'application**
- Frontend: http://localhost:3000
- API Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Installation Locale (Développement)

#### Backend
\`\`\`bash
cd backend
pip install -r requirements.txt
playwright install chromium
uvicorn main:app --reload
\`\`\`

#### Frontend
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

#### Celery Workers
\`\`\`bash
cd backend
celery -A celery_app worker --loglevel=info
celery -A celery_app beat --loglevel=info
\`\`\`

## 📊 Structure du Projet

\`\`\`
web-scrapper/
├── backend/
│   ├── api/                 # Endpoints FastAPI
│   │   ├── products.py      # CRUD produits
│   │   ├── analytics.py     # Analytics & insights
│   │   └── alerts.py        # Gestion alertes
│   ├── scrapers/            # Scrapers multi-sources
│   │   ├── amazon_scraper.py
│   │   ├── aliexpress_scraper.py
│   │   ├── ebay_scraper.py
│   │   └── shopify_scraper.py
│   ├── tasks/               # Tâches Celery
│   │   ├── scraping_tasks.py
│   │   ├── alert_tasks.py
│   │   └── export_tasks.py
│   ├── analytics/           # Analyse de données
│   ├── database/            # Schéma PostgreSQL
│   ├── models.py            # Modèles SQLAlchemy
│   ├── main.py              # Application FastAPI
│   └── celery_app.py        # Configuration Celery
├── frontend/
│   ├── src/
│   │   ├── app/             # Pages Next.js
│   │   ├── components/      # Composants React
│   │   └── lib/             # Utilitaires
│   ├── package.json
│   └── tailwind.config.js
├── nginx/
│   └── nginx.conf           # Configuration reverse proxy
└── docker-compose.yml       # Orchestration services
\`\`\`

## 🗄️ Base de Données

### Tables Principales
- **products** - Produits scrapés
- **price_history** - Historique des prix
- **competitors** - Liste des vendeurs concurrents
- **trends** - Scores de tendance calculés
- **alerts** - Notifications personnalisées
- **sentiment_analysis** - Analyse des avis clients
- **shopify_stores** - Tracking stores Shopify

## 🔧 Configuration

### Variables d'Environnement

\`\`\`env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce_scraper

# Redis
REDIS_URL=redis://localhost:6379/0

# API Keys (optionnel)
OPENAI_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_token_here
SENDGRID_API_KEY=your_key_here

# Scraping
PROXY_LIST=proxy1:port,proxy2:port
\`\`\`

## 📈 Utilisation

### Lancer un Scraping Manuel
\`\`\`python
from tasks.scraping_tasks import scrape_all_sources
scrape_all_sources.delay()
\`\`\`

### Créer une Alerte
\`\`\`bash
curl -X POST http://localhost:8000/api/alerts/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "product_id": 1,
    "type_alerte": "price_drop",
    "seuil": 50.00
  }'
\`\`\`

### Exporter les Données
\`\`\`python
from tasks.export_tasks import export_weekly_report
export_weekly_report.delay()
\`\`\`

## 🎨 Design

Le dashboard utilise un **thème sombre minimaliste** avec:
- Palette de couleurs harmonieuse
- Animations fluides et micro-interactions
- Glassmorphism subtil
- Typographie moderne (Inter font)
- Responsive design

## 🔒 Sécurité & Optimisations

- ✅ Rotation de proxies pour éviter les bans
- ✅ Rate limiting respectueux
- ✅ Cache intelligent (pas de scrape si données <6h)
- ✅ Gestion d'erreurs robuste
- ✅ Logs détaillés pour debugging

## 📝 API Endpoints

### Products
- `GET /api/products` - Liste produits avec filtres
- `GET /api/products/trending` - Top produits tendances
- `GET /api/products/{id}` - Détail produit
- `GET /api/products/{id}/history` - Historique prix
- `GET /api/products/{id}/competitors` - Concurrents

### Analytics
- `GET /api/analytics/profit` - Opportunités de profit
- `GET /api/analytics/saturation` - Saturation marché
- `GET /api/analytics/trends/predictions` - Prédictions
- `GET /api/analytics/seasonal` - Produits saisonniers
- `GET /api/analytics/dashboard/summary` - Résumé dashboard

### Alerts
- `GET /api/alerts` - Liste alertes
- `POST /api/alerts` - Créer alerte
- `PUT /api/alerts/{id}` - Modifier alerte
- `DELETE /api/alerts/{id}` - Supprimer alerte

## 🚀 Roadmap

- [ ] Détection produits viraux TikTok/Pinterest
- [ ] Sentiment analysis avec IA (transformers)
- [ ] Reverse image search
- [ ] Générateur de descriptions avec IA
- [ ] Application mobile
- [ ] Intégration Shopify API

## 📄 License

MIT License - voir LICENSE file

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou un pull request.

## 📧 Contact

Pour toute question ou suggestion, contactez-nous.

---

**Made with ❤️ for e-commerce entrepreneurs**
