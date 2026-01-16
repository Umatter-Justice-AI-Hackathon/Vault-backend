#!/usr/bin/env python3
"""
Database initialization script.

This script creates all tables defined in the SQLAlchemy models.
Run this after deploying to Render or starting local development.

Usage:
    python init_db.py
"""

import sys
from sqlalchemy import inspect

from app.database import engine, Base
from app.models import UserTable, WellnessMetrics


def check_tables_exist():
    """Check if tables already exist."""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    return existing_tables


def create_tables():
    """Create all tables defined in the models."""
    try:
        # Check existing tables
        existing_tables = check_tables_exist()

        if existing_tables:
            print("Existing tables found:")
            for table in existing_tables:
                print(f"  - {table}")

            response = input("\nDo you want to recreate tables? This will DROP all existing data! (yes/no): ")
            if response.lower() == 'yes':
                print("\nDropping all tables...")
                Base.metadata.drop_all(bind=engine)
                print("✓ All tables dropped")

        print("\nCreating tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created successfully!")

        # Verify tables were created
        tables = check_tables_exist()
        print(f"\nCurrent tables in database:")
        for table in tables:
            print(f"  - {table}")

        print("\n✓ Database initialization complete!")
        return True

    except Exception as e:
        print(f"\n✗ Error creating tables: {e}", file=sys.stderr)
        return False


def verify_connection():
    """Verify database connection."""
    try:
        with engine.connect() as connection:
            print("✓ Database connection successful!")
            print(f"  Database URL: {engine.url.render_as_string(hide_password=True)}")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}", file=sys.stderr)
        return False


def main():
    """Main function."""
    print("=" * 60)
    print("Umatter Backend - Database Initialization")
    print("=" * 60)
    print()

    # Verify connection first
    print("Step 1: Verifying database connection...")
    if not verify_connection():
        print("\nPlease check your DATABASE_URL environment variable.")
        sys.exit(1)

    print()
    print("Step 2: Creating tables...")
    if not create_tables():
        sys.exit(1)

    print()
    print("=" * 60)
    print("Database is ready! You can now start the application.")
    print("=" * 60)


if __name__ == "__main__":
    main()
