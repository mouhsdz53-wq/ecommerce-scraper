#!/bin/bash

echo "🚀 Démarrage de la plateforme E-Commerce Scraper..."

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
fi

echo "✅ Docker et Docker Compose sont installés"

# Créer le fichier .env s'il n'existe pas
if [ ! -f backend/.env ]; then
    echo "📝 Création du fichier .env..."
    cp backend/.env.example backend/.env
    echo "✅ Fichier .env créé. Vous pouvez le modifier pour ajouter vos clés API."
fi

# Créer les dossiers nécessaires
mkdir -p backend/exports
mkdir -p frontend/public

echo "🐳 Lancement des containers Docker..."
docker-compose up -d

echo "⏳ Attente du démarrage des services (30 secondes)..."
sleep 30

echo ""
echo "✨ Plateforme démarrée avec succès!"
echo ""
echo "📊 Accès aux services:"
echo "   - Frontend Dashboard: http://localhost:3000"
echo "   - API Backend: http://localhost:8000"
echo "   - API Documentation: http://localhost:8000/docs"
echo ""
echo "🔍 Pour voir les logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Pour arrêter:"
echo "   docker-compose down"
echo ""
echo "📚 Consultez QUICKSTART.md pour plus d'informations"
