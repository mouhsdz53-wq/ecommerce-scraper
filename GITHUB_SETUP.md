# 🚀 Guide Push GitHub et Codespaces

## ✅ Git Initialisé

Le repository Git a été initialisé avec succès :
- **43 fichiers** ajoutés
- **Premier commit** créé
- **Configuration Codespaces** ajoutée

## 📤 Étapes pour Pousser sur GitHub

### 1. Créer un Repository sur GitHub

1. Va sur https://github.com/new
2. Nom du repository : `ecommerce-scraper` (ou autre nom)
3. **NE PAS** initialiser avec README, .gitignore ou license
4. Clique sur "Create repository"

### 2. Pousser le Code

Copie l'URL de ton repository (exemple: `https://github.com/TON_USERNAME/ecommerce-scraper.git`)

Puis exécute ces commandes :

```bash
# Ajouter le remote GitHub
git remote add origin https://github.com/TON_USERNAME/ecommerce-scraper.git

# Pousser le code
git branch -M main
git push -u origin main
```

### 3. Lancer dans GitHub Codespaces

Une fois poussé sur GitHub :

1. Va sur ton repository GitHub
2. Clique sur **"Code"** (bouton vert)
3. Sélectionne l'onglet **"Codespaces"**
4. Clique sur **"Create codespace on main"**
5. Attends 2-3 minutes que Codespaces démarre

### 4. Démarrer la Plateforme dans Codespaces

Une fois Codespaces ouvert :

```bash
# Créer le fichier .env
cp backend/.env.example backend/.env

# Lancer tous les services Docker
docker-compose up -d

# Attendre 30 secondes puis vérifier
docker-compose ps
```

### 5. Accéder aux Services

Codespaces va automatiquement forward les ports :

- **Frontend** : Clique sur le port 3000 dans l'onglet "Ports"
- **Backend API** : Clique sur le port 8000
- **API Docs** : Port 8000 puis ajoute `/docs` à l'URL

## 🔧 Commandes Utiles dans Codespaces

```bash
# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Redémarrer
docker-compose restart

# Lancer un scraping manuel
docker exec -it ecommerce_scraper_backend python -c "from tasks.scraping_tasks import scrape_all_sources; scrape_all_sources()"
```

## 📝 Configuration Optionnelle

### Variables d'Environnement

Édite `backend/.env` pour ajouter tes clés API :

```env
# Telegram (optionnel)
TELEGRAM_BOT_TOKEN=ton_token_ici
TELEGRAM_CHAT_ID=ton_chat_id_ici

# Email (optionnel)
SENDGRID_API_KEY=ta_clé_sendgrid_ici

# Proxies (optionnel)
PROXY_LIST=proxy1:port,proxy2:port
```

## ✨ Fonctionnalités Disponibles

Une fois lancé dans Codespaces, tu auras accès à :

✅ **Dashboard temps réel** (port 3000)
✅ **API REST complète** (port 8000)
✅ **Documentation Swagger** (port 8000/docs)
✅ **Scraping automatisé** (quotidien + 6h)
✅ **Base de données PostgreSQL**
✅ **Cache Redis**
✅ **Celery workers** pour automation

## 🎯 Prochaines Étapes

1. Push sur GitHub
2. Créer Codespace
3. Lancer `docker-compose up -d`
4. Accéder au dashboard sur port 3000
5. Profiter de la plateforme ! 🚀

## 🆘 Troubleshooting

**Si Docker ne démarre pas dans Codespaces :**
```bash
# Vérifier que Docker est installé
docker --version

# Si besoin, installer Docker
sudo apt-get update
sudo apt-get install docker.io docker-compose
```

**Si les ports ne sont pas accessibles :**
- Va dans l'onglet "Ports" en bas de VS Code
- Vérifie que les ports 3000 et 8000 sont "Public" ou "Private to Organization"

**Si la base de données ne démarre pas :**
```bash
# Vérifier les logs PostgreSQL
docker-compose logs postgres

# Recréer les containers
docker-compose down -v
docker-compose up -d
```

---

**Prêt à déployer sur GitHub Codespaces ! 🎉**
