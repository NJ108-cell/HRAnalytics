#!/usr/bin/env python3
"""
HR Analytics System - Initialization and Run Script
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from init_db import init_database, create_dummy_data, get_database_stats


def main():
    """Main entry point"""
    print("=" * 60)
    print("HR ANALYTICS SYSTEM - INITIALIZATION")
    print("=" * 60)
    print()
    
    # Check if database exists
    db_exists = os.path.exists('hr_analytics.db')
    
    if not db_exists:
        print("Database not found. Creating database...")
        init_database(app)
        
        response = input("\nWould you like to create dummy data for testing? (yes/no): ")
        if response.lower() in ['yes', 'y']:
            print("\nCreating dummy data...")
            create_dummy_data(app)
            print("\nDummy data created successfully!")
            get_database_stats(app)
        else:
            print("\nSkipping dummy data creation.")
    else:
        print("Database already exists.")
        get_database_stats(app)
    
    print("\n" + "=" * 60)
    print("STARTING HR ANALYTICS SYSTEM")
    print("=" * 60)
    print("\nAccess the application at: http://localhost:5000")
    print("Default login credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
