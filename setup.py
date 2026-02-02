#!/usr/bin/env python
"""
Setup script for NutriGem Django Backend
Run this script to set up the database and load initial data
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutrigem_backend.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def setup_database():
    """Create database tables and load initial data"""
    print("Setting up NutriGem Django Backend...")
    print("\n1. Creating database migrations...")
    call_command('makemigrations')
    
    print("\n2. Applying migrations...")
    call_command('migrate')
    
    print("\n3. Loading initial food data...")
    call_command('load_initial_food_data')
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Run the server: python manage.py runserver")
    print("3. Access API at: http://localhost:8000/api/")
    print("4. Access Admin at: http://localhost:8000/admin/")

if __name__ == '__main__':
    try:
        setup_database()
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)

