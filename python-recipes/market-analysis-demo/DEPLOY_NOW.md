# 🚀 Quick Deploy Guide - Railway

## TL;DR - Deploy in 5 Minutes

### 1. Push to GitHub (2 minutes)

```bash
cd "/Users/ronak/Documents/Coding Projects/parallel research/parallel-cookbook/python-recipes/market-analysis-demo"

# If not already a git repo
git init
git add .
git commit -m "Initial commit for Railway deployment"

# Create new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Railway (3 minutes)

1. **Go to Railway**: https://railway.app
2. **Sign in** with GitHub
3. **Click "New Project"** → "Deploy from GitHub repo"
4. **Select your repository**
5. **Click "+ New"** → "Database" → "PostgreSQL"

### 3. Set Environment Variables

In Railway dashboard, click your service → "Variables" → Add these:

```
PARALLEL_API_KEY=your_key_here
RESEND_API_KEY=your_key_here
SECRET_KEY=your_secret_here
BASE_URL=https://your-app.up.railway.app
```

### 4. Setup Database

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and link
railway login
railway link

# Run database setup
railway run python3 setup_db.py
```

### 5. Done! ✨

Your app will be live at: `https://your-app-name.up.railway.app`

---

## Need More Details?

See `RAILWAY_DEPLOYMENT_GUIDE.md` for comprehensive instructions.

## Still Want Netlify?

⚠️ **Not recommended** - Netlify doesn't support:
- PostgreSQL databases
- Long-running background tasks
- Server-side sessions
- Traditional Flask apps

But if you must, you'd need to:
1. Rebuild as serverless functions
2. Host database elsewhere (Supabase, PlanetScale)
3. Host Flask backend on another platform
4. Use Netlify only for static frontend

**Bottom line**: Use Railway instead! 🚂

