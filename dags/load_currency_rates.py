import sys
from datetime import datetime, timedelta

from airflow.sdk import dag, task

sys.path.insert(0, "/opt/airflow/project/src")

default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="load_currency_rates",
    schedule="@daily",
    start_date=datetime(2026, 11, 1),
    catchup=False,
    default_args=default_args,
    tags=["etl", "cbr"],
)
def load_currency_rates():

    @task
    def get_rates():
        import config
        from load_rates import get_data
        return get_data(config.RATES_API_URL)

    @task
    def tarnsform_data(data):
        from load_rates import parse_data
        rows = parse_data(data)
        print(f"Parsed {len(rows)} rows")
        return rows

    @task
    def load_rows(rows):
        from load_rates import load_data
        load_data(rows)
        print(f"Loaded {len(rows)} rows")

    load_rows(tarnsform_data(get_rates()))


load_currency_rates()
