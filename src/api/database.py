from psycopg2.extras import RealDictCursor
from db import get_connection


def fetch_all(sql, params=()):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as curr:
            curr.execute(sql, params)
            return curr.fetchall()
    finally:
        curr.close()


def fetch_one(sql, params=()):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as curr:
            curr.execute(sql, params)
            return curr.fetchone()
    finally:
        curr.close()
