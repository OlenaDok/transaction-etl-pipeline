from datetime import date

from fastapi import APIRouter, HTTPException, Query

from api.database import fetch_all, fetch_one
from api.schemas import Rate

router = APIRouter(prefix="/rates", tags=["rates"])


@router.get("", response_model=list[Rate])
def list_rates(
    rate_date: date | None = None,
    currency_code: str | None = Query(None, min_length=3, max_length=3),
    limit: int = Query(50, ge=1, le=500),
):
    sql = """
        SELECT rate_date, currency_code, currency_name, nominal, rate 
        FROM STG.currency_rates 
        WHERE 1 = 1
    """
    print(currency_code)
    params = []

    if rate_date is not None:
        sql += " AND rate_date = %s"
        params.append(rate_date)

    if currency_code is not None:
        sql += " AND currency_code = %s"
        params.append(currency_code.upper())

    sql += " ORDER BY rate_date DESC, currency_code LIMIT %s"
    params.append(limit)

    print(sql, params)
    return fetch_all(sql, params)


@router.get("/{currency_code}/latest", response_model=Rate)
def get_last_rates(currency_code: str):
    sql = """
        SELECT rate_date, currency_code, currency_name, nominal, rate
        FROM STG.currency_rates
        WHERE currency_code = %s
        order by rate_date DESC
        limit 1
    """
    row = fetch_one(sql, (currency_code.upper(),))
    if row is None:
        raise HTTPException(status_code=404, detail="Currency not found")

    return row


@router.get("/{currency_code}/history", response_model=list[Rate])
def get_rates_history(
    currency_code: str,
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = Query(50, ge=1, le=500),
):

    if date_from is not None and date_to is not None and date_from > date_to:
        raise HTTPException(
            status_code=400, detail="date_from must be less than or equal to date_to")

    sql = """
        SELECT rate_date, currency_code, currency_name, nominal, rate 
        FROM STG.currency_rates 
        WHERE currency_code = %s        
    """
    print(currency_code)
    params = []
    params.append(currency_code.upper())

    if date_from is not None:
        sql += " AND rate_date >= %s"
        params.append(date_from)

    if date_to is not None:
        sql += " AND rate_date <= %s"
        params.append(date_to)

    sql += " ORDER BY rate_date LIMIT %s"
    params.append(limit)

    print(sql, params)
    return fetch_all(sql, params)
