#!/usr/bin/env python3
"""Test script to verify MySQL database connection with pymysql"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test the database connection using pymysql"""
    
    # Get the raw database URL
    raw_database_url = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://portfolio_user:portfolio_pass@portfolio_mysql:3306/portfolio?charset=utf8mb4",
    )
    
    # Ensure we're using pymysql driver for MySQL
    if raw_database_url.startswith("mysql://"):
        database_url = raw_database_url.replace("mysql://", "mysql+pymysql://", 1)
        # Add charset if not present
        if "charset=" not in database_url:
            database_url += "?charset=utf8mb4" if "?" not in database_url else "&charset=utf8mb4"
    else:
        database_url = raw_database_url
    
    print(f"Original URL: {raw_database_url}")
    print(f"Modified URL: {database_url}")
    
    try:
        # Create engine
        engine = create_engine(database_url, pool_pre_ping=True)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✓ Database connection successful!")
            
            # Check tables
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            print(f"✓ Found {len(tables)} tables: {tables}")
            
            # Check users table
            if 'users' in tables:
                result = conn.execute(text("SELECT COUNT(*) FROM users"))
                count = result.scalar()
                print(f"✓ Users table has {count} records")
            
        return True
        
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)