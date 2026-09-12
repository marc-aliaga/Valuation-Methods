# -----------------------
# CERTAINTY EQUIVALENT NPV (WITH INITIAL INVESTMENT)
# -----------------------

# Cash flows CF_t
cash_flows = [100000, 150000, 200000, 250000, 300000]

# Certainty-equivalent factors α_t (0 < α ≤ 1)
certainty_factors = [0.9, 0.85, 0.8, 0.75, 0.7]

# Risk-free rate r_f
rf = 0.03

# Initial investment I (cash outflow at t = 0)
initial_investment = 400000   # user input

# -----------------------
# NPV FUNCTION
# -----------------------
def npv(rate, cashflows):
    value = 0.0
    for t, cf in enumerate(cashflows, start=1):
        value += cf / (1 + rate) ** t
    return value

# -----------------------
# CERTAINTY EQUIVALENT CASH FLOWS
# CE_t = α_t * CF_t
# -----------------------
ce_cash_flows = [
    cf * alpha for cf, alpha in zip(cash_flows, certainty_factors)
]

# -----------------------
# PRESENT VALUE OF CE CASH FLOWS
# -----------------------
pv_ce = npv(rf, ce_cash_flows)

# -----------------------
# NET PRESENT VALUE
# NPV = PV − I
# -----------------------
npv_ce = pv_ce - initial_investment

print("Certainty-Equivalent Cash Flows:")
for t, cf in enumerate(ce_cash_flows, start=1):
    print(f"Year {t}: {cf:,.2f}")

print(f"\nPresent Value of CE Cash Flows: ${pv_ce:,.2f}")
print(f"Initial Investment: ${initial_investment:,.2f}")
print(f"Certainty Equivalent NPV: ${npv_ce:,.2f}")
