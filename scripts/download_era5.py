"""Tahtalı Barajı için günlük ERA5 verisini Open-Meteo Archive API'den indirir.

Kullanım:
    python scripts/download_era5.py
    python scripts/download_era5.py --start 2014-01-01 --end 2026-09-30 --out data/raw/tahtali_era5_daily.csv

Veri: ERA5 (Copernicus), Open-Meteo üzerinden, CC BY 4.0.
"""

import argparse
from pathlib import Path

import pandas as pd
import requests

API_URL = "https://archive-api.open-meteo.com/v1/archive"

# Baraj koordinatları: İzmir Açık Veri Portalı, izsu-baraj-doluluk-oranlari.csv
TAHTALI_LAT = 38.157434
TAHTALI_LON = 27.122630

DEFAULT_OUT = Path(__file__).resolve().parents[1] / "data" / "raw" / "tahtali_era5_daily.csv"


def fetch_era5(start: str, end: str, lat: float, lon: float) -> pd.DataFrame:
    """Verilen nokta ve tarih aralığı için günlük yağış ve ET0 tablosu döndürür.

    Sütunlar: date (YYYY-MM-DD), precipitation_mm, et0_mm
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "daily": "precipitation_sum,et0_fao_evapotranspiration",
        "timezone": "Europe/Istanbul",
    }
    response = requests.get(API_URL, params=params, timeout=120)
    response.raise_for_status()
    daily = response.json()["daily"]
    return pd.DataFrame(
        {
            "date": daily["time"],
            "precipitation_mm": daily["precipitation_sum"],
            "et0_mm": daily["et0_fao_evapotranspiration"],
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", default="2014-01-01")
    parser.add_argument("--end", default="2026-09-30")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    df = fetch_era5(args.start, args.end, TAHTALI_LAT, TAHTALI_LON)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"{len(df)} gün yazıldı → {args.out}")


if __name__ == "__main__":
    main()
