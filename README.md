<div align="center">
  <img src="images/Logo.png" alt="vault Logo" width="200"/>
</div>


A FastAPI backend for tracking user wellness metrics over time. Built for deployment on Render with PostgreSQL.

## Quick Start

```bash
# Create a user
curl -X POST https://your-app.onrender.com/api/v1/wellness/users

# Add wellness score
curl -X POST https://your-app.onrender.com/api/v1/wellness/wellness-metrics \
  -H "Content-Type: application/json" \
  -d '{"userid": 1, "wellness_score": 8.5}'

# Get wellness history
curl https://your-app.onrender.com/api/v1/wellness/users/1/wellness-metrics
```

📖 **[5-Minute Setup Guide →](QUICK_START.md)**

## Database Structure

```
user_table
  └─ userid (primary key)

wellness_metrics
  ├─ id (primary key)
  ├─ userid (foreign key)
  ├─ time (timestamp)
  └─ wellness_score (0-10)
```

## API Endpoints

- `POST /api/v1/wellness/users` - Create user
- `POST /api/v1/wellness/wellness-metrics` - Add wellness score
- `GET /api/v1/wellness/users/{userid}/wellness-metrics` - Get wellness history
- `GET /api/v1/wellness/users/{userid}/wellness-trend` - Get trend analysis

**Full API Docs:** Visit `/api/v1/docs` when running

## Render Deployment

### Important: Use Internal Database URL

✅ **Correct:**
```bash
DATABASE_URL=postgresql://user:pass@dpg-xxxxx-internal:5432/dbname
```

❌ **Incorrect:**
```bash
DATABASE_URL=postgresql://user:pass@dpg-xxxxx.region.render.com:5432/dbname
```

**Why?** Internal URL is faster, free, and more secure when both services are on Render.

### Environment Variables

Set these in Render Dashboard → Web Service → Environment:

```bash
DATABASE_URL=<internal-database-url>
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ENVIRONMENT=production
FRONTEND_URL=https://your-frontend.onrender.com
LLM_PROVIDER=groq
GROQ_API_KEY=<your-groq-api-key>

# Optional: Auto-generate mock data on deploy (for testing)
AUTO_GENERATE_MOCK_DATA=true
```

**Note:** On deployment, tables are created automatically and mock data is generated if `AUTO_GENERATE_MOCK_DATA=true` 🚀

📖 **[Auto Mock Data Guide →](AUTO_MOCK_DATA.md)**

### Create Tables

Run this SQL in Render PostgreSQL SQL Editor:

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

Or use: `create_tables.sql`

## Documentation

| Document | Description |
|----------|-------------|
| [QUICK_START.md](QUICK_START.md) | Get running in 5 minutes |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | Complete deployment guide |
| [RENDER_DATABASE_SETUP.md](RENDER_DATABASE_SETUP.md) | Database connection details |
| [AUTO_MOCK_DATA.md](AUTO_MOCK_DATA.md) | Auto mock data on Render (Free Tier) |
| [MOCK_DATA_GUIDE.md](MOCK_DATA_GUIDE.md) | Generate test data manually |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture diagrams |
| [SUMMARY.md](SUMMARY.md) | What we built and why |

## Local Development

```bash
# Start PostgreSQL
docker-compose up -d db

# Install dependencies
pip install -r requirements.txt

# Create tables
python init_db.py

# Generate mock data (optional - 2 users, 10 records each)
python generate_mock_data.py

# Run server
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/api/v1/docs

## Testing with Mock Data

Generate realistic test data instantly:

```bash
# Generate 2 users with 10 wellness records each (2 days)
python generate_mock_data.py

# Show current data
python generate_mock_data.py show

# Clear all data
python generate_mock_data.py clear
```

📖 **[Mock Data Guide →](MOCK_DATA_GUIDE.md)**

## Tech Stack

- **Framework:** FastAPI 0.115.0
- **Database:** PostgreSQL with SQLAlchemy 2.0
- **Validation:** Pydantic 2.10
- **Deployment:** Render.com
- **LLM Support:** Groq, OpenAI, Anthropic, Hugging Face
