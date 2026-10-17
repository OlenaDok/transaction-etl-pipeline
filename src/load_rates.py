from db import get_connection
import config
import sys
import requests
import psycopg2

from pathlib import Path

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


def get_data(url):
    """Get data rates from API"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def parse_data(data):
    """Parse json into list"""
    rate_date = data["Date"][:10]
    rows = []

    for value in data["Valute"].values():
        rows.append(
            (rate_date, value["CharCode"], value["Name"], value["Nominal"], value["Value"]))

    return rows


def read_sql(filename):
    """Read SQL query from file in sql/ folder."""

    return (SQL_DIR / filename).read_text(encoding="utf-8")


def load_data(rows):
    """Load data to a table (upsert)"""
    sql = read_sql("upsert_currency_rates.sql")
    conn = get_connection()

    print(sql)

    try:
        with conn:
            with conn.cursor() as cur:
                cur.executemany(sql, rows)
    finally:
        conn.close()


def main():
    try:
        data = get_data(config.RATES_API_URL)
        rows = parse_data(data)
        load_data(rows)

    except requests.exceptions.RequestException as e:
        print(f"[EXTRACT] Ошибка при запросе к API: {e}")
        return 1
    except (KeyError, TypeError) as e:
        print(f"[TRANSFORM] Неожиданный формат данных от API: {e}")
        return 1
    except psycopg2.Error as e:
        print(f"[LOAD] Ошибка базы данных: {e}")
        return 1

    print(f"Загружено курсов: {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
