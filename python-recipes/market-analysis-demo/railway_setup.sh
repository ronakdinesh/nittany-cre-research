#!/bin/bash
# Railway Deployment Setup Script

echo "🚂 Railway Deployment Setup"
echo "=============================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null
then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
else
    echo "✅ Railway CLI already installed"
fi

echo ""
echo "🔐 Logging into Railway..."
railway login

echo ""
echo "🔗 Linking to your Railway project..."
echo "   (If this is a new project, create it on https://railway.app first)"
railway link

echo ""
echo "📊 Setting up database..."
railway run python3 setup_db.py

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure you've set all environment variables in Railway dashboard"
echo "2. Your app should be deploying now!"
echo "3. Check deployment status: railway status"
echo "4. View logs: railway logs"
echo ""


