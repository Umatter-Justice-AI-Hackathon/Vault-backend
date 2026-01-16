# Umatter Backend - Setup Summary

## ✅ What We've Done

Your FastAPI backend is now configured to work with your existing Render PostgreSQL database!

### 1. **Updated Database Models** ✅
- Simplified to match your structure:
  - `user_table` with `userid` (primary key)
  - `wellness_metrics` with `id`, `userid`, `time`, `wellness_score`
- Models in: [app/models.py](app/models.py)

### 2. **Created API Endpoints** ✅
All endpoints for managing users and wellness metrics:

**Users:**
- `POST /api/v1/wellness/users` - Create user
- `GET /api/v1/wellness/users/{userid}` - Get user
- `GET /api/v1/wellness/users` - List users
- `DELETE /api/v1/wellness/users/{userid}` - Delete user

**Wellness Metrics:**
- `POST /api/v1/wellness/wellness-metrics` - Add wellness score
- `GET /api/v1/wellness/wellness-metrics/{id}` - Get specific metric
- `GET /api/v1/wellness/users/{userid}/wellness-metrics` - Get user's history
- `GET /api/v1/wellness/users/{userid}/wellness-trend` - Get trend analysis
- `DELETE /api/v1/wellness/wellness-metrics/{id}` - Delete metric

API code in: [app/api/wellness.py](app/api/wellness.py)

### 3. **Updated Pydantic Schemas** ✅
Request/response validation schemas matching your database:
- [app/schemas.py](app/schemas.py)

### 4. **Database Configuration** ✅
Already set up in [app/database.py](app/database.py):
- ✅ Reads `DATABASE_URL` from environment
- ✅ Automatically enables SSL for production
- ✅ Connection pooling configured
- ✅ Works with Render's internal database URL

### 5. **Created Documentation** ✅
- **[QUICK_START.md](QUICK_START.md)** - Get running in 5 minutes
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Complete deployment guide
- **[RENDER_DATABASE_SETUP.md](RENDER_DATABASE_SETUP.md)** - Database connection details
- **[create_tables.sql](create_tables.sql)** - SQL to create tables
- **[init_db.py](init_db.py)** - Python script to initialize database
- **[.env.render](.env.render)** - Example environment variables

### 6. **Created Tests** ✅
Comprehensive test suite in: [tests/test_wellness.py](tests/test_wellness.py)

---

## 🎯 Key Answer to Your Question

### **Should you use Internal or External Database URL?**

**YES! Use INTERNAL Database URL** ✅

```bash
# ✅ CORRECT - Use this!
DATABASE_URL=postgresql://user:pass@dpg-xxxxx-internal:5432/dbname
                                          ^^^^^^^^
                                          Internal!
```

**Why Internal URL is Better:**
1. **Faster** - No public internet routing
2. **Free** - No bandwidth charges for internal traffic
3. **More Secure** - Traffic stays in Render's private network
4. **Lower Latency** - Direct connection

**When to use External URL:**
- Only when connecting from outside Render
- For local development tools (pgAdmin, DBeaver, etc.)
- For debugging from your laptop

**Your code already supports both!** Just set the environment variable on Render.

---

## 🚀 Next Steps - Deploy to Render

### 1. **Get Your Internal Database URL**
- Go to Render Dashboard → Your PostgreSQL Database
- Copy the "Internal Database URL"
- Should end with `-internal`

### 2. **Create Tables**
Run this SQL in your Render PostgreSQL SQL Editor:
```sql
CREATE TABLE user_table (userid SERIAL PRIMARY KEY);

CREATE TABLE wellness_metrics (
    id SERIAL PRIMARY KEY,
    userid INTEGER NOT NULL REFERENCES user_table(userid) ON DELETE CASCADE,
    time TIMESTAMP NOT NULL DEFAULT NOW(),
    wellness_score FLOAT NOT NULL CHECK (wellness_score >= 0 AND wellness_score <= 10)
);

CREATE INDEX idx_wellness_metrics_userid ON wellness_metrics(userid);
CREATE INDEX idx_wellness_metrics_time ON wellness_metrics(time);
```

Or use the provided file: Copy contents from [create_tables.sql](create_tables.sql)

### 3. **Set Environment Variables on Render**
In your Web Service → Environment:

```bash
DATABASE_URL=<your-internal-database-url>
SECRET_KEY=<run: openssl rand -hex 32>
ENVIRONMENT=production
FRONTEND_URL=https://your-frontend.onrender.com
LLM_PROVIDER=groq
GROQ_API_KEY=<your-groq-api-key>
```

### 4. **Deploy**
- Push to GitHub
- Render auto-deploys
- Check logs for any errors

### 5. **Test Your API**
```bash
# Health check
curl https://your-app.onrender.com/health

# Create a user
curl -X POST https://your-app.onrender.com/api/v1/wellness/users

# Add wellness metric
curl -X POST https://your-app.onrender.com/api/v1/wellness/wellness-metrics \
  -H "Content-Type: application/json" \
  -d '{"userid": 1, "wellness_score": 8.5}'

# Get wellness history
curl https://your-app.onrender.com/api/v1/wellness/users/1/wellness-metrics
```

---

## 📊 Your Database Structure

```
┌─────────────┐
│ user_table  │
├─────────────┤
│ userid (PK) │──┐
└─────────────┘  │
                 │ (FK)
                 │
┌──────────────────────┐
│ wellness_metrics     │
├──────────────────────┤
│ id (PK)              │
│ userid (FK)          │◄───┘
│ time                 │
│ wellness_score (0-10)│
└──────────────────────┘
```

---

## 🧪 Features Included

### ✅ Implemented
- User management (CRUD)
- Wellness metrics (CRUD)
- Wellness history with pagination
- Wellness trend analysis
- Average score calculation
- Time-based filtering
- Cascade delete (deleting user removes their metrics)
- Input validation (wellness_score must be 0-10)
- Comprehensive tests

### 🔄 Ready to Add (when you need them)
- Authentication (OAuth)
- Chat functionality
- LLM integration for wellness scoring
- Action plan generation
- Real-time interventions

---

## 📖 Documentation Quick Links

| Document | Purpose |
|----------|---------|
| [QUICK_START.md](QUICK_START.md) | 5-minute setup guide |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | Step-by-step deployment |
| [RENDER_DATABASE_SETUP.md](RENDER_DATABASE_SETUP.md) | Database connection guide |
| [create_tables.sql](create_tables.sql) | SQL to create tables |
| [.env.render](.env.render) | Example environment variables |

---

## 🎓 Understanding the Code

### Database Connection Flow
```
app/main.py (FastAPI app)
    ↓
app/config.py (loads DATABASE_URL from environment)
    ↓
app/database.py (creates engine with SSL for production)
    ↓
app/models.py (defines UserTable and WellnessMetrics)
    ↓
app/api/wellness.py (API endpoints using models)
```

### API Request Flow
```
User Request
    ↓
FastAPI app (app/main.py)
    ↓
Router (app/api/wellness.py)
    ↓
Database Session (get_db dependency)
    ↓
SQLAlchemy Models (app/models.py)
    ↓
PostgreSQL on Render (via internal URL)
    ↓
Response (validated by Pydantic schemas)
```

---

## 🔍 Verification Commands

After deployment, verify everything works:

```bash
# Set your API URL
export API_URL=https://your-app.onrender.com/api/v1

# Test health
curl $API_URL/../health

# Create user
USER_ID=$(curl -s -X POST $API_URL/wellness/users | jq -r '.userid')
echo "Created user: $USER_ID"

# Add wellness metrics
curl -X POST $API_URL/wellness/wellness-metrics \
  -H "Content-Type: application/json" \
  -d "{\"userid\": $USER_ID, \"wellness_score\": 8.0}"

curl -X POST $API_URL/wellness/wellness-metrics \
  -H "Content-Type: application/json" \
  -d "{\"userid\": $USER_ID, \"wellness_score\": 7.5}"

curl -X POST $API_URL/wellness/wellness-metrics \
  -H "Content-Type: application/json" \
  -d "{\"userid\": $USER_ID, \"wellness_score\": 9.0}"

# Get history
curl -s $API_URL/wellness/users/$USER_ID/wellness-metrics | jq

# Get trend
curl -s $API_URL/wellness/users/$USER_ID/wellness-trend?days=30 | jq
```

---

## 💡 Pro Tips

1. **Always use internal database URL** for backend services on Render
2. **Check logs** if something doesn't work: Render Dashboard → Logs
3. **Use API docs** for testing: `https://your-app.onrender.com/api/v1/docs`
4. **Enable auto-deploy** on Render for automatic updates on git push
5. **Monitor database connections** in Render dashboard

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Use internal URL (with `-internal`) |
| "Tables don't exist" | Run `create_tables.sql` |
| "SSL error" | Code handles this automatically |
| "Validation error" | Check wellness_score is 0-10 |
| "User not found" | Create user first with POST /users |

---

## ✨ Summary

Your backend is now:
- ✅ Configured for Render deployment
- ✅ Using internal database URL (fast & free)
- ✅ Matching your existing database structure
- ✅ Ready to track wellness metrics
- ✅ Fully documented and tested

**Your FastAPI backend can now connect to your Render PostgreSQL database using the internal URL for optimal performance!** 🚀

All you need to do is:
1. Set the internal DATABASE_URL on Render
2. Create the tables (using create_tables.sql)
3. Deploy!

Enjoy building your wellness tracking app! 🎉
