#!/usr/bin/env python
"""Script to create the MySQL database"""
import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Connect to MySQL server (without specifying database)
    conn = MySQLdb.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '1234'),
        port=int(os.getenv('DB_PORT', '3306'))
    )
    
    cursor = conn.cursor()
    
    # Create database
    db_name = os.getenv('DB_NAME', 'nutrigem_db')
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn.commit()
    
    print(f"Database '{db_name}' created successfully!")
    
    cursor.close()
    conn.close()
    
except MySQLdb.Error as e:
    print(f"Error creating database: {e}")
    exit(1)

