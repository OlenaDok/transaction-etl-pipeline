CREATE SCHEMA IF NOT EXISTS stg;

CREATE TABLE IF NOT EXISTS STG.currency_rates (
	rate_date DATE NOT NULL,
	currency_code VARCHAR(3) NOT NULL,
	currency_name VARCHAR(100),
	nominal INTEGER NOT NULL,
	rate NUMERIC(12,4) NOT NULL,
	loaded_at TIMESTAMP NOT NULL DEFAULT now(),
	PRIMARY KEY (rate_date, currency_code)	
);