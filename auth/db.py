import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """
    Creates and returns a fresh MySQL connection.
    Always close it after use with conn.close()
    """
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", os.getenv("MYSQLHOST", "localhost")),
        user=os.getenv("MYSQL_USER", os.getenv("MYSQLUSER", "root")),
        password=os.getenv("MYSQL_PASSWORD", os.getenv("MYSQLPASSWORD", "")),
        database=os.getenv("MYSQL_DB", os.getenv("MYSQLDATABASE", "mutualscope_db"))
    )


def init_db():
    """
    Ensure the users table exists. Safe to call on startup.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    cursor.close()
    conn.close()

