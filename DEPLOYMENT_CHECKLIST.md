# Render Deployment Checklist

Complete guide to deploy your Umatter Backend to Render with PostgreSQL.

---

## ✅ Pre-Deployment Checklist

### 1. Code Ready
- [x] Database models match your structure (`user_table`, `wellness_metrics`)
- [x] API endpoints implemented
- [x] Environment configuration set up
- [x] Tests written

### 2. Render Account
- [ ] Create a Render account at https://render.com
- [ ] Connect your GitHub repository
- [ ] Create PostgreSQL database
- [ ] Create Web Service

---

## 🗄️ Step 1: Create PostgreSQL Database on Render

1. **Go to Render Dashboard** → Click "New +" → "PostgreSQL"

2. **Configure Database:**
   - **Name:** `umatter-db`
   - **Database:** `umatter`
   - **User:** (auto-generated)
   - **Region:** Choose closest to your users
   - **Plan:** Free tier for testing

3. **Create Database** → Wait for provisioning (~2 minutes)

4. **Get Connection Strings:**
   - Go to your database dashboard
   - Copy **Internal Database URL** (ends with `-internal`)
   - Format: `postgresql://user:pass@dpg-xxxxx-internal:5432/dbname`

5. **Create Tables:**
   - Click "SQL Editor" in database dashboard
   - Copy contents from `create_tables.sql`
   - Paste and execute
   - Verify tables exist:
     ```sql
     \dt
     ```

---

## 🚀 Step 2: Create Web Service on Render

1. **Go to Render Dashboard** → Click "New +" → "Web Service"

2. **Connect Repository:**
   - Select your GitHub repository
   - Grant Render access if needed

3. **Configure Service:**
   - **Name:** `umatter-backend`
   - **Region:** Same as your database
   - **Branch:** `main`
   - **Root Directory:** (leave empty)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Choose Plan:**
   - Free tier for testing
   - Starter for production

---

## ⚙️ Step 3: Configure Environment Variables

In your Web Service → Environment tab, add these variables:

### Required Variables

```bash
# DATABASE (USE INTERNAL URL!)
DATABASE_URL=postgresql://user:pass@dpg-xxxxx-internal:5432/umatter_db

# SECURITY
SECRET_KEY=<run: openssl rand -hex 32>

# APPLICATION
ENVIRONMENT=production
FRONTEND_URL=https://your-frontend.onrender.com
```

### LLM Provider (Choose One)

**Option 1: Groq (Recommended - FREE & FAST)**
```bash
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.1-70b-versatile
```

Get API key: https://console.groq.com/keys

**Option 2: Hugging Face (FREE)**
```bash
LLM_PROVIDER=huggingface
HUGGINGFACE_API_KEY=your-hf-token
HUGGINGFACE_MODEL=meta-llama/Llama-3.1-70B-Instruct
```

Get token: https://huggingface.co/settings/tokens

**Option 3: OpenAI (Paid)**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4o-mini
```

**Option 4: Anthropic (Paid)**
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-anthropic-key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

---

## 🔧 Step 4: Deploy

1. **Save Environment Variables**
2. **Click "Manual Deploy"** → Deploy Latest Commit
3. **Wait for Build** (~2-3 minutes)
4. **Check Logs** for any errors

---

## ✨ Step 5: Initialize Database

### Option 1: Using Python Script (Recommended)

```bash
# In Render Shell
render shell
python init_db.py
```

### Option 2: Using SQL Editor

Already done in Step 1! If you skipped it, run `create_tables.sql` now.

---

## 🧪 Step 6: Test Your Deployment

### 1. Check Health Endpoint

```bash
curl https://your-app.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "ollama": "connected"
  }
}
```

### 2. Test API Documentation

Visit: `https://your-app.onrender.com/api/v1/docs`

### 3. Test Creating a User

```bash
curl -X POST https://your-app.onrender.com/api/v1/wellness/users
```

Expected response:
```json
{
  "userid": 1
}
```

### 4. Test Adding Wellness Metric

```bash
curl -X POST https://your-app.onrender.com/api/v1/wellness/wellness-metrics \
  -H "Content-Type: application/json" \
  -d '{
    "userid": 1,
    "wellness_score": 7.5
  }'
```

### 5. Test Getting Wellness History

```bash
curl https://your-app.onrender.com/api/v1/wellness/users/1/wellness-metrics
```

---

## 📊 Available API Endpoints

Once deployed, you'll have these endpoints:

### Core Endpoints
- `GET /` - Health check
- `GET /health` - Detailed health status
- `GET /api/v1/docs` - Interactive API docs (Swagger UI)
- `GET /api/v1/redoc` - Alternative docs (ReDoc)

### User Endpoints
- `POST /api/v1/wellness/users` - Create user
- `GET /api/v1/wellness/users/{userid}` - Get user
- `GET /api/v1/wellness/users` - List users
- `DELETE /api/v1/wellness/users/{userid}` - Delete user

### Wellness Metrics Endpoints
- `POST /api/v1/wellness/wellness-metrics` - Add wellness score
- `GET /api/v1/wellness/wellness-metrics/{id}` - Get metric
- `GET /api/v1/wellness/users/{userid}/wellness-metrics` - Get history
- `GET /api/v1/wellness/users/{userid}/wellness-trend` - Get trend
- `DELETE /api/v1/wellness/wellness-metrics/{id}` - Delete metric

---

## 🔍 Troubleshooting

### Issue: "Connection refused"
**Cause:** Using external URL instead of internal
**Solution:** Update `DATABASE_URL` to use `-internal` suffix

### Issue: "relation does not exist"
**Cause:** Tables not created
**Solution:** Run `create_tables.sql` or `init_db.py`

### Issue: "SSL required"
**Cause:** Database requires SSL (already handled!)
**Solution:** Code automatically enables SSL for production

### Issue: "Environment variable not found"
**Cause:** Missing environment variable
**Solution:** Check all required variables in Step 3

### Issue: Slow response times
**Cause:** Using external database URL
**Solution:** Switch to internal URL (faster)

### Issue: "Database connection pool exhausted"
**Cause:** Too many concurrent requests
**Solution:** Increase `DATABASE_POOL_SIZE` environment variable

---

## 🎯 Performance Optimization

### Already Configured ✅
- Connection pooling enabled
- Internal database URL for speed
- SSL for security
- Indexes on frequently queried columns

### Optional Improvements
1. **Add caching** for frequently accessed data
2. **Increase pool size** if handling many concurrent users:
   ```bash
   DATABASE_POOL_SIZE=10
   DATABASE_MAX_OVERFLOW=20
   ```
3. **Enable compression** for API responses
4. **Add CDN** for static assets (if any)

---

## 🔒 Security Checklist

- [ ] Using internal database URL
- [ ] SSL enabled for database (automatic)
- [ ] Strong secret key (32+ characters)
- [ ] No credentials in code
- [ ] CORS configured for your frontend only
- [ ] Environment variables set in Render (not in `.env` file)
- [ ] Database backups enabled (Render dashboard)

---

## 📈 Monitoring

### Render Dashboard
- **Logs:** Web Service → Logs tab
- **Metrics:** View CPU, memory, request count
- **Database:** View connection count, disk usage

### Key Metrics to Watch
- Response time
- Error rate
- Database connection count
- Memory usage

---

## 🔄 Updating Your Deployment

### Automatic Deployments
Render automatically deploys when you push to your main branch.

### Manual Deployment
1. Go to Web Service dashboard
2. Click "Manual Deploy"
3. Select branch
4. Click "Deploy"

### Database Migrations
For schema changes:
1. Update models in `app/models.py`
2. Run migration SQL in database SQL Editor
3. Deploy new code

---

## 💾 Database Backups

### Automatic Backups (Paid Plans)
Render automatically backs up paid databases.

### Manual Backup
```bash
# From Render shell
pg_dump $DATABASE_URL > backup.sql
```

### Restore from Backup
```bash
psql $DATABASE_URL < backup.sql
```

---

## 🎓 Additional Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
- [PostgreSQL Documentation](https://www.postgresql.org/docs)

---

## 📞 Support

If you encounter issues:
1. Check Render logs first
2. Review this checklist
3. Check `RENDER_DATABASE_SETUP.md` for detailed database info
4. Visit Render community: https://community.render.com

---

## ✅ Final Verification

- [ ] Database created on Render
- [ ] Tables created (user_table, wellness_metrics)
- [ ] Web service created and deployed
- [ ] Environment variables configured (using INTERNAL database URL)
- [ ] Health endpoint responding
- [ ] API docs accessible
- [ ] Can create users
- [ ] Can add wellness metrics
- [ ] Can retrieve wellness history

---

**Your API is now live! 🎉**

API Base URL: `https://your-app.onrender.com/api/v1`
API Docs: `https://your-app.onrender.com/api/v1/docs`
