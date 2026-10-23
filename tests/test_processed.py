from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"


def test_processed_matches_clean():
    monthly = pd.read_csv(DATA / "processed" / "tahtali_monthly.csv")
    assert list(monthly.columns) == ["month", "precipitation_mm", "et0_mm"]
    assert len(monthly) == 153
    assert monthly["month"].iloc[0] == "2014-01"
    assert monthly["month"].iloc[-1] == "2026-09"

    clean = pd.read_csv(DATA / "raw" / "tahtali_era5_daily.csv", parse_dates=["date"])
    expected = clean.set_index("date").resample("MS").sum()
    for col in ["precipitation_mm", "et0_mm"]:
        got = monthly[col].to_numpy()
        want = expected[col].to_numpy()
        # Eksik günler interpolasyonla doldurulduğu için birebir eşleşme beklenmez. Toplam ±%1 içinde olmalı.
        # Ay bazında: ET0 düzgün değiştiği için ≤3 mm; yağışta ise silinmiş yağmurlu bir gün geri
        # getirilemez, bu yüzden ≤35 mm (ölçülen en büyük fark ~29 mm).
        assert abs(got.sum() - want.sum()) / want.sum() < 0.01, col
        per_month_limit = 3 if col == "et0_mm" else 35
        assert (abs(got - want) <= per_month_limit).all(), col
