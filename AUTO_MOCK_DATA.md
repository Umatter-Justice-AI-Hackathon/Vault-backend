# Automatic Mock Data Generation on Render

This guide explains how mock data generation works on Render (Free Tier compatible).

## 🎯 How It Works

On Render Free Tier (no shell access), mock data is automatically generated during deployment using the startup script.

### Deployment Flow

```
Deploy to Render
    ↓
Build (pip install)
    ↓
Start (./start.sh)
    ↓
Step 1: Initialize Database (create tables)
    ↓
Step 2: Generate Mock Data (if enabled)
    ↓
Step 3: Start FastAPI Server
```

---

## 🔧 Configuration

### Method 1: Set Environment Variable (Recommended)

In **Render Dashboard → Web Service → Environment**:

```bash
AUTO_GENERATE_MOCK_DATA=true
```

**Result:** Mock data will be generated on every deployment.

### Method 2: Use Development Environment

Set:
```bash
ENVIRONMENT=development
```

**Result:** Mock data auto-generates when `ENVIRONMENT=development`.

### Method 3: Disable (Default for Production)

```bash
AUTO_GENERATE_MOCK_DATA=false
ENVIRONMENT=production
```

**Result:** Mock data is NOT generated (production default).

---

## 📋 Configuration Matrix

| ENVIRONMENT | AUTO_GENERATE_MOCK_DATA | Result |
|-------------|------------------------|--------|
| production | false (default) | ❌ No mock data |
| production | true | ✅ Generates mock data |
| development | (any) | ✅ Generates mock data |
| staging | false | ❌ No mock data |
| staging | true | ✅ Generates mock data |

---

## 🚀 Setup Instructions

### For Testing/Development Deployment

1. Go to **Render Dashboard** → Your Web Service → **Environment**

2. Add/Edit environment variable:
   ```
   AUTO_GENERATE_MOCK_DATA = true
   ```

3. Deploy (push to GitHub or manual deploy)

4. Check logs to verify:
   ```
   Step 2: Checking if mock data should be generated...
   AUTO_GENERATE_MOCK_DATA=true - Generating mock data...
   ✓ Created User 1: userid=1
   ✓ Created User 2: userid=2
   ...
   ```

### For Production Deployment

1. Keep the default settings:
   ```
   AUTO_GENERATE_MOCK_DATA = false
   ENVIRONMENT = production
   ```

2. Deploy normally

3. Mock data will NOT be generated ✅

---

## 📝 What Gets Generated

When enabled, the script automatically:

1. **Creates database tables** (if they don't exist)
2. **Clears existing mock data** (auto mode, no prompts)
3. **Generates 2 users**
4. **Generates 10 wellness records per user** (20 total)
5. **Spreads data over 2 days**
6. **Creates realistic patterns:**
   - User 1: Improving trend (5.1 → 8.5)
   - User 2: Declining trend (8.0 → 5.5)

---

## 🔍 Viewing Deployment Logs

Check if mock data was generated:

1. Go to **Render Dashboard** → Your Web Service → **Logs**

2. Look for:
   ```
   ==========================================
   Starting Umatter Backend
   Environment: production
   ==========================================

   Step 1: Initializing database...
   ✓ Database connection successful!
   ✓ Tables created successfully!

   Step 2: Checking if mock data should be generated...
   AUTO_GENERATE_MOCK_DATA=true - Generating mock data...
   ============================================================
   Generating Mock Data for Umatter Backend
   ============================================================
   ...
   ✓ Mock Data Generation Complete!

   Step 3: Starting FastAPI server...
   ==========================================
   ```

---

## 🧪 Testing After Deployment

Once deployed with mock data:

```bash
# Replace with your Render URL
API_URL=https://your-app.onrender.com/api/v1

# Get user 1 wellness history
curl $API_URL/wellness/users/1/wellness-metrics

# Get user 1 trend (should show "improving")
curl $API_URL/wellness/users/1/wellness-trend?days=7

# Get user 2 trend (should show "declining")
curl $API_URL/wellness/users/2/wellness-trend?days=7
```

---

## ⚙️ Auto Mode vs Interactive Mode

### Auto Mode (Deployment)
```bash
python generate_mock_data.py auto
```
- ✅ No prompts
- ✅ Automatically clears existing data
- ✅ Perfect for automated deployments
- ✅ Works on Render Free Tier

### Interactive Mode (Local Development)
```bash
python generate_mock_data.py
```
- ❓ Prompts before clearing data
- ✅ Safe for manual testing
- ✅ Better for local development

---

## 📂 Files Involved

| File | Purpose |
|------|---------|
| [start.sh](start.sh) | Startup script that runs on deployment |
| [generate_mock_data.py](generate_mock_data.py) | Mock data generator with auto mode |
| [init_db.py](init_db.py) | Database initialization (creates tables) |
| [render.yaml](render.yaml) | Render configuration (uses start.sh) |

---

## 🔄 How to Enable/Disable

### Enable Mock Data Generation

**Option A: In render.yaml** (recommended for version control)
```yaml
- key: AUTO_GENERATE_MOCK_DATA
  value: "true"
```

**Option B: In Render Dashboard** (overrides render.yaml)
1. Environment → Add
2. Key: `AUTO_GENERATE_MOCK_DATA`
3. Value: `true`

### Disable Mock Data Generation

**Option A: In render.yaml**
```yaml
- key: AUTO_GENERATE_MOCK_DATA
  value: "false"
```

**Option B: In Render Dashboard**
1. Delete the `AUTO_GENERATE_MOCK_DATA` variable
2. Or set it to `false`

---

## 🛡️ Production Safety

### Default Behavior (Safe)
By default, mock data is **NOT** generated in production:
- `ENVIRONMENT=production` (default)
- `AUTO_GENERATE_MOCK_DATA=false` (default)

### If You Accidentally Enable It
Mock data won't harm production, but:
- It clears existing mock data (not user data)
- Adds 2 test users with 20 wellness records
- You can delete them via API:
  ```bash
  curl -X DELETE https://your-app.onrender.com/api/v1/wellness/users/1
  curl -X DELETE https://your-app.onrender.com/api/v1/wellness/users/2
  ```

---

## 🔧 Troubleshooting

### Issue: Mock data not generating

**Check 1:** Verify environment variable
```bash
# In Render logs, look for:
Environment: production
AUTO_GENERATE_MOCK_DATA=true - Generating mock data...
```

**Check 2:** Verify start.sh is executable
```bash
# Locally:
ls -la start.sh
# Should show: -rwxr-xr-x (executable)

# If not:
chmod +x start.sh
git add start.sh
git commit -m "Make start.sh executable"
git push
```

**Check 3:** Check logs for errors
```bash
# Look for error messages in:
Render Dashboard → Logs
```

### Issue: Database connection failed

**Solution:** Verify DATABASE_URL is set correctly
- Should use **internal** URL (with `-internal`)
- Format: `postgresql://user:pass@dpg-xxxxx-internal:5432/dbname`

### Issue: Tables don't exist

**Solution:** The script creates tables automatically via `init_db.py`
- Check logs for "Step 1: Initializing database..."
- If it fails, manually run SQL from `create_tables.sql`

### Issue: Start script fails

**Solution:** Check script permissions and format
```bash
# Locally test:
bash start.sh

# Check line endings (must be Unix LF, not Windows CRLF)
dos2unix start.sh  # If on Windows
```

---

## 📊 Deployment Scenarios

### Scenario 1: First Deployment (Testing)
```yaml
ENVIRONMENT: production
AUTO_GENERATE_MOCK_DATA: true
```
**Result:** Tables created + Mock data generated ✅

### Scenario 2: Production (Real Users)
```yaml
ENVIRONMENT: production
AUTO_GENERATE_MOCK_DATA: false
```
**Result:** Tables created, no mock data ✅

### Scenario 3: Development Environment
```yaml
ENVIRONMENT: development
# AUTO_GENERATE_MOCK_DATA not needed
```
**Result:** Mock data auto-generated ✅

### Scenario 4: Staging Environment
```yaml
ENVIRONMENT: staging
AUTO_GENERATE_MOCK_DATA: true
```
**Result:** Mock data generated for testing ✅

---

## 💡 Best Practices

### ✅ Do This
- Use `AUTO_GENERATE_MOCK_DATA=true` for dev/staging
- Use `AUTO_GENERATE_MOCK_DATA=false` for production
- Check logs after deployment to verify
- Test API endpoints after deploying with mock data
- Document which environments have mock data

### ❌ Don't Do This
- Don't leave mock data in production long-term
- Don't rely on mock data for actual user testing
- Don't forget to disable before going live
- Don't mix mock data with real user data

---

## 🎯 Summary

✅ **Automatic:** Runs during deployment startup
✅ **Free Tier Compatible:** No shell access needed
✅ **Configurable:** Enable/disable via environment variable
✅ **Safe:** Disabled by default in production
✅ **Logged:** All actions visible in Render logs
✅ **No Prompts:** Auto mode works without interaction

**To enable mock data generation on Render:**
```bash
# In Render Dashboard → Environment
AUTO_GENERATE_MOCK_DATA = true
```

**Your deployment will then automatically:**
1. Create database tables
2. Generate 2 users with 10 wellness records each
3. Start the API server

**Check [MOCK_DATA_GUIDE.md](MOCK_DATA_GUIDE.md) for more details about the mock data itself.**
