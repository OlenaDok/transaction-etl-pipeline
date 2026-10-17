from load_rates import parse_data

SAMPLE = {
    "Date": "2026-10-17T11:30:00+03:00",
    "PreviousDate": "2026-10-16T11:30:00+03:00",
    "PreviousURL": "//www.cbr-xml-daily.ru/archive/2026/10/16/daily_json.js",
    "Timestamp": "2026-10-16T20:00:00+03:00",
    "Valute": {
            "AUD": {
                "ID": "R01010",
                "NumCode": "036",
                "CharCode": "AUD",
                "Nominal": 1,
                "Name": "Австралийский доллар",
                        "Value": 58.0892,
                        "Previous": 58.2551
            },
        "AZN": {
                "ID": "R01020A",
                "NumCode": "944",
                "CharCode": "AZN",
                "Nominal": 1,
                "Name": "Азербайджанский манат",
                        "Value": 49.1869,
                        "Previous": 49.2706
        },
        "DZD": {
                "ID": "R01030",
                "NumCode": "012",
                "CharCode": "DZD",
                "Nominal": 100,
                "Name": "Алжирских динаров",
                        "Value": 62.2034,
                        "Previous": 62.3078
        },
    }
}


def test_parse_rates_returns_row_per_currency():
    rows = parse_data(SAMPLE)
    assert len(rows) == 3


def test_parse_cuts_date():
    rows = parse_data(SAMPLE)
    assert rows[0][0] == "2026-10-17"


def test_parse_keeps_nominal():
    rows = parse_data(SAMPLE)
    print(rows)
    DZD = [r for r in rows if r[1] == "DZD"][0]
    print(DZD)
    assert DZD[3] == 100
