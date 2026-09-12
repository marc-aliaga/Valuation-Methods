"""
Main entry point: PDFs in -> Excel out.
"""

from config import PDF_SOURCES, OUTPUT_FILE
from extractor import extract_all_statements
from normalizer import normalize_year_data
from builder import build_dataframe, add_growth_columns, write_excel


def main():
    print("=" * 60)
    print("ROSNEFT FINANCIAL DATA PIPELINE")
    print("=" * 60)

    # 1. Extract
    print("\n[1/4] Extracting tables from PDFs...")
    raw_data = extract_all_statements(PDF_SOURCES)

    # 2. Normalize
    print("\n[2/4] Normalizing units and currency...")
    normalized = {}
    for year, data in raw_data.items():
        cfg = PDF_SOURCES[year]
        normalized[year] = normalize_year_data(
            data, currency=cfg["currency"], unit=cfg["unit"]
        )

    # 3. Build DataFrame
    print("\n[3/4] Building output table...")
    years = sorted(normalized.keys())
    df = build_dataframe(normalized, years)
    df = add_growth_columns(df, years)

    # 4. Write Excel
    print("\n[4/4] Writing Excel...")
    write_excel(
        df,
        OUTPUT_FILE,
        company_name="Rosneft Oil Company",
        ticker="ROSN",
        currency="RUB",
        unit="millions",
    )

    print("\n" + "=" * 60)
    print("DONE. Preview:")
    print("=" * 60)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()