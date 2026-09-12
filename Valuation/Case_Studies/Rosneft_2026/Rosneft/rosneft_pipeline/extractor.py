"""
Robust PDF extractor for Rosneft financial statements.

Key improvements over v1:
1. Auto-detects which pages contain each statement (no hard-coded pages)
2. Falls back to text-based parsing when extract_tables() returns nothing
3. Fuzzy label matching with rapidfuzz
4. Splits labels from numbers when they appear in the same cell
"""

import re
import pdfplumber
from pathlib import Path
from rapidfuzz import process, fuzz


# ---------- NUMBER PARSING ----------

def clean_number(value):
    """Convert a PDF-extracted string into a float."""
    if value is None:
        return None
    s = str(value).strip()
    if s in ("", "—", "–", "-", "n/a", "N/A", "None"):
        return None

    negative = s.startswith("(") and s.endswith(")")
    s = s.strip("()")

    # Remove currency symbols and spaces
    s = re.sub(r"[₽$€£]", "", s)
    s = s.replace(" ", "").replace("\u00a0", "")

    # Handle thousands/decimal separators
    if "," in s and "." in s:
        s = s.replace(",", "")
    elif "," in s:
        if re.search(r",\d{3}$", s):
            s = s.replace(",", "")
        else:
            s = s.replace(",", ".")

    try:
        num = float(s)
        return -num if negative else num
    except ValueError:
        return None


# ---------- LABEL EXTRACTION ----------

# Regex to split "Current assets 4,283 3,839" into label + numbers
LABEL_NUMBER_SPLIT = re.compile(
    r"^(?P<label>.*?)\s+(?P<numbers>(?:[\-\(\)\d\s,\.]+\s*)+)$"
)

def split_label_and_numbers(text):
    """
    Given a cell like 'Current assets 4,283 3,839',
    return ('Current assets', [4283.0, 3839.0]).
    If no numbers, return (text, []).
    """
    if text is None:
        return "", []

    s = str(text).strip().replace("\n", " ")

    # Try to find all numbers at the end
    numbers = []
    # Match numbers like: 4,283  3,839  (1,234)  -1,234  1.5
    num_pattern = re.compile(r"\(?-?[\d,]+(?:\.\d+)?\)?")
    matches = list(num_pattern.finditer(s))

    if not matches:
        return s, []

    # Take numbers that appear after the first letter
    first_letter = re.search(r"[A-Za-z]", s)
    if not first_letter:
        return s, []

    # Split at the position of the first number that comes after text
    label_end = None
    for m in matches:
        if m.start() > first_letter.start():
            label_end = m.start()
            break

    if label_end is None:
        return s, []

    label = s[:label_end].strip(" .:-")
    number_str = s[label_end:]

    for m in num_pattern.finditer(number_str):
        v = clean_number(m.group())
        if v is not None:
            numbers.append(v)

    return label, numbers


# ---------- FUZZY MATCHING ----------

def fuzzy_canonical(label, canonical_map, threshold=80):
    """Match a label to the canonical map using fuzzy string matching."""
    if not label:
        return None

    key = label.lower().strip().rstrip(":").strip()
    if key in canonical_map:
        return canonical_map[key]

    match, score, _ = process.extractOne(
        key, canonical_map.keys(), scorer=fuzz.token_sort_ratio
    )
    if score >= threshold:
        return canonical_map[match]
    return None


# ---------- PAGE DETECTION ----------

STATEMENT_MARKERS = {
    "balance_sheet": ["total assets", "current assets", "total liabilities and equity"],
    "income": ["operating profit", "profit before income tax", "total revenues"],
    "cashflow": ["operating activities", "investing activities", "financing activities"],
}

def find_statement_pages(pdf_path):
    """
    Scan all pages and return a dict:
        { 'balance_sheet': [page_idx, ...], 'income': [...], 'cashflow': [...] }
    based on keyword hits in the page text.
    """
    found = {"balance_sheet": [], "income": [], "cashflow": []}

    with pdfplumber.open(pdf_path) as pdf:
        for idx, page in enumerate(pdf.pages):
            text = (page.extract_text() or "").lower()

            for statement, markers in STATEMENT_MARKERS.items():
                hits = sum(1 for m in markers if m in text)
                if hits >= 2:   # require at least 2 markers to be confident
                    found[statement].append(idx)

    return found


# ---------- TABLE EXTRACTION ----------

def extract_page_tables(pdf_path, page_indices):
    """Extract tables from given pages. Returns list of raw tables."""
    tables = []
    if not page_indices:
        return tables

    with pdfplumber.open(pdf_path) as pdf:
        for idx in page_indices:
            if idx >= len(pdf.pages):
                continue
            page = pdf.pages[idx]

            # Try default table extraction
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)
            else:
                # Fallback: parse text line-by-line
                text = page.extract_text() or ""
                pseudo_table = [[line] for line in text.split("\n") if line.strip()]
                tables.append(pseudo_table)

    return tables


# ---------- STATEMENT PARSING ----------

def parse_statement(raw_tables, canonical_map):
    """
    Parse a list of raw tables into { canonical_name: [values] }.
    Handles both well-formed tables and text-line fallbacks.
    """
    result = {}

    for table in raw_tables:
        for row in table:
            if not row:
                continue

            # A row may have 1 cell (text fallback) or many cells (real table)
            first_cell = str(row[0]) if row[0] else ""

            # Try splitting label + numbers from the first cell
            label, numbers_from_first = split_label_and_numbers(first_cell)

            # Also collect numbers from other cells
            numbers_from_rest = []
            for cell in row[1:]:
                v = clean_number(cell)
                if v is not None:
                    numbers_from_rest.append(v)

            all_numbers = numbers_from_first + numbers_from_rest

            if not label or not all_numbers:
                continue

            canonical = fuzzy_canonical(label, canonical_map)
            if canonical and canonical not in result:
                result[canonical] = all_numbers

    return result


# ---------- MAIN ENTRY POINT ----------

def extract_all_statements(pdf_sources):
    """
    Extract all statements from all PDFs.
    Returns: { year: { 'balance_sheet': {...}, 'income': {...}, 'cashflow': {...} } }
    """
    from config import INPUT_DIR, CANONICAL_MAP

    all_data = {}

    for year, cfg in pdf_sources.items():
        pdf_path = INPUT_DIR / cfg["file"]
        if not pdf_path.exists():
            print(f"⚠️  Missing PDF: {pdf_path}")
            continue

        print(f"\n📄 Extracting {year}: {cfg['file']}")

        # Auto-detect pages
        pages = find_statement_pages(pdf_path)
        print(f"   Detected pages -> BS: {pages['balance_sheet']}, "
              f"IS: {pages['income']}, CF: {pages['cashflow']}")

        year_data = {}

        for statement_key in ("balance_sheet", "income", "cashflow"):
            page_list = pages.get(statement_key) or []
            if not page_list:
                print(f"   ⚠️  No pages found for {statement_key}")
                year_data[statement_key] = {}
                continue

            raw_tables = extract_page_tables(pdf_path, page_list)
            parsed = parse_statement(raw_tables, CANONICAL_MAP)
            year_data[statement_key] = parsed

            print(f"   ✓ {statement_key}: {len(parsed)} line items matched")

        all_data[year] = year_data

    return all_data