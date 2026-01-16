#!/usr/bin/env python3
"""
Mock Data Generation Script

Generates test data for the Umatter backend:
- 2 users
- 10 wellness metrics per user (spread over 2 days)

Usage:
    python generate_mock_data.py
"""

import sys
from datetime import datetime, timedelta
import random

from app.database import SessionLocal, engine
from app.models import UserTable, WellnessMetrics


def generate_mock_data(auto_mode=False):
    """
    Generate mock data for testing.

    Args:
        auto_mode: If True, automatically clears existing data without prompting
    """
    db = SessionLocal()

    try:
        print("=" * 60)
        print("Generating Mock Data for Umatter Backend")
        print("=" * 60)
        print()

        # Check if data already exists
        existing_users = db.query(UserTable).count()
        if existing_users > 0:
            if auto_mode:
                print(f"\n⚠️  Database already has {existing_users} users.")
                print("Running in AUTO MODE - clearing existing data...")
                db.query(WellnessMetrics).delete()
                db.query(UserTable).delete()
                db.commit()
                print("✓ Existing data cleared")
            else:
                response = input(f"\n⚠️  Database already has {existing_users} users. Clear existing data? (yes/no): ")
                if response.lower() == 'yes':
                    print("\nClearing existing data...")
                    db.query(WellnessMetrics).delete()
                    db.query(UserTable).delete()
                    db.commit()
                    print("✓ Existing data cleared")
                else:
                    print("\nKeeping existing data and adding new records...")

        print("\n" + "=" * 60)
        print("Creating Users")
        print("=" * 60)

        # Create 2 users
        users = []
        for i in range(2):
            user = UserTable()
            db.add(user)
            db.commit()
            db.refresh(user)
            users.append(user)
            print(f"✓ Created User {i+1}: userid={user.userid}")

        print("\n" + "=" * 60)
        print("Creating Wellness Metrics")
        print("=" * 60)

        # Generate wellness metrics for each user
        # Spread over 2 days, 10 records per user
        base_time = datetime.utcnow() - timedelta(days=2)

        for user_idx, user in enumerate(users):
            print(f"\nUser {user_idx + 1} (userid={user.userid}):")
            print("-" * 40)

            # Generate 10 wellness scores spread over 2 days
            # Day 1: 5 records, Day 2: 5 records
            for record_idx in range(10):
                # Determine which day (0 or 1)
                day = record_idx // 5

                # Time within the day (spread throughout the day)
                hours_offset = (record_idx % 5) * 4 + random.randint(0, 120)  # Add 0-2 hours random
                record_time = base_time + timedelta(days=day, minutes=hours_offset)

                # Generate wellness score with some pattern
                # User 1: Improving trend (5.0 -> 8.5)
                # User 2: Declining trend (8.0 -> 5.5)
                if user_idx == 0:
                    # Improving trend
                    base_score = 5.0 + (record_idx * 0.35)
                    wellness_score = round(base_score + random.uniform(-0.3, 0.3), 1)
                else:
                    # Declining trend
                    base_score = 8.0 - (record_idx * 0.25)
                    wellness_score = round(base_score + random.uniform(-0.3, 0.3), 1)

                # Ensure score is within 0-10 range
                wellness_score = max(0.0, min(10.0, wellness_score))

                # Create wellness metric
                metric = WellnessMetrics(
                    userid=user.userid,
                    time=record_time,
                    wellness_score=wellness_score
                )
                db.add(metric)
                db.commit()
                db.refresh(metric)

                # Print with day indicator
                day_label = "Day 1" if day == 0 else "Day 2"
                print(f"  {day_label} - Record {record_idx + 1:2d}: "
                      f"score={wellness_score:4.1f}, "
                      f"time={record_time.strftime('%Y-%m-%d %H:%M')}")

        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)

        # Generate summary
        total_users = db.query(UserTable).count()
        total_metrics = db.query(WellnessMetrics).count()

        print(f"\nTotal Users Created: {total_users}")
        print(f"Total Wellness Metrics: {total_metrics}")

        print("\nPer User Breakdown:")
        for user in users:
            user_metrics = db.query(WellnessMetrics).filter(
                WellnessMetrics.userid == user.userid
            ).all()

            if user_metrics:
                avg_score = sum(m.wellness_score for m in user_metrics) / len(user_metrics)
                first_score = user_metrics[0].wellness_score
                last_score = user_metrics[-1].wellness_score

                # Determine trend
                if last_score > first_score + 0.5:
                    trend = "📈 Improving"
                elif last_score < first_score - 0.5:
                    trend = "📉 Declining"
                else:
                    trend = "➡️  Stable"

                print(f"\n  User {user.userid}:")
                print(f"    Records: {len(user_metrics)}")
                print(f"    Average Score: {avg_score:.2f}")
                print(f"    First Score: {first_score:.1f}")
                print(f"    Last Score: {last_score:.1f}")
                print(f"    Trend: {trend}")

        print("\n" + "=" * 60)
        print("Test API Endpoints")
        print("=" * 60)
        print("\nYou can now test these endpoints:\n")

        for user in users:
            print(f"# User {user.userid}")
            print(f"curl http://localhost:8000/api/v1/wellness/users/{user.userid}")
            print(f"curl http://localhost:8000/api/v1/wellness/users/{user.userid}/wellness-metrics")
            print(f"curl http://localhost:8000/api/v1/wellness/users/{user.userid}/wellness-trend?days=7")
            print()

        print("=" * 60)
        print("✓ Mock Data Generation Complete!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n✗ Error generating mock data: {e}", file=sys.stderr)
        db.rollback()
        return False

    finally:
        db.close()


def clear_all_data():
    """Clear all data from the database."""
    db = SessionLocal()

    try:
        print("Clearing all data...")
        db.query(WellnessMetrics).delete()
        db.query(UserTable).delete()
        db.commit()
        print("✓ All data cleared")
        return True

    except Exception as e:
        print(f"✗ Error clearing data: {e}", file=sys.stderr)
        db.rollback()
        return False

    finally:
        db.close()


def show_current_data():
    """Display current data in the database."""
    db = SessionLocal()

    try:
        print("\n" + "=" * 60)
        print("Current Database Contents")
        print("=" * 60)

        users = db.query(UserTable).all()

        if not users:
            print("\nNo users found in database.")
            return

        print(f"\nTotal Users: {len(users)}")

        for user in users:
            metrics = db.query(WellnessMetrics).filter(
                WellnessMetrics.userid == user.userid
            ).order_by(WellnessMetrics.time.asc()).all()

            print(f"\n{'=' * 60}")
            print(f"User ID: {user.userid}")
            print(f"{'=' * 60}")

            if not metrics:
                print("  No wellness metrics")
                continue

            print(f"  Total Records: {len(metrics)}")
            print(f"  Average Score: {sum(m.wellness_score for m in metrics) / len(metrics):.2f}")
            print(f"\n  Recent Metrics:")

            for metric in metrics[-5:]:  # Show last 5
                print(f"    {metric.time.strftime('%Y-%m-%d %H:%M')} - "
                      f"Score: {metric.wellness_score:.1f}")

    finally:
        db.close()


def main():
    """Main function with menu."""

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'clear':
            clear_all_data()
            return
        elif command == 'show':
            show_current_data()
            return
        elif command == 'auto':
            # Auto mode: no prompts, clears existing data automatically
            success = generate_mock_data(auto_mode=True)
            sys.exit(0 if success else 1)
        elif command == 'help':
            print("Usage:")
            print("  python generate_mock_data.py         # Generate mock data (interactive)")
            print("  python generate_mock_data.py auto    # Generate mock data (auto mode, no prompts)")
            print("  python generate_mock_data.py clear   # Clear all data")
            print("  python generate_mock_data.py show    # Show current data")
            return

    # Default: generate mock data (interactive mode)
    success = generate_mock_data(auto_mode=False)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
