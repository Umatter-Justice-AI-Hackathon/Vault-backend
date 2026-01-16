#!/bin/bash
# Startup script for Render deployment

set -e  # Exit on error

echo "=========================================="
echo "Starting Umatter Backend"
echo "Environment: $ENVIRONMENT"
echo "=========================================="

# Initialize database (create tables if they don't exist)
echo ""
echo "Step 1: Initializing database..."
python init_db.py

# Generate mock data based on environment
echo ""
echo "Step 2: Checking if mock data should be generated..."

if [ "$AUTO_GENERATE_MOCK_DATA" = "true" ]; then
    echo "AUTO_GENERATE_MOCK_DATA=true - Generating mock data..."
    python generate_mock_data.py auto
elif [ "$ENVIRONMENT" = "development" ]; then
    echo "ENVIRONMENT=development - Generating mock data..."
    python generate_mock_data.py auto
else
    echo "Skipping mock data generation"
    echo "To generate mock data, set AUTO_GENERATE_MOCK_DATA=true"
fi

# Start the server
echo ""
echo "Step 3: Starting FastAPI server..."
echo "=========================================="
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
