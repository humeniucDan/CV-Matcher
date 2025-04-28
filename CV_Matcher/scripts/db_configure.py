import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("PG_DBNAME"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT")
}


def create_tables():
    """Create tables without timestamps or UUIDs"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS cv_embeddings (
            id SERIAL PRIMARY KEY,
            embedding FLOAT[] NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS job_embeddings (
            id SERIAL PRIMARY KEY,
            embedding FLOAT[] NOT NULL
        )
        """
    )

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for command in commands:
            cursor.execute(command)

        conn.commit()
        print("Tables created successfully!")

        # Verify tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name IN ('cv_embeddings', 'job_embeddings')
        """)
        print("Created tables:", [row[0] for row in cursor.fetchall()])

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    create_tables()