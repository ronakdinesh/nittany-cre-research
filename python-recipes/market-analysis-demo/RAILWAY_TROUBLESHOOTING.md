# Railway Deployment Troubleshooting

## Error: "Error creating build plan with Railpack"

**Fix Applied:** ✅ 

I've created two files to fix this:
1. `nixpacks.toml` - Tells Railway exactly how to build your app
2. `runtime.txt` - Specifies Python version

**Next Steps:**

```bash
cd "/Users/ronak/Documents/Coding Projects/parallel research/parallel-cookbook/python-recipes/market-analysis-demo"

# Commit the fixes
git add nixpacks.toml runtime.txt
git commit -m "Fix Railway build configuration"
git push origin main
```

Railway will automatically redeploy with the fixed configuration!

---

## Common Railway Errors & Fixes

### 1. Build Failed - Missing Dependencies

**Error:** `ModuleNotFoundError` or missing package

**Fix:** Add missing package to `requirements.txt`:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### 2. Database Connection Failed

**Error:** `could not connect to server` or database timeout

**Fix:**
1. Verify PostgreSQL service is running in Railway
2. Check environment variables are set:
   - Railway should auto-set `DATABASE_URL`
   - Check in Railway dashboard → Variables
3. Make sure database schema is set up:
   ```bash
   railway run python3 setup_db.py
   ```

### 3. Port Binding Error

**Error:** `Failed to bind to $PORT`

**Fix:** Already handled! Your app uses:
```python
port = int(os.getenv('PORT', 5001))
```

### 4. Gunicorn Not Found

**Error:** `gunicorn: command not found`

**Fix:** Already added to `requirements.txt`! 
If you see this, verify:
```bash
grep gunicorn requirements.txt
```

### 5. App Crashes Immediately

**Error:** App starts then crashes

**Debugging Steps:**
1. Check Railway logs:
   - Click "View Logs" in Railway dashboard
   - Look for Python errors
2. Check environment variables:
   - All required vars set?
   - `PARALLEL_API_KEY`, `SECRET_KEY`, etc.
3. Test locally:
   ```bash
   python3 app.py
   ```

### 6. 502 Bad Gateway

**Error:** Site shows 502 error

**Fix:**
1. App might still be starting (wait 30 seconds)
2. Check if app is listening on correct port
3. View logs for startup errors

### 7. Static Files Not Loading

**Error:** CSS/JS files return 404

**Fix:** Already configured! Flask serves from `/static/`
If issues persist, check:
```python
app = Flask(__name__)  # Should auto-detect static folder
```

---

## Railway CLI Commands

### View Logs
```bash
railway logs
```

### Check Status
```bash
railway status
```

### Run Commands on Railway
```bash
railway run python3 setup_db.py
```

### Connect to Database
```bash
railway connect postgres
```

### Restart Service
```bash
railway restart
```

---

## Verify Your Setup

### ✅ Required Files Checklist

- [x] `app.py` - Main Flask application
- [x] `requirements.txt` - Python dependencies (with gunicorn)
- [x] `runtime.txt` - Python version specification
- [x] `nixpacks.toml` - Railway build configuration
- [x] `Procfile` - Alternative start command
- [x] `setup_database.sql` - Database schema
- [x] `.gitignore` - Exclude sensitive files

### ✅ Required Environment Variables

In Railway Dashboard → Variables tab:

```
PARALLEL_API_KEY=your_key
RESEND_API_KEY=your_key
SECRET_KEY=your_secret
BASE_URL=https://your-app.up.railway.app
```

Railway auto-sets:
- `PORT`
- `DATABASE_URL`
- `POSTGRES_URL`
- `POSTGRES_URL_NON_POOLING`

---

## Still Having Issues?

### Option 1: Check Railway Logs
1. Railway Dashboard → Your Service
2. Click "View Logs"
3. Look for specific error messages

### Option 2: Railway Support
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app
- Help Center: https://help.railway.app

### Option 3: Try Alternative Platform

If Railway continues to have issues, consider:
- **Render.com** - Very similar to Railway
- **Fly.io** - More control, Docker-based
- See `HOSTING_OPTIONS.md` for details

---

## Quick Redeploy

If you want to force a fresh deployment:

```bash
# Make a trivial change
echo "" >> runtime.txt

# Commit and push
git add runtime.txt
git commit -m "Trigger redeploy"
git push origin main
```

---

## Success Indicators

Your deployment is successful when:
1. ✅ Railway shows "Deployed" status (green)
2. ✅ Logs show: "Listening at: http://0.0.0.0:PORT"
3. ✅ Your URL loads without errors
4. ✅ Can log in and generate reports

---

## Getting Help

If you're still stuck:

1. **Copy the error from Railway logs**
2. **Check this troubleshooting guide**
3. **Search Railway Discord** - Someone probably had the same issue
4. **Open a GitHub issue** in your repo with:
   - Full error message
   - Railway logs
   - What you've tried

Good luck! 🚀


