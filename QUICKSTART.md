# E-Commerce Scraper - Quick Start Guide

## Démarrage Rapide (5 minutes)

### 1. Prérequis
```bash
# Vérifier Docker
docker --version
docker-compose --version
```

### 2. Configuration
```bash
# Copier le fichier d'environnement
cp backend/.env.example backend/.env

# Éditer backend/.env avec vos clés API (optionnel pour démarrage)
# Les clés API sont optionnelles, la plateforme fonctionne sans
```

### 3. Lancement
```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier les logs
docker-compose logs -f
```

### 4. Accès
- **Frontend Dashboard**: http://localhost:3000
- **API Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Nginx (Production)**: http://localhost

### 5. Premier Scraping Manuel
```bash
# Se connecter au container backend
docker exec -it ecommerce_scraper_backend bash

# Lancer un scraping manuel
python -c "from tasks.scraping_tasks import scrape_all_sources; scrape_all_sources()"
```

## Services Disponibles

### Backend (Port 8000)
- FastAPI avec auto-documentation
- PostgreSQL pour stockage
- Redis pour cache
- Celery pour automation

### Frontend (Port 3000)
- Next.js 14 avec React
- Dashboard temps réel
- Thème sombre minimaliste

### Celery Workers
- Scraping quotidien (2h du matin)
- Mise à jour prix (toutes les 6h)
- Calcul tendances (quotidien)
- Alertes (toutes les heures)

## Commandes Utiles

### Docker
```bash
# Arrêter tous les services
docker-compose down

# Rebuild après modifications
docker-compose up -d --build

# Voir les logs d'un service
docker-compose logs -f backend
docker-compose logs -f frontend

# Accéder à la base de données
docker exec -it ecommerce_scraper_db psql -U scraper_user -d ecommerce_scraper
```

### Backend
```bash
# Installer les dépendances localement
cd backend
pip install -r requirements.txt

# Lancer le serveur en dev
uvicorn main:app --reload

# Lancer Celery worker
celery -A celery_app worker --loglevel=info

# Lancer Celery beat (scheduler)
celery -A celery_app beat --loglevel=info
```

### Frontend
```bash
# Installer les dépendances
cd frontend
npm install

# Lancer en dev
npm run dev

# Build production
npm run build
npm start
```

## Tests API

### Récupérer les produits
```bash
curl http://localhost:8000/api/products?limit=10
```

### Récupérer les tendances
```bash
curl http://localhost:8000/api/products/trending?limit=20
```

### Récupérer le résumé dashboard
```bash
curl http://localhost:8000/api/analytics/dashboard/summary
```

### Créer une alerte
```bash
curl -X POST http://localhost:8000/api/alerts/ \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "type_alerte": "price_drop",
    "seuil": 50.00
  }'
```

## Troubleshooting

### Le backend ne démarre pas
```bash
# Vérifier les logs
docker-compose logs backend

# Vérifier que PostgreSQL est prêt
docker-compose ps
```

### Le frontend ne se connecte pas à l'API
```bash
# Vérifier la variable d'environnement
echo $NEXT_PUBLIC_API_URL

# Devrait être: http://localhost:8000
```

### Celery ne fonctionne pas
```bash
# Vérifier Redis
docker exec -it ecommerce_scraper_redis redis-cli ping

# Vérifier les workers
docker-compose logs celery_worker
```

## Configuration Avancée

### Ajouter des proxies
```env
# Dans backend/.env
PROXY_LIST=proxy1.com:8080,proxy2.com:8080,proxy3.com:8080
```

### Configurer Telegram
```env
# Dans backend/.env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### Configurer Email
```env
# Dans backend/.env
SENDGRID_API_KEY=your_sendgrid_key
FROM_EMAIL=noreply@yourdomain.com
```

## Prochaines Étapes

1. ✅ Vérifier que tous les services sont lancés
2. ✅ Accéder au dashboard sur http://localhost:3000
3. ✅ Lancer un premier scraping manuel
4. ✅ Configurer les alertes
5. ✅ Personnaliser les catégories à scraper
6. ✅ Déployer en production (optionnel)

## Support

Pour toute question, consultez:
- README.md principal
- Documentation API: http://localhost:8000/docs
- Logs: `docker-compose logs -f`
