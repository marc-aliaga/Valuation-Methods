import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# PARAMETERS
# ======================
asset_1 = "ROSN.ME"
asset_2 = "^GSPC"
start = "2022-01-01"
end = "2026-09-13"

output_returns_file = "Returns.xlsx"
output_stats_file   = "Stats.xlsx"

# ======================
# DOWNLOAD DATA
# ======================
data = yf.download(
    [asset_1, asset_2],
    start=start,
    end=end,
    auto_adjust=True,
    progress=False
)["Close"]

data = data[[asset_1, asset_2]].dropna()

# ======================
# LOG RETURNS (daily)
# ======================
returns = np.log(data / data.shift(1)).dropna()
X = returns[asset_1]
Y = returns[asset_2]

# ======================
# MOMENTS
# ======================
EX, EY = X.mean(), Y.mean()

var_X = np.mean((X - EX) ** 2)
var_Y = np.mean((Y - EY) ** 2)
cov_XY = np.mean((X - EX) * (Y - EY))
corr_XY = cov_XY / np.sqrt(var_X * var_Y)

vol_X, vol_Y = np.sqrt(var_X), np.sqrt(var_Y)

# ======================
# BETA (daily, both directions)
# ======================
beta_Y_on_X = cov_XY / var_X   # SOFI sensitivity to ROSN
beta_X_on_Y = cov_XY / var_Y   # ROSN sensitivity to SOFI

# ======================
# WEEKLY RETURNS + WEEKLY BETA
# ======================
# Resample prices to weekly (Friday close), then compute log returns
weekly_prices = data.resample("W-FRI").last()
weekly_returns = np.log(weekly_prices / weekly_prices.shift(1)).dropna()

wX = weekly_returns[asset_1]
wY = weekly_returns[asset_2]

w_var_X = np.var(wX, ddof=0)
w_var_Y = np.var(wY, ddof=0)
w_cov   = np.mean((wX - wX.mean()) * (wY - wY.mean()))
w_corr  = w_cov / np.sqrt(w_var_X * w_var_Y)

weekly_beta_Y_on_X = w_cov / w_var_X
weekly_beta_X_on_Y = w_cov / w_var_Y

# ======================
# BUILD RETURNS SPREADSHEET
# ======================
# Align daily prices + returns
daily_df = pd.concat(
    [data.add_suffix("_Price"), returns.add_suffix("_LogRet")],
    axis=1
)

# Align weekly prices + returns
weekly_df = pd.concat(
    [weekly_prices.add_suffix("_Price"), weekly_returns.add_suffix("_LogRet")],
    axis=1
)

with pd.ExcelWriter(output_returns_file, engine="openpyxl") as writer:
    daily_df.to_excel(writer, sheet_name="Daily")
    weekly_df.to_excel(writer, sheet_name="Weekly")
    returns.to_excel(writer, sheet_name="Daily_Returns_Only")
    weekly_returns.to_excel(writer, sheet_name="Weekly_Returns_Only")

print(f"[OK] Returns written to: {output_returns_file}")

# ======================
# BUILD STATS TABLE
# ======================
stats_rows = [
    ("Expected Return (mean)",        EX,                EY),
    ("Variance (population)",         var_X,             var_Y),
    ("Volatility (std, pop)",         vol_X,             vol_Y),
    ("Skewness",                      X.skew(),          Y.skew()),
    ("Excess Kurtosis",               X.kurtosis(),      Y.kurtosis()),
    ("Min",                           X.min(),           Y.min()),
    ("Max",                           X.max(),           Y.max()),
    ("Observations (daily)",          len(X),            len(Y)),
    ("Observations (weekly)",         len(wX),           len(wY)),
    ("Weekly Volatility",             np.sqrt(w_var_X),  np.sqrt(w_var_Y)),
]

stats_df = pd.DataFrame(stats_rows, columns=["Metric", asset_1, asset_2])

joint_rows = [
    ("Covariance (daily)",            cov_XY),
    ("Correlation (daily)",           corr_XY),
    ("Covariance (weekly)",           w_cov),
    ("Correlation (weekly)",          w_corr),
    ("Beta (SOFI on ROSN, daily)",    beta_Y_on_X),
    ("Beta (ROSN on SOFI, daily)",    beta_X_on_Y),
    ("Beta (SOFI on ROSN, weekly)",   weekly_beta_Y_on_X),
    ("Beta (ROSN on SOFI, weekly)",   weekly_beta_X_on_Y),
    ("Theta (arccos corr, daily)",    np.arccos(np.clip(corr_XY, -1, 1))),
]

joint_df = pd.DataFrame(joint_rows, columns=["Joint Metric", "Value"])

with pd.ExcelWriter(output_stats_file, engine="openpyxl") as writer:
    stats_df.to_excel(writer, sheet_name="Per_Asset_Stats", index=False)
    joint_df.to_excel(writer, sheet_name="Joint_Stats", index=False)

print(f"[OK] Stats written to:   {output_stats_file}")

# ======================
# GEOMETRIC REPRESENTATION
# ======================
theta = np.arccos(np.clip(corr_XY, -1.0, 1.0))

v1 = np.array([vol_X, 0.0])
v2 = np.array([
    vol_Y * np.cos(theta),
    vol_Y * np.sin(theta)
])

# ======================
# DASHBOARD
# ======================
fig, axs = plt.subplots(2, 2, figsize=(16, 10))

# --- Prices
data.plot(ax=axs[0, 0])
axs[0, 0].set_title("Adjusted Prices")

# --- Returns
returns.plot(ax=axs[0, 1])
axs[0, 1].set_title("Log Returns")

# --- Scatter
axs[1, 0].scatter(X, Y, alpha=0.5)
axs[1, 0].axhline(0, linewidth=0.8)
axs[1, 0].axvline(0, linewidth=0.8)
axs[1, 0].set_title("Returns Scatter (Covariance)")
axs[1, 0].set_xlabel(asset_1)
axs[1, 0].set_ylabel(asset_2)

# --- Vector geometry panel
ax = axs[1, 1]
scale = max(vol_X, vol_Y) * 0.05

ax.arrow(0, 0, v1[0], v1[1], head_width=scale, length_includes_head=True)
ax.arrow(0, 0, v2[0], v2[1], head_width=scale, length_includes_head=True)

ax.text(v1[0] * 1.05, v1[1], asset_1)
ax.text(v2[0] * 1.05, v2[1] * 1.05, asset_2)

ax.set_aspect("equal")
ax.set_title("Assets as Vectors in $L^2(\\Omega)$")
ax.set_xlabel("Risk dimension 1")
ax.set_ylabel("Risk dimension 2")
ax.grid(True)

# ----------------------
# NUMERIC STATS OVERLAY
# ----------------------
stats_text = f"""
PORTFOLIO STATISTICS
====================

{asset_1}
--------------------
Expected Return : {EX:.6f}
Variance        : {var_X:.6f}
Volatility      : {vol_X:.6f}

{asset_2}
--------------------
Expected Return : {EY:.6f}
Variance        : {var_Y:.6f}
Volatility      : {vol_Y:.6f}

JOINT METRICS
--------------------
Covariance      : {cov_XY:.6f}
Correlation     : {corr_XY:.4f}
Beta ({asset_2} on {asset_1}) : {beta_Y_on_X:.4f}
Beta ({asset_1} on {asset_2}) : {beta_X_on_Y:.4f}
"""

ax.text(
    0.02, 0.98,
    stats_text,
    fontsize=10,
    verticalalignment="top",
    family="monospace",
    transform=ax.transAxes
)

plt.tight_layout()
plt.show()