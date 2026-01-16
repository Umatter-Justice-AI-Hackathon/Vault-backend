# Render Database Setup Guide

This guide explains how to connect your FastAPI backend to PostgreSQL on Render using the **internal database URL** for optimal performance.

## Why Use Internal Database URL?

When both your backend and database are hosted on Render:

✅ **Use Internal URL** (Recommended)
- Faster connection (no public internet routing)
- No bandwidth charges for internal traffic
- Better security (traffic stays in Render's private network)
- Lower latency

❌ **Avoid External URL** (Only for external connections)
- Slower (goes through public internet)
- May incur bandwidth charges
- Only needed when connecting from outside Render

---

## Step 1: Get Your Database URLs from Render

1. Go to your Render Dashboard
2. Navigate to your PostgreSQL database
3. Look for these connection strings:

```bash
# External Database URL (for external clients only)
postgresql://user:pass@dpg-xxxxx.region.render.com:5432/dbname

# Internal Database URL (USE THIS for your backend!)
postgresql://user:pass@dpg-xxxxx-internal:5432/dbname
```

Notice the `-internal` suffix? That's the key!

---

## Step 2: Configure Environment Variables on Render

In your Render Web Service settings:

### Go to: Dashboard → Your Web Service → Environment

Add these variables:

```bash
# DATABASE - Use Internal URL!
DATABASE_URL=postgresql://user:pass@dpg-xxxxx-internal:5432/dbname

# SECURITY
SECRET_KEY=your-secret-key-here

# APPLICATION
ENVIRONMENT=production
FRONTEND_URL=https://your-frontend.onrender.com

# LLM PROVIDER (recommended: Groq - free and fast)
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-api-key
```

### Generate a Secret Key

```bash
# Run locally and copy the output
openssl rand -hex 32
```

---

## Step 3: Verify Your Database Connection

The FastAPI backend is already configured to:

1. ✅ Use `DATABASE_URL` environment variable
2. ✅ Enable SSL for production (non-localhost) connections
3. ✅ Use connection pooling for better performance

Check the configuration in `app/database.py`:

```python
# Automatically adds SSL for production databases
connect_args = {}
if settings.database_url.startswith("postgresql://") and "localhost" not in settings.database_url:
    connect_args = {"sslmode": "require"}
```

---

## Step 4: Database Structure

Your database should have these tables:

### `user_table`
```sql
CREATE TABLE user_table (
    userid SERIAL PRIMARY KEY
);
```

### `wellness_metrics`
```sql
CREATE TABLE wellness_metrics (
    id SERIAL PRIMARY KEY,
    userid INTEGER NOT NULL REFERENCES user_table(userid) ON DELETE CASCADE,
    time TIMESTAMP NOT NULL DEFAULT NOW(),
    wellness_score FLOAT NOT NULL CHECK (wellness_score >= 0 AND wellness_score <= 10)
);

CREATE INDEX idx_wellness_metrics_userid ON wellness_metrics(userid);
CREATE INDEX idx_wellness_metrics_time ON wellness_metrics(time);
```

### Create Tables via SQL Editor

1. Go to your Render PostgreSQL dashboard
2. Click "SQL Editor" or "Connect" → "PSQL"
3. Paste and run the SQL commands above

---

## Step 5: Test Your Connection

### Option 1: Check Health Endpoint

After deploying, visit:
```
https://your-app.onrender.com/health
```

### Option 2: Test API Endpoints

```bash
# Create a user
curl -X POST https://your-app.onrender.com/api/v1/wellness/users

# Response: {"userid": 1}

# Add wellness metric
curl -X POST https://your-app.onrender.com/api/v1/wellness/wellness-metrics \
  -H "Content-Type: application/json" \
  -d '{"userid": 1, "wellness_score": 7.5}'

# Get user's wellness history
curl https://your-app.onrender.com/api/v1/wellness/users/1/wellness-metrics
```

---

## Available API Endpoints

Once deployed, your API will have these endpoints:

### Users
- `POST /api/v1/wellness/users` - Create a new user
- `GET /api/v1/wellness/users/{userid}` - Get user by ID
- `GET /api/v1/wellness/users` - List all users
- `DELETE /api/v1/wellness/users/{userid}` - Delete user

### Wellness Metrics
- `POST /api/v1/wellness/wellness-metrics` - Add wellness score
- `GET /api/v1/wellness/wellness-metrics/{id}` - Get metric by ID
- `GET /api/v1/wellness/users/{userid}/wellness-metrics` - Get user's history
- `GET /api/v1/wellness/users/{userid}/wellness-trend` - Get trend analysis
- `DELETE /api/v1/wellness/wellness-metrics/{id}` - Delete metric

### Documentation
- `/api/v1/docs` - Interactive API documentation (Swagger UI)
- `/api/v1/redoc` - Alternative documentation (ReDoc)

---

## Common Issues & Solutions

### Issue: "Connection refused"
**Solution:** Make sure you're using the **internal** database URL, not external.

### Issue: "SSL required"
**Solution:** The code already handles this! SSL is automatically enabled for production databases.

### Issue: "Database does not exist"
**Solution:** Make sure the database name in your connection string matches the actual database name in Render.

### Issue: "Password authentication failed"
**Solution:** Copy the exact connection string from Render - don't manually type credentials.

### Issue: "Tables don't exist"
**Solution:** Run the SQL commands in Step 4 to create the tables.

---

## Local Development

For local development, use Docker Compose:

```bash
# Start PostgreSQL locally
docker-compose up -d db

# Set local environment variable
export DATABASE_URL=postgresql://umatter:umatter_dev_password@localhost:5432/umatter

# Run the app
uvicorn app.main:app --reload
```

---

## Database Migration (If Needed)

If you have existing tables with different names and want to migrate:

### Option 1: Rename Existing Tables
```sql
ALTER TABLE your_old_user_table RENAME TO user_table;
ALTER TABLE your_old_metrics_table RENAME TO wellness_metrics;

-- Update column names if needed
ALTER TABLE user_table RENAME COLUMN old_column TO userid;
```

### Option 2: Keep Your Models Synced
The SQLAlchemy models in `app/models.py` are already configured to match your structure:
- `user_table` with `userid`
- `wellness_metrics` with `id`, `userid`, `time`, `wellness_score`

---

## Monitoring

### Check Database Connections

In Render Dashboard → Database:
- Monitor active connections
- Check connection pool usage
- View query performance

### Application Logs

In Render Dashboard → Web Service → Logs:
- Look for SQLAlchemy connection logs
- Check for any database errors

---

## Performance Tips

1. ✅ Use connection pooling (already configured)
2. ✅ Use internal database URL (fastest)
3. ✅ Add indexes on frequently queried columns (already done)
4. ✅ Use prepared statements (SQLAlchemy does this automatically)
5. ⚠️ Consider adding more indexes if you have custom queries

---

## Security Checklist

- [ ] Using internal database URL
- [ ] SSL enabled for database connection
- [ ] Strong secret key set (32+ characters)
- [ ] Database credentials in environment variables (not in code)
- [ ] CORS properly configured for your frontend
- [ ] API prefix configured (`/api/v1`)

---

## Need Help?

- **API Documentation**: Visit `https://your-app.onrender.com/api/v1/docs`
- **Render Docs**: https://render.com/docs/databases
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

## Quick Reference

```bash
# Your Internal Database URL format
postgresql://username:password@dpg-xxxxx-internal:5432/dbname
                                          ^^^^^^^^
                                          Important!

# Test connection from Render shell
render shell
python -c "from app.database import engine; print('Connected!' if engine.connect() else 'Failed')"
```

---

**Remember:** Always use the **internal** database URL when your backend and database are both on Render! 🚀
