# Quick Start Guide

Get your Umatter backend running in 5 minutes!

## 🎯 TL;DR - For Render Deployment

### 1. Database URL
```bash
# ✅ USE THIS (Internal - Fast & Free)
DATABASE_URL=postgresql://user:pass@dpg-xxxxx-internal:5432/dbname
                                          ^^^^^^^^
# ❌ NOT THIS (External - Slower)
DATABASE_URL=postgresql://user:pass@dpg-xxxxx.region.render.com:5432/dbname
```

### 2. Environment Variables (Render Dashboard)
```bash
DATABASE_URL=<your-internal-url-from-render>
SECRET_KEY=<run: openssl rand -hex 32>
ENVIRONMENT=production
FRONTEND_URL=https://your-frontend.onrender.com
LLM_PROVIDER=groq
GROQ_API_KEY=<get-from-console.groq.com>
```

### 3. Create Tables
In Render PostgreSQL SQL Editor:
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

### 4. Deploy
Push to GitHub → Render auto-deploys → Done! 🚀

---

## 📝 Database Structure

### Tables
```
user_table
  └─ userid (PK, auto-increment)

wellness_metrics
  ├─ id (PK, auto-increment)
  ├─ userid (FK → user_table.userid)
  ├─ time (timestamp, default now)
  └─ wellness_score (float, 0-10)
```

---

## 🔌 API Endpoints

Base URL: `https://your-app.onrender.com/api/v1`

### Quick Examples

```bash
# Create user
curl -X POST $BASE_URL/wellness/users
# → {"userid": 1}

# Add wellness score
curl -X POST $BASE_URL/wellness/wellness-metrics \
  -H "Content-Type: application/json" \
  -d '{"userid": 1, "wellness_score": 7.5}'

# Get user's wellness history
curl $BASE_URL/wellness/users/1/wellness-metrics

# Get wellness trend (last 30 days)
curl $BASE_URL/wellness/users/1/wellness-trend?days=30
```

### Full API Docs
Visit: `https://your-app.onrender.com/api/v1/docs`

---

## 🧪 Local Development

### Option 1: Docker (Recommended)
```bash
# Start PostgreSQL
docker-compose up -d db

# Set environment
export DATABASE_URL=postgresql://umatter:umatter_dev_password@localhost:5432/umatter

# Install dependencies
pip install -r requirements.txt

# Create tables
python init_db.py

# Run server
uvicorn app.main:app --reload
```

### Option 2: Local PostgreSQL
```bash
# Install PostgreSQL locally
# Create database
createdb umatter

# Set environment
export DATABASE_URL=postgresql://localhost:5432/umatter

# Install & run
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload
```

---

## ✅ Verification

```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/api/v1/docs
```

---

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| Connection refused | Use internal database URL (with `-internal`) |
| Tables don't exist | Run `create_tables.sql` in SQL Editor |
| SSL error | Already handled automatically! |
| Slow queries | Make sure using internal URL, not external |

---

## 📚 More Info

- **Detailed Setup:** `DEPLOYMENT_CHECKLIST.md`
- **Database Guide:** `RENDER_DATABASE_SETUP.md`
- **API Reference:** Visit `/api/v1/docs` when running

---

## 🎉 That's It!

Your API is ready to accept wellness scores and track user wellbeing trends!
