import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from make_dirty_copy import UNIT_ERROR_YEAR, make_dirty  # noqa: E402


@pytest.fixture(scope="module")
def clean():
    return pd.read_csv(ROOT / "data" / "raw" / "tahtali_era5_daily.csv")


@pytest.fixture(scope="module")
def dirty(clean):
    return make_dirty(clean)


def parse_dates(s: pd.Series) -> pd.Series:
    iso = pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")
    dotted = pd.to_datetime(s, format="%d.%m.%Y", errors="coerce")
    return iso.fillna(dotted)


def test_deterministic(clean):
    pd.testing.assert_frame_equal(make_dirty(clean), make_dirty(clean))


def test_missing_days(clean, dirty):
    n_clean = len(clean)
    n_unique = parse_dates(dirty["date"]).nunique()
    missing_ratio = (n_clean - n_unique) / n_clean
    assert 0.015 <= missing_ratio <= 0.025


def test_duplicates(dirty):
    assert dirty.duplicated().sum() == 20


def test_unit_error(clean, dirty):
    assert UNIT_ERROR_YEAR == 2019
    clean_2019 = clean[clean["date"].str.startswith("2019")]["precipitation_mm"].sum()
    d = dirty.assign(date=parse_dates(dirty["date"])).drop_duplicates()
    d = d[(d["precipitation_mm"] >= 0) & (d["precipitation_mm"] < 500)]
    d = d[d["date"].dt.year == 2019]
    clean_same_days = clean[clean["date"].isin(d["date"].dt.strftime("%Y-%m-%d"))]
    ratio = d["precipitation_mm"].sum() / clean_same_days["precipitation_mm"].sum()
    assert ratio == pytest.approx(0.1, rel=0.01)
    assert clean_2019 > 0


def test_impossible_values(dirty):
    unique = dirty.drop_duplicates()
    assert (unique["precipitation_mm"] < 0).sum() == 3
    assert (unique["precipitation_mm"] == 900).sum() == 2


def test_mixed_dates(dirty):
    dotted = dirty["date"].str.match(r"^\d{2}\.\d{2}\.\d{4}$")
    iso = dirty["date"].str.match(r"^\d{4}-\d{2}-\d{2}$")
    assert (dotted | iso).all()
    assert 0.05 <= dotted.mean() <= 0.15


def test_recoverable(clean, dirty):
    d = dirty.assign(date=parse_dates(dirty["date"])).drop_duplicates(subset="date")
    d = d[(d["precipitation_mm"] >= 0) & (d["precipitation_mm"] != 900)].copy()
    in_error_year = d["date"].dt.year == UNIT_ERROR_YEAR
    d.loc[in_error_year, "precipitation_mm"] *= 10
    c = clean.assign(date=pd.to_datetime(clean["date"])).set_index("date")
    d = d.set_index("date").sort_index()
    pd.testing.assert_frame_equal(d, c.loc[d.index], check_exact=False, atol=1e-6)
