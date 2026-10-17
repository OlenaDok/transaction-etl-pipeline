
INSERT INTO STG.currency_rates (rate_date, currency_code, currency_name, nominal, rate)
VALUES(%s, %s, %s, %s, %s)
ON CONFLICT (rate_date, currency_code)
DO UPDATE SET
    currency_code = EXCLUDED.currency_code,
    nominal = EXCLUDED.nominal,
    rate = EXCLUDED.rate,
    loaded_at = now();