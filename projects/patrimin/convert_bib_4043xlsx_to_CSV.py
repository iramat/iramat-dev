from pathlib import Path
import re
import pandas as pd

import os

CURRENT_DIR = Path(__file__).parent
INPUT_XLSX = CURRENT_DIR / "BIB 4043.xlsx"
OUTPUT_CSV = INPUT_XLSX.with_suffix(".csv")


def dms_to_decimal(value):
    """
    Convert a coordinate like '21 17 57' to decimal degrees.
    Accepts strings with spaces, commas, dots, or degree-like separators.
    Returns None for empty values.
    """
    if pd.isna(value):
        return None

    text = str(value).strip()
    if not text:
        return None

    # Normalize decimal commas inside seconds if any
    text = text.replace(",", ".")

    # Extract numeric parts, including optional sign and decimals
    parts = re.findall(r"[-+]?\d+(?:\.\d+)?", text)

    if len(parts) < 3:
        raise ValueError(f"Invalid DMS value: {value!r}")

    deg = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])

    sign = -1 if deg < 0 else 1
    deg = abs(deg)

    decimal = deg + minutes / 60 + seconds / 3600
    return sign * decimal


def main():
    # Read Excel as strings to avoid Excel/pandas auto-conversions
    df = pd.read_excel(INPUT_XLSX, dtype=str)

    required_cols = ["x", "y", "num biblio"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required column(s): {', '.join(missing)}")

    # Convert x/y from DMS to decimal degrees
    df["x"] = df["x"].apply(dms_to_decimal)
    df["y"] = df["y"].apply(dms_to_decimal)

    # Replace commas by dots in 'num biblio'
    df["num biblio"] = df["num biblio"].apply(
        lambda v: None if pd.isna(v) else str(v).replace(",", ".")
    )

    # Save to CSV
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print(f"CSV saved to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()