"""
Configuration: file paths, page hints, and canonical line-item mapping.
"""

from pathlib import Path

# ---------- PATHS ----------
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "rosneft_financials.xlsx"

# ---------- PDF SOURCES ----------
# Each entry: fiscal_year -> (filename, [page hints], currency, unit)
# Page numbers are 0-indexed. Adjust if your PDFs differ.
PDF_SOURCES = {
    2023: {
        "file": "2023_Audites.pdf",
        "balance_sheet_pages": [4],      # page 5 in 1-indexed = 4 in 0-indexed
        "income_pages": [5],
        "cashflow_pages": [6],
        "currency": "RUB",
        "unit": "billions",
    },
    2024: {
        "file": "12m2024_ENG.pdf",
        "balance_sheet_pages": [4],
        "income_pages": [5],
        "cashflow_pages": [6],
        "currency": "RUB",
        "unit": "billions",
    },
    2025: {
        "file": "12m2025_ENG.pdf",
        "balance_sheet_pages": [4],
        "income_pages": [5],
        "cashflow_pages": None,          # 2025 file has NO cash flow statement
        "currency": "RUB",
        "unit": "billions",
    },
}

# ---------- CANONICAL LINE-ITEM MAP ----------
# Maps raw PDF captions -> canonical names (matching your Amazon template)
# Keys are lowercase, stripped versions of what appears in the PDF.

CANONICAL_MAP = {
    # --- Balance Sheet ---
    "current assets": "CurrentAssets",
    "non-current assets": "NonCurrentAssets",
    "total non-current assets": "TotalNonCurrentAssets",
    "total assets": "TotalAssets",
    "current liabilities": "CurrentLiabilities",
    "non-current liabilities": "NonCurrentLiabilities",
    "total equity": "TotalEquity",
    "total liabilities and equity": "TotalLiabilitiesAndEquity",
    "property, plant and equipment": "PPE",
    "other non-current assets": "OtherNonCurrentAssets",
    "share capital": "ShareCapital",
    "retained earnings": "RetainedEarnings",
    "other funds and reserves": "OtherFundsAndReserves",

    # --- Income Statement ---
    "oil, gas, petroleum products and petrochemicals sales": "Revenue_OilGas",
    "support services, other revenues, equity share in profit of associates and joint ventures": "Revenue_Other",
    "total revenues and equity share in profits of associates and joint ventures": "TotalRevenue",
    "production and operating expenses": "ProductionExpenses",
    "depreciation, depletion, amortization and impairment": "DDA",
    "taxes other than income tax": "TaxesOtherThanIncome",
    "other costs and expenses": "OtherCosts",
    "total costs and expenses": "TotalCosts",
    "operating profit": "OperatingProfit",
    "other expenses": "OtherExpenses",
    "profit before income tax": "ProfitBeforeTax",
    "income tax expense": "IncomeTax",
    "profit for the year": "NetIncome",
    "profit for the year attributable to rosneft shareholders": "NetIncomeAttributable",

    # --- Cash Flow (from 2024 file, which has one) ---
    "net cash provided by operating activities": "CFO",
    "net cash provided by / used in operating activities": "CFO",
    "net cash used in investing activities": "CFI",
    "net cash used in financing activities": "CFF",
    "capital expenditures": "Capex",
    "proceeds from loans and borrowings": "ProceedsFromLoans",
    "repayment of loans and borrowings": "RepaymentOfLoans",
    "other financing repayment": "OtherFinancingRepayment",
    "net increase in cash and cash equivalents": "NetChangeInCash",
}

# ---------- OUTPUT TEMPLATE LINE ORDER ----------
# The order in which lines appear in the final Excel sheet.
# This mirrors your Amazon template structure.

OUTPUT_LINE_ORDER = [
    # Balance Sheet
    "CurrentAssets",
    "TotalNonCurrentAssets",
    "TotalAssets",
    "CurrentLiabilities",
    "NonCurrentLiabilities",
    "TotalEquity",
    # Income Statement
    "TotalRevenue",
    "ProductionExpenses",
    "DDA",
    "TaxesOtherThanIncome",
    "OtherCosts",
    "TotalCosts",
    "OperatingProfit",
    "ProfitBeforeTax",
    "IncomeTax",
    "NetIncome",
    "NetIncomeAttributable",
    # Cash Flow (only available for 2023, 2024)
    "CFO",
    "CFI",
    "CFF",
    "Capex",
    "NetChangeInCash",
]

# Human-readable labels for the Excel output
OUTPUT_LABELS = {
    "CurrentAssets": "Current assets",
    "TotalNonCurrentAssets": "Total non-current assets",
    "TotalAssets": "Total assets",
    "CurrentLiabilities": "Current liabilities",
    "NonCurrentLiabilities": "Non-current liabilities",
    "TotalEquity": "Total equity",
    "TotalRevenue": "Total revenues and equity share in profits",
    "ProductionExpenses": "Production and operating expenses",
    "DDA": "Depreciation, depletion, amortization and impairment",
    "TaxesOtherThanIncome": "Taxes other than income tax",
    "OtherCosts": "Other costs and expenses",
    "TotalCosts": "Total costs and expenses",
    "OperatingProfit": "Operating profit",
    "ProfitBeforeTax": "Profit before income tax",
    "IncomeTax": "Income tax expense",
    "NetIncome": "Profit for the year",
    "NetIncomeAttributable": "Profit for the year attributable to Rosneft shareholders",
    "CFO": "Net cash provided by operating activities",
    "CFI": "Net cash used in investing activities",
    "CFF": "Net cash used in financing activities",
    "Capex": "Capital expenditures",
    "NetChangeInCash": "Net increase in cash and cash equivalents",
}