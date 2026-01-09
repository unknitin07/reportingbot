#!/usr/bin/env python3
"""
Database Initialization Script
Run this to initialize or reset the database
"""

import os
import sys
from database import Database
from config import DATABASE_PATH, SUPER_ADMIN_ID

def main():
    print("=" * 50)
    print("Telegram Bot Database Initialization")
    print("=" * 50)
    
    # Check if database exists
    if os.path.exists(DATABASE_PATH):
        response = input(f"\nDatabase '{DATABASE_PATH}' already exists. Reset it? (yes/no): ")
        if response.lower() != 'yes':
            print("Operation cancelled.")
            sys.exit(0)
        
        # Backup existing database
        backup_path = f"{DATABASE_PATH}.backup"
        os.rename(DATABASE_PATH, backup_path)
        print(f"✅ Existing database backed up to: {backup_path}")
    
    # Initialize database
    print("\n🔧 Creating new database...")
    db = Database()
    print("✅ Database schema created successfully!")
    
    # Auto-approve super admin
    print(f"\n👑 Setting up super admin (ID: {SUPER_ADMIN_ID})...")
    db.add_user(
        user_id=SUPER_ADMIN_ID,
        username="super_admin",
        first_name="Super",
        last_name="Admin"
    )
    print("✅ Super admin configured!")
    
    # Display statistics
    stats = db.get_user_stats()
    print("\n" + "=" * 50)
    print("Database Statistics:")
    print("=" * 50)
    print(f"Total Users: {stats['total']}")
    print(f"Approved Users: {stats['approved']}")
    print(f"Pending Users: {stats['pending']}")
    print(f"Blocked Users: {stats['blocked']}")
    print("=" * 50)
    
    print("\n✨ Database initialization complete!")
    print(f"📁 Database location: {os.path.abspath(DATABASE_PATH)}")
    print("\n🚀 You can now start the bot with: python bot.py")

if __name__ == '__main__':
    main()
