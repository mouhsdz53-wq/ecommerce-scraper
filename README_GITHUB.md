# E-Commerce Scraper Platform

Plateforme complète de veille e-commerce avec scraping multi-sources (Amazon, AliExpress, eBay, Shopify, TikTok/Pinterest), analyse de données en temps réel, et dashboard analytique.

## 🚀 Quick Start avec GitHub Codespaces

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new)

### Démarrage en Codespaces

1. Cliquer sur "Code" > "Codespaces" > "Create codespace"
2. Attendre le démarrage (2-3 minutes)
3. Lancer la plateforme :
```bash
docker-compose up -d
```

## 📦 Stack Technique

- **Backend**: FastAPI + PostgreSQL + Redis + Celery
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Scrapers**: Playwright + BeautifulSoup (5 sources)
- **Infrastructure**: Docker Compose + Nginx

## 📚 Documentation

- [README.md](./README.md) - Documentation complète
- [QUICKSTART.md](./QUICKSTART.md) - Guide démarrage rapide

## ✨ Fonctionnalités

✅ Scraping multi-sources automatisé
✅ Dashboard temps réel avec thème sombre
✅ Analyse profit & saturation marché
✅ Alertes Telegram/Email
✅ Export CSV/Excel
✅ API REST complète

## 🔗 Accès

- Frontend: http://localhost:3000
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
