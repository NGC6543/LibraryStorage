import os

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()


def create_db():
    """Connect to default database."""
    new_db = os.getenv("POSTGRES_DB")
    conn = psycopg2.connect(
        dbname="postgres",
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        port=os.getenv('DB_PORT'),
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()

    cursor.execute(
        'SELECT 1 FROM pg_database WHERE datname = %s;', (new_db,)
    )
    exists = cursor.fetchone()

    if not exists:
        cursor.execute('CREATE DATABASE "%s";', (new_db,))
        print(f'Database {new_db} created.')
    else:
        print(f'Database {new_db} already exists.')

    cursor.close()
    conn.close()
