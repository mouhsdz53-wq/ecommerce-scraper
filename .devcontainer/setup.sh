#!/bin/bash

echo "🚀 Setting up E-Commerce Scraper Platform..."

# Install Docker Compose
echo "📦 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating .env file..."
    cp backend/.env.example backend/.env
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Run: docker-compose up -d"
echo "   2. Wait 30 seconds for services to start"
echo "   3. Access the dashboard on port 3000"
echo ""
