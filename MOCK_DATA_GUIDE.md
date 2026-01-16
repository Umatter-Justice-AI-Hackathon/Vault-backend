# Mock Data Generation Guide

This guide explains how to generate test data for your Umatter backend.

## Quick Start

```bash
# Generate mock data (2 users, 10 records each, 2 days)
python generate_mock_data.py

# Show current data
python generate_mock_data.py show

# Clear all data
python generate_mock_data.py clear
```

---

## What Gets Generated

### Users
- **2 users** are created with auto-incremented `userid`
- Each user gets 10 wellness metrics

### Wellness Metrics
- **10 records per user** (20 total)
- Spread over **2 days**
- Realistic wellness scores (0-10)
- Timestamps distributed throughout each day

### Data Patterns

**User 1: Improving Trend 📈**
- Starts at ~5.0
- Gradually improves to ~8.5
- Shows positive mental health progression

**User 2: Declining Trend 📉**
- Starts at ~8.0
- Gradually declines to ~5.5
- Shows concerning trend requiring attention

---

## Example Output

```
==============================================================
Generating Mock Data for Umatter Backend
==============================================================

==============================================================
Creating Users
==============================================================
✓ Created User 1: userid=1
✓ Created User 2: userid=2

==============================================================
Creating Wellness Metrics
==============================================================

User 1 (userid=1):
----------------------------------------
  Day 1 - Record  1: score= 5.1, time=2026-01-13 00:15
  Day 1 - Record  2: score= 5.6, time=2026-01-13 04:45
  Day 1 - Record  3: score= 6.0, time=2026-01-13 08:30
  Day 1 - Record  4: score= 6.5, time=2026-01-13 12:15
  Day 1 - Record  5: score= 6.9, time=2026-01-13 16:00
  Day 2 - Record  6: score= 7.3, time=2026-01-14 00:45
  Day 2 - Record  7: score= 7.8, time=2026-01-14 04:30
  Day 2 - Record  8: score= 8.1, time=2026-01-14 08:15
  Day 2 - Record  9: score= 8.4, time=2026-01-14 12:00
  Day 2 - Record 10: score= 8.5, time=2026-01-14 16:45

User 2 (userid=2):
----------------------------------------
  Day 1 - Record  1: score= 8.0, time=2026-01-13 00:30
  Day 1 - Record  2: score= 7.7, time=2026-01-13 04:15
  Day 1 - Record  3: score= 7.5, time=2026-01-13 08:45
  Day 1 - Record  4: score= 7.1, time=2026-01-13 12:30
  Day 1 - Record  5: score= 6.9, time=2026-01-13 16:15
  Day 2 - Record  6: score= 6.5, time=2026-01-14 00:00
  Day 2 - Record  7: score= 6.2, time=2026-01-14 04:45
  Day 2 - Record  8: score= 5.9, time=2026-01-14 08:30
  Day 2 - Record  9: score= 5.6, time=2026-01-14 12:15
  Day 2 - Record 10: score= 5.5, time=2026-01-14 16:00

==============================================================
Summary
==============================================================

Total Users Created: 2
Total Wellness Metrics: 20

Per User Breakdown:

  User 1:
    Records: 10
    Average Score: 6.92
    First Score: 5.1
    Last Score: 8.5
    Trend: 📈 Improving

  User 2:
    Records: 10
    Average Score: 6.89
    First Score: 8.0
    Last Score: 5.5
    Trend: 📉 Declining

==============================================================
✓ Mock Data Generation Complete!
==============================================================
```

---

## Testing with Generated Data

After generating mock data, test your API endpoints:

### Get User Information
```bash
# Get user 1
curl http://localhost:8000/api/v1/wellness/users/1

# Get user 2
curl http://localhost:8000/api/v1/wellness/users/2
```

### Get Wellness History
```bash
# Get all wellness metrics for user 1
curl http://localhost:8000/api/v1/wellness/users/1/wellness-metrics

# Get wellness metrics for user 2
curl http://localhost:8000/api/v1/wellness/users/2/wellness-metrics

# Get with pagination (first 5 records)
curl "http://localhost:8000/api/v1/wellness/users/1/wellness-metrics?limit=5"
```

### Get Wellness Trend Analysis
```bash
# Get 7-day trend for user 1 (should show improving)
curl http://localhost:8000/api/v1/wellness/users/1/wellness-trend?days=7

# Get 7-day trend for user 2 (should show declining)
curl http://localhost:8000/api/v1/wellness/users/2/wellness-trend?days=7
```

### Expected Trend Results

**User 1 Response:**
```json
{
  "userid": 1,
  "data_points": [...],
  "trend": "improving",
  "average_score": 6.92,
  "period_days": 7
}
```

**User 2 Response:**
```json
{
  "userid": 2,
  "data_points": [...],
  "trend": "declining",
  "average_score": 6.89,
  "period_days": 7
}
```

---

## Using the Script

### Generate Mock Data
```bash
python generate_mock_data.py
```

This will:
1. Check if data already exists
2. Prompt you to clear existing data (optional)
3. Create 2 users
4. Generate 10 wellness records per user
5. Display summary with trends

### Show Current Data
```bash
python generate_mock_data.py show
```

Displays:
- Number of users
- Wellness metrics per user
- Average scores
- Recent records

### Clear All Data
```bash
python generate_mock_data.py clear
```

⚠️ **Warning:** This will delete ALL users and wellness metrics!

### Help
```bash
python generate_mock_data.py help
```

Shows available commands.

---

## Data Generation Details

### Time Distribution
Records are spread across 2 days:
- **Day 1:** Records 1-5 (over ~16 hours)
- **Day 2:** Records 6-10 (over ~16 hours)

Each record is spaced roughly 4 hours apart with random variation (0-2 hours).

### Score Patterns

**User 1 (Improving):**
```
Day 1: 5.1 → 5.6 → 6.0 → 6.5 → 6.9
Day 2: 7.3 → 7.8 → 8.1 → 8.4 → 8.5
```
Progression: ~0.35 points per record

**User 2 (Declining):**
```
Day 1: 8.0 → 7.7 → 7.5 → 7.1 → 6.9
Day 2: 6.5 → 6.2 → 5.9 → 5.6 → 5.5
```
Regression: ~-0.25 points per record

### Random Variation
Each score includes random variation (±0.3 points) to simulate real-world data:
- Scores stay within 0-10 range
- Natural fluctuations preserved
- Trends still clearly visible

---

## Use Cases

### Development Testing
```bash
# Fresh start
python generate_mock_data.py clear
python generate_mock_data.py

# Start your server
uvicorn app.main:app --reload

# Test API
curl http://localhost:8000/api/v1/wellness/users/1/wellness-trend?days=7
```

### Frontend Development
Generate mock data once, then use the API endpoints to develop your frontend:
- Visualize improving vs. declining trends
- Test chart rendering
- Validate data display
- Test pagination

### Demo Preparation
```bash
# Generate fresh demo data
python generate_mock_data.py clear
python generate_mock_data.py

# Your API is now ready to demo with realistic data!
```

### Testing Trend Analysis
The generated data is perfect for testing your trend analysis algorithm:
- User 1: Clear improving trend
- User 2: Clear declining trend
- Both have 10+ data points for statistical relevance

---

## Production Deployment

### On Render

1. **Upload the script:**
   ```bash
   git add generate_mock_data.py
   git commit -m "Add mock data generator"
   git push
   ```

2. **Run via Render Shell:**
   ```bash
   # Open Render shell for your web service
   render shell

   # Generate mock data
   python generate_mock_data.py
   ```

3. **Or create a one-time job:**
   - Render Dashboard → Your Service → Shell
   - Run: `python generate_mock_data.py`

### Environment Variables
Make sure `DATABASE_URL` is set (script uses the same config as your main app).

---

## Customization

To modify the generated data, edit `generate_mock_data.py`:

### Change Number of Users
```python
# Line ~40: Change from 2 to desired number
for i in range(2):  # Change to range(5) for 5 users
```

### Change Number of Records
```python
# Line ~55: Change from 10 to desired number
for record_idx in range(10):  # Change to range(20) for 20 records
```

### Change Time Period
```python
# Line ~50: Change from 2 days to desired period
base_time = datetime.utcnow() - timedelta(days=2)  # Change to days=7
```

### Change Score Patterns
```python
# Lines ~64-73: Modify the score calculation logic
if user_idx == 0:
    base_score = 5.0 + (record_idx * 0.35)  # Adjust multiplier
```

---

## Troubleshooting

### Error: "No module named 'app'"
Make sure you're in the project root directory:
```bash
cd /path/to/Umatter-backend
python generate_mock_data.py
```

### Error: Database connection failed
Check your `DATABASE_URL` environment variable:
```bash
export DATABASE_URL=postgresql://localhost:5432/umatter
python generate_mock_data.py
```

### Error: Tables don't exist
Create the tables first:
```bash
python init_db.py
python generate_mock_data.py
```

### Script hangs on "Clear existing data?" prompt
Type `yes` or `no` and press Enter:
```bash
⚠️  Database already has 2 users. Clear existing data? (yes/no): yes
```

---

## Integration with Tests

You can also use this in automated tests:

```python
from generate_mock_data import generate_mock_data, clear_all_data

def test_with_mock_data():
    # Generate test data
    generate_mock_data()

    # Run your tests
    response = client.get("/api/v1/wellness/users/1/wellness-trend")
    assert response.json()["trend"] == "improving"

    # Clean up
    clear_all_data()
```

---

## Quick Reference

| Command | Action |
|---------|--------|
| `python generate_mock_data.py` | Generate 2 users with 10 records each |
| `python generate_mock_data.py show` | Display current database contents |
| `python generate_mock_data.py clear` | Delete all data |
| `python generate_mock_data.py help` | Show help message |

---

## Summary

✅ **Easy to Use:** One command generates realistic test data

✅ **Realistic Patterns:** Includes improving and declining trends

✅ **Flexible:** Clear, show, and regenerate data easily

✅ **Production Ready:** Works locally and on Render

✅ **Well Documented:** Clear output shows what was created

Start generating mock data now:
```bash
python generate_mock_data.py
```
