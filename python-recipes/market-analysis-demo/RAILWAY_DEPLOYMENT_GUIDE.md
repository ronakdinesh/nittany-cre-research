# Railway Deployment Guide for Market Analysis Demo

This guide will help you deploy your Flask Market Research application to Railway.

## Why Railway?

Railway is perfect for your app because:
- ✅ Automatically detects Flask applications
- ✅ Built-in PostgreSQL support
- ✅ Supports long-running background tasks
- ✅ Easy environment variable management
- ✅ Automatic HTTPS and custom domains
- ✅ Free tier available ($5/month credit)

## Prerequisites

1. A GitHub account (to connect your repository)
2. A Railway account (sign up at https://railway.app)
3. Your environment variables from `.env.local`

## Step-by-Step Deployment

### 1. Prepare Your Repository

First, make sure your code is in a Git repository:

```bash
cd "/Users/ronak/Documents/Coding Projects/parallel research/parallel-cookbook/python-recipes/market-analysis-demo"

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Railway deployment"
```

### 2. Push to GitHub

Create a new repository on GitHub (https://github.com/new), then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 3. Deploy on Railway

1. **Go to Railway**: Visit https://railway.app and sign in with GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository

3. **Add PostgreSQL Database**:
   - In your project dashboard, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically provision a database

4. **Configure Environment Variables**:
   - Click on your Flask service
   - Go to "Variables" tab
   - Add these variables (get values from your `.env.local`):

   ```
   PARALLEL_API_KEY=your_parallel_api_key
   RESEND_API_KEY=your_resend_api_key
   SECRET_KEY=your_secret_key
   BASE_URL=https://your-app-name.up.railway.app
   ```

   Railway automatically provides these database variables:
   - `DATABASE_URL` (Railway sets this automatically)
   - `POSTGRES_URL` (Railway sets this automatically)
   - `POSTGRES_URL_NON_POOLING` (Railway sets this automatically)

5. **Set Port Variable**:
   Add this variable:
   ```
   PORT=5001
   ```

### 4. Database Setup

After your app deploys, you need to set up the database schema:

1. **Connect to Railway PostgreSQL**:
   - In Railway, click on your PostgreSQL service
   - Click "Connect" and copy the connection command
   
2. **Run the setup script**:
   ```bash
   # Install psql if you don't have it (Mac)
   brew install postgresql
   
   # Connect using the Railway connection string
   psql postgresql://user:pass@host:port/dbname
   
   # Then run your SQL schema
   \i setup_database.sql
   ```

   OR use the Railway CLI:
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli
   
   # Login
   railway login
   
   # Link to your project
   railway link
   
   # Run database setup
   railway run python3 setup_db.py
   ```

### 5. Update App Configuration for Production

Your app is already configured to work with Railway! The code automatically:
- Uses `PORT` environment variable (Railway provides this)
- Connects to PostgreSQL using Railway's environment variables
- Handles production settings

### 6. Monitor Deployment

1. In Railway dashboard, click on your service
2. Go to "Deployments" tab to see build logs
3. Once deployed, click "View Logs" to monitor your app

### 7. Access Your App

Once deployed:
- Railway will provide a URL like: `https://your-app-name.up.railway.app`
- Update your `BASE_URL` environment variable with this URL
- Test by visiting the URL in your browser

## Troubleshooting

### Build Fails
- Check "Deployments" → "View Logs" for errors
- Ensure all dependencies are in `requirements.txt`
- Verify `gunicorn` is listed in requirements.txt

### Database Connection Issues
- Verify PostgreSQL service is running in Railway
- Check that environment variables are set correctly
- Ensure database schema is set up (run `setup_db.py`)

### App Crashes on Start
- Check "View Logs" for Python errors
- Verify all environment variables are set
- Check that `PORT` is correctly configured

## Cost Estimate

Railway pricing:
- **Free tier**: $5/month credit (sufficient for testing)
- **Pro plan**: $20/month for unlimited projects
- Resource usage: ~$5-10/month for this app size

## Custom Domain (Optional)

To use your own domain:
1. Go to your service settings in Railway
2. Click "Settings" → "Domains"
3. Click "Add Domain"
4. Follow instructions to configure DNS

## Environment Variables Reference

Required variables for your `.env.local` (copy to Railway):

```env
# Parallel AI API
PARALLEL_API_KEY=your_parallel_api_key_here

# Email (Resend API)
RESEND_API_KEY=your_resend_api_key_here

# Flask Secret
SECRET_KEY=your_secret_key_here

# Base URL (update after deployment)
BASE_URL=https://your-app-name.up.railway.app
```

Railway automatically provides:
- `DATABASE_URL`
- `POSTGRES_URL`
- `POSTGRES_URL_NON_POOLING`
- `PORT`

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Create issues in your repository

## Alternative: Quick Deploy Button (Future)

You can create a one-click deploy button for future deployments:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

---

**Need Help?** Check Railway's documentation or their Discord community for support.


