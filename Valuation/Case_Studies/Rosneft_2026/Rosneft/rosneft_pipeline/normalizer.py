"""
Normalize all extracted values to a common unit and currency.
Rosneft reports in billions of RUB. We convert everything to millions of RUB.
"""

UNIT_MULTIPLIERS = {
    "units": 1.0,
    "thousands": 1e-3,
    "millions": 1.0,
    "billions": 1e3,
}

CURRENCY_TO_USD = {
    # Approximate rates — update as needed for your analysis
    "USD": 1.0,
    "RUB": 0.011,   # ~1 RUB = 0.011 USD (adjust to your period avg)
    "EUR": 1.08,
}


def normalize_value(value, unit, currency, target_currency="RUB", target_unit="millions"):
    """Convert a value to target currency and unit."""
    if value is None:
        return None

    # Unit conversion
    src_mult = UNIT_MULTIPLIERS.get(unit, 1.0)
    tgt_mult = UNIT_MULTIPLIERS.get(target_unit, 1.0)
    value_in_target_unit = value * (src_mult / tgt_mult)

    # Currency conversion
    if currency != target_currency:
        usd_value = value_in_target_unit * CURRENCY_TO_USD.get(currency, 1.0)
        value_in_target_unit = usd_value / CURRENCY_TO_USD.get(target_currency, 1.0)

    return value_in_target_unit


def normalize_year_data(year_data, currency, unit):
    """Apply normalization to every value in a year's data dict."""
    normalized = {}
    for statement, items in year_data.items():
        normalized[statement] = {}
        for canonical, values in items.items():
            normalized[statement][canonical] = [
                normalize_value(v, unit, currency) for v in values
            ]
    return normalized