import psycopg2
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv(f".env.{os.getenv('APP_ENV', 'development')}")

# CREATE TABLE links (
#     id SERIAL PRIMARY KEY,
#     url VARCHAR(2048) NOT NULL,
#     slug VARCHAR(20) UNIQUE NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     expires_at TIMESTAMP,
#     clicks INT DEFAULT 0
# );

def execute(query, *args, fetch=False):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, args)
            conn.commit()
            if fetch:
                return cur.fetchall()
    finally:
        conn.close()
