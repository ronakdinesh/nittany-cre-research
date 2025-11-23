# Setup Guide - Market Analysis Demo

## Prerequisites Checklist

### 1. Python Environment
- **Python 3.12** (as specified in `runtime.txt`)
- Check your version: `python3 --version` or `python --version`

### 2. Required API Keys & Services

#### A. Parallel API Key (REQUIRED)
- Sign up at: https://platform.parallel.ai
- Navigate to API keys section
- Create a new API key
- **Cost**: Check Parallel's pricing for Deep Research API usage

#### B. Supabase Database (REQUIRED)
- Sign up at: https://supabase.com (free tier available)
- Create a new project
- Go to **Settings** → **Database**
- Copy the connection string (use "Direct connection" URL)
- **Cost**: Free tier includes 500MB database

#### C. Resend API Key (OPTIONAL - for email notifications)
- Sign up at: https://resend.com
- Create an API key
- Verify domain or use resend.dev for testing
- **Cost**: Free tier includes 3,000 emails/month

## Step-by-Step Setup

### Step 1: Install Python Dependencies

```bash
cd "/Users/ronak/Documents/Coding Projects/parallel research/parallel-cookbook/python-recipes/market-analysis-demo"
pip install -r requirements.txt
```

Or if you prefer a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or: venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### Step 2: Set Up Database

1. **Create Supabase Project** (if not done already)
   - Go to https://supabase.com
   - Create new project
   - Wait for database to be provisioned

2. **Get Database Connection String**
   - Go to **Settings** → **Database**
   - Under "Connection string", select "Direct connection"
   - Copy the connection string (format: `postgresql://postgres:[password]@[host]/postgres`)

3. **Create Database Tables**
   
   Connect to your Supabase database (via SQL Editor in Supabase dashboard) and run:

   ```sql
   -- Reports table (stores both running tasks and completed reports)
   CREATE TABLE IF NOT EXISTS reports (
       id VARCHAR PRIMARY KEY,
       task_run_id VARCHAR UNIQUE NOT NULL,
       title VARCHAR,
       slug VARCHAR UNIQUE,
       industry VARCHAR NOT NULL,
       geography VARCHAR,
       details TEXT,
       content TEXT,
       basis JSONB,
       status VARCHAR DEFAULT 'running',
       session_id VARCHAR,
       email VARCHAR,
       is_public BOOLEAN DEFAULT TRUE,
       error_message TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       completed_at TIMESTAMP
   );

   -- Rate limit table (for global rate limiting)
   CREATE TABLE IF NOT EXISTS rate_limit (
       id SERIAL PRIMARY KEY,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   -- Indexes for performance
   CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);
   CREATE INDEX IF NOT EXISTS idx_reports_slug ON reports(slug);
   CREATE INDEX IF NOT EXISTS idx_reports_task_run_id ON reports(task_run_id);
   CREATE INDEX IF NOT EXISTS idx_rate_limit_created_at ON rate_limit(created_at);
   ```

### Step 3: Create Environment Variables File

Create a file named `.env.local` in the project directory:

```bash
touch .env.local
```

Then add the following content (replace with your actual values):

```env
# Required - Parallel Deep Research API
PARALLEL_API_KEY=your_parallel_api_key_here

# Required - Flask Secret Key (generate a random string)
SECRET_KEY=your_secret_key_here_generate_random_string

# Required - Supabase Database
POSTGRES_URL_NON_POOLING=postgresql://postgres:[password]@[host]/postgres
# Replace [password] and [host] with your actual Supabase credentials

# Optional - Email Notifications via Resend
RESEND_API_KEY=your_resend_api_key_here
BASE_URL=http://localhost:5000
```

**To generate a SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Fix Import Issue

The code references `OpenAI` but doesn't import it. You can either:

**Option A**: Remove the OpenAI client code (it's not actually used)
**Option B**: Add `openai` to requirements.txt if you want to keep it

Since the code has a try/except that handles the missing import, it should work as-is, but you may see a warning.

### Step 5: Run the Application

```bash
python app.py
```

Or with explicit Python version:
```bash
python3 app.py
```

The app will start on `http://localhost:5000`

## Verification Checklist

- [ ] Python 3.12 installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env.local` file created with all required variables
- [ ] Supabase database created and tables set up
- [ ] Parallel API key is valid
- [ ] Database connection string is correct
- [ ] App starts without errors (`python app.py`)

## Common Issues & Solutions

### Issue: "PARALLEL_API_KEY not found"
**Solution**: Make sure `.env.local` exists and contains `PARALLEL_API_KEY=your_key`

### Issue: "No PostgreSQL URL found"
**Solution**: Add `POSTGRES_URL_NON_POOLING` to `.env.local` with your Supabase connection string

### Issue: Database connection errors
**Solution**: 
- Verify your Supabase project is active
- Check the connection string format
- Ensure your IP is allowed (Supabase may require IP whitelisting)

### Issue: Import errors
**Solution**: Make sure all dependencies are installed: `pip install -r requirements.txt`

### Issue: Port already in use
**Solution**: Change the port in `app.py` line 2015: `app.run(debug=True, host='0.0.0.0', port=5001)`

## Cost Estimates

- **Parallel API**: Pay-per-use for Deep Research tasks (check pricing)
- **Supabase**: Free tier (500MB database, 2GB bandwidth)
- **Resend**: Free tier (3,000 emails/month)

## Next Steps

Once running:
1. Visit `http://localhost:5000`
2. Fill out the form with an industry (e.g., "SaaS", "Electric Vehicles")
3. Click "Launch AI Research"
4. Watch real-time progress via Server-Sent Events
5. View completed reports in the public library

## Production Deployment

For production (e.g., Vercel):
- Set `DEBUG=False`
- Use production database connection
- Set proper `BASE_URL` for email links
- Configure environment variables in your hosting platform

