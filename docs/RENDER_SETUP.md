# Render Deployment Notes

## Database Setup on Render

1. **Create PostgreSQL Database:**
   - Go to Render Dashboard → New → PostgreSQL
   - Choose a name (e.g., `umatter-db`)
   - Select free or paid tier
   - Render will automatically provide the `DATABASE_URL` environment variable

2. **The DATABASE_URL format from Render:**
   ```
   postgresql://username:password@hostname:5432/database_name
   ```

3. **SSL Connection:**
   - Render requires SSL for database connections
   - Our app automatically detects non-localhost connections and enables SSL
   - No manual configuration needed!

## Environment Variables on Render

Set these in your Render Web Service:

**Required:**
- `DATABASE_URL` - Automatically set when you link the database
- `SECRET_KEY` - Generate with: `openssl rand -hex 32`
- `FRONTEND_URL` - Your React app URL (e.g., `https://umatter.onrender.com`)

**OAuth (when ready):**
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`
- `MICROSOFT_CLIENT_ID`
- `MICROSOFT_CLIENT_SECRET`

**Optional:**
- `ENVIRONMENT=production`
- `OLLAMA_BASE_URL` - If hosting Ollama separately
- `OLLAMA_MODEL=llama3.1:8b`

## Connection Pooling

Our app is configured with sensible defaults for Render:
- Pool size: 5 connections
- Max overflow: 10 connections
- Pool pre-ping enabled (auto-reconnect)
- SSL required for production databases

These settings work well with Render's connection limits and ensure reliable database connectivity.
