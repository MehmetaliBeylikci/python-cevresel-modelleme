from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"


def load_era5():
    return pd.read_csv(RAW / "tahtali_era5_daily.csv", parse_dates=["date"])


def test_era5_shape():
    df = load_era5()
    assert list(df.columns) == ["date", "precipitation_mm", "et0_mm"]
    assert df["date"].iloc[0] == pd.Timestamp("2014-01-01")
    assert df["date"].iloc[-1] == pd.Timestamp("2026-09-30")
    assert len(df) == 4656
    assert not df["date"].duplicated().any()


def test_era5_values():
    df = load_era5()
    assert not df.isna().any().any()
    assert (df["precipitation_mm"] >= 0).all()
    assert (df["et0_mm"] >= 0).all()
    full_years = df[df["date"].dt.year <= 2025]
    annual = full_years.groupby(full_years["date"].dt.year)["precipitation_mm"].sum()
    assert 300 <= annual.mean() <= 1200


def test_izsu_snapshots():
    for name in ["izsu_baraj_2026-10-14.csv", "izsu_baraj_2025-08-11_wayback.csv"]:
        df = pd.read_csv(RAW / name, sep=";", encoding="utf-8-sig")
        assert "Tahtalı Barajı" in set(df["BARAJ_KUYU_ADI"]), name
    current = pd.read_csv(RAW / "izsu_baraj_2026-10-14.csv", sep=";", encoding="utf-8-sig")
    tahtali = current[current["BARAJ_KUYU_ADI"] == "Tahtalı Barajı"].iloc[0]
    assert tahtali["SU_DURUMU"] == 142323000
    assert tahtali["DOLULUK_ORANI"] == 42.75
