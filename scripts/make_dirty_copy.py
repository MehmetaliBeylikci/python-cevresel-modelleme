"""Gün 1 için temiz ERA5 verisinin kasıtlı olarak bozulmuş bir kopyasını üretir.

Kullanım:
    python scripts/make_dirty_copy.py

Yapılan bozmalar (data/README.md içinde de belgelenir):
- UNIT_ERROR_YEAR yılında yağış cm cinsinden yazılmış (değerler 10'a bölünmüş)
- 3 negatif yağış ve 2 adet 900 mm/gün değeri (fiziksel olarak imkânsız)
- Günlerin ~%2'si silinmiş
- Tarihlerin ~%10'u `GG.AA.YYYY` biçiminde
- 20 satır birebir tekrarlanmış

Aynı seed her zaman aynı dosyayı üretir.
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
UNIT_ERROR_YEAR = 2019

N_NEGATIVE = 3
N_TOO_LARGE = 2
MISSING_FRACTION = 0.02
DOTTED_DATE_FRACTION = 0.10
N_DUPLICATES = 20


def make_dirty(clean: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """Temiz tabloyu (date, precipitation_mm, et0_mm) bozup yeni bir tablo döndürür."""
    rng = np.random.default_rng(seed)
    df = clean.copy().reset_index(drop=True)
    df["date"] = df["date"].astype(str)

    # 1) Birim hatası: bir yıl boyunca yağış cm olarak yazılmış
    error_year = df["date"].str.startswith(str(UNIT_ERROR_YEAR))
    df.loc[error_year, "precipitation_mm"] = (df.loc[error_year, "precipitation_mm"] / 10).round(2)

    # 2) İmkânsız değerler (birim hatası yılının dışından seçilir)
    candidates = df.index[~error_year]
    impossible = rng.choice(candidates, size=N_NEGATIVE + N_TOO_LARGE, replace=False)
    df.loc[impossible[:N_NEGATIVE], "precipitation_mm"] = -rng.integers(1, 10, N_NEGATIVE).astype(float)
    df.loc[impossible[N_NEGATIVE:], "precipitation_mm"] = 900.0

    # 3) Eksik günler (imkânsız değerli satırlar korunur)
    normal = df.index.difference(impossible)
    n_missing = int(round(len(df) * MISSING_FRACTION))
    df = df.drop(index=rng.choice(normal, size=n_missing, replace=False))

    # 4) Karışık tarih biçimi. Tekrarlardan önce yapılır ki tekrarlanan satırlar birebir aynı kalsın.
    dotted = rng.random(len(df)) < DOTTED_DATE_FRACTION
    dotted_idx = df.index[dotted]
    df.loc[dotted_idx, "date"] = pd.to_datetime(df.loc[dotted_idx, "date"]).dt.strftime("%d.%m.%Y")

    # 5) Tekrarlanan satırlar (imkânsız değerli satırlardan seçilmez)
    normal = df.index.difference(impossible)
    duplicates = df.loc[rng.choice(normal, size=N_DUPLICATES, replace=False)]
    df = pd.concat([df, duplicates])

    # Tekrarlar orijinallerinin hemen yanına gelsin
    return df.sort_index(kind="stable").reset_index(drop=True)


def main() -> None:
    clean = pd.read_csv(RAW / "tahtali_era5_daily.csv")
    dirty = make_dirty(clean)
    out = RAW / "tahtali_era5_daily_kirli.csv"
    dirty.to_csv(out, index=False)
    print(f"{len(dirty)} satır yazıldı → {out}")


if __name__ == "__main__":
    main()
