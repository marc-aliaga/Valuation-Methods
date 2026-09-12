# Startup Valuation Tool (CAPM-based)
# Method: First Chicago using CAPM discount rate

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------
# 1. INPUTS
# -----------------------
cash_flows = {
    'year': [1, 2, 3, 4, 5],
    'base': [100000, 150000, 200000, 250000, 300000],
    'best': [120000, 180000, 240000, 300000, 360000],
    'worst': [80000, 120000, 160000, 200000, 240000]
}

probabilities = {
    'best': 0.2,
    'base': 0.5,
    'worst': 0.3
}

# CAPM inputs
rf = 0.03     # Risk-free rate
beta = 1.2    # Startup beta
rm = 0.08     # Expected market return

df = pd.DataFrame(cash_flows)

# -----------------------
# 2. DISCOUNT RATE (CAPM)
# -----------------------
discount_rate = rf + beta * (rm - rf)
print(f"Discount rate (CAPM): {discount_rate:.2%}\n")

# -----------------------
# 3. NPV FUNCTION
# -----------------------
def npv(rate, cashflows):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows, start=1))

# -----------------------
# 4. FIRST CHICAGO METHOD
# -----------------------
npv_best = npv(discount_rate, df['best'])
npv_base = npv(discount_rate, df['base'])
npv_worst = npv(discount_rate, df['worst'])

first_chicago_value = (
    probabilities['best'] * npv_best +
    probabilities['base'] * npv_base +
    probabilities['worst'] * npv_worst
)

print(f"NPV (Best):  ${npv_best:,.0f}")
print(f"NPV (Base):  ${npv_base:,.0f}")
print(f"NPV (Worst): ${npv_worst:,.0f}\n")

print(f"First Chicago Valuation (CAPM): ${first_chicago_value:,.0f}\n")

# -----------------------
# 5. DISPLAY TABLE
# -----------------------
print("Projected Cash Flows:")
print(df.to_string(index=False))

# -----------------------
# 6. VISUALIZATION
# -----------------------
sns.set_style("whitegrid")

# Cash flows over time
plt.figure(figsize=(10, 6))
plt.plot(df['year'], df['best'], marker='o', label='Best Case')
plt.plot(df['year'], df['base'], marker='o', label='Base Case')
plt.plot(df['year'], df['worst'], marker='o', label='Worst Case')
plt.title('Projected Cash Flows')
plt.xlabel('Year')
plt.ylabel('Cash Flow ($)')
plt.legend()
plt.show()

# NPV by scenario
plt.figure(figsize=(6, 4))
plt.bar(['Best', 'Base', 'Worst'], [npv_best, npv_base, npv_worst])
plt.title('NPV by Scenario (CAPM)')
plt.ylabel('NPV ($)')
plt.show()
