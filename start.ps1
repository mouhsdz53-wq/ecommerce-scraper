# Write-Host with colors
Write-Host "🚀 Démarrage de la plateforme E-Commerce Scraper..." -ForegroundColor Cyan

# Check Docker
try {
    docker --version | Out-Null
    docker-compose --version | Out-Null
    Write-Host "✅ Docker et Docker Compose sont installés" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker ou Docker Compose n'est pas installé." -ForegroundColor Red
    Write-Host "Veuillez installer Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Create .env if not exists
if (-not (Test-Path "backend\.env")) {
    Write-Host "📝 Création du fichier .env..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "✅ Fichier .env créé. Vous pouvez le modifier pour ajouter vos clés API." -ForegroundColor Green
}

# Create necessary directories
New-Item -ItemType Directory -Force -Path "backend\exports" | Out-Null
New-Item -ItemType Directory -Force -Path "frontend\public" | Out-Null

Write-Host "🐳 Lancement des containers Docker..." -ForegroundColor Cyan
docker-compose up -d

Write-Host "⏳ Attente du démarrage des services (30 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

Write-Host ""
Write-Host "✨ Plateforme démarrée avec succès!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Accès aux services:" -ForegroundColor Cyan
Write-Host "   - Frontend Dashboard: http://localhost:3000" -ForegroundColor White
Write-Host "   - API Backend: http://localhost:8000" -ForegroundColor White
Write-Host "   - API Documentation: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "🔍 Pour voir les logs:" -ForegroundColor Cyan
Write-Host "   docker-compose logs -f" -ForegroundColor White
Write-Host ""
Write-Host "🛑 Pour arrêter:" -ForegroundColor Cyan
Write-Host "   docker-compose down" -ForegroundColor White
Write-Host ""
Write-Host "📚 Consultez QUICKSTART.md pour plus d'informations" -ForegroundColor Cyan
