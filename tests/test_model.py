import dataclasses
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.model import S0_DATE, S0_HM3, Params, active_fill_pct, simulate  # noqa: E402

P = Params()
MONTHS = pd.date_range("2020-01-01", periods=12, freq="MS")


def series(value):
    return pd.Series(value, index=MONTHS, dtype=float)


def test_no_forcing_no_change():
    params = dataclasses.replace(P, withdrawal=0.0)
    out = simulate(series(0), series(0), s0=150.0, params=params)
    assert np.allclose(out["storage"], 150.0)


def test_bounds():
    rng = np.random.default_rng(42)
    precip = pd.Series(rng.uniform(0, 400, 12), index=MONTHS)
    et0 = pd.Series(rng.uniform(0, 200, 12), index=MONTHS)
    out = simulate(precip, et0, s0=150.0)
    assert (out["storage"] >= P.s_min - 1e-9).all()
    assert (out["storage"] <= P.s_max + 1e-9).all()


def test_spill_when_full():
    out = simulate(series(300), series(0), s0=P.s_max)
    assert out["spill"].iloc[0] > 0
    assert out["storage"].iloc[0] == pytest.approx(P.s_max)


def test_shortfall_when_dry():
    out = simulate(series(0), series(0), s0=P.s_min + 5)
    assert out["shortfall"].iloc[0] > 0
    assert out["storage"].iloc[0] == pytest.approx(P.s_min)


def test_mass_balance_closes():
    rng = np.random.default_rng(42)
    precip = pd.Series(rng.uniform(0, 400, 12), index=MONTHS)
    et0 = pd.Series(rng.uniform(0, 200, 12), index=MONTHS)
    s0 = 100.0
    out = simulate(precip, et0, s0=s0)
    previous = pd.concat([pd.Series([s0]), out["storage"].iloc[:-1].reset_index(drop=True)])
    delta = out["storage"].to_numpy() - previous.to_numpy()
    budget = out["inflow"] - out["evaporation"] - out["withdrawal"] - out["spill"]
    assert np.allclose(delta, budget.to_numpy(), atol=1e-9)


def test_unit_conversion():
    params = dataclasses.replace(P, runoff_coef=0.25, withdrawal=0.0)
    out = simulate(series(100), series(0), s0=100.0, params=params)
    expected = 0.25 * 100 * 546 * 0.001 + 100 * 23.52 * 0.001
    assert out["inflow"].iloc[0] == pytest.approx(expected)


def test_active_fill_pct():
    assert active_fill_pct(142.323) == pytest.approx(42.75, abs=0.01)
    assert active_fill_pct(P.s_min) == pytest.approx(0.0)
    assert active_fill_pct(P.s_max) == pytest.approx(100.0)
    s = active_fill_pct(pd.Series([P.s_min, P.s_max]))
    assert list(s.round(6)) == [0.0, 100.0]


def test_rejects_misaligned_or_nan():
    other_index = pd.Series(0.0, index=pd.date_range("2021-01-01", periods=12, freq="MS"))
    with pytest.raises(ValueError, match="indeks"):
        simulate(series(10), other_index, s0=100.0)
    with_nan = series(10)
    with_nan.iloc[3] = np.nan
    with pytest.raises(ValueError, match="eksik"):
        simulate(with_nan, series(0), s0=100.0)


def test_s0_matches_observation():
    obs = pd.read_csv(ROOT / "data" / "raw" / "tahtali_gozlemler.csv", parse_dates=["date"])
    first = obs.iloc[0]
    assert S0_DATE == "2019-09"
    assert first["date"] == pd.Timestamp("2019-08-17")
    assert active_fill_pct(S0_HM3) == pytest.approx(first["active_fill_pct"], abs=0.01)


def test_runoff_coef_matches_annual_potential():
    """C, havzadan + göle düşen yağışla gelen yıllık suyun 153 hm³ potansiyele eşit olacağı şekilde türetilir."""
    clean = pd.read_csv(ROOT / "data" / "raw" / "tahtali_era5_daily.csv", parse_dates=["date"])
    full_years = clean[clean["date"].dt.year <= 2025]
    mean_annual_precip = full_years.groupby(full_years["date"].dt.year)["precipitation_mm"].sum().mean()
    annual_inflow = (P.runoff_coef * P.catchment_km2 + P.lake_km2) * mean_annual_precip * 0.001
    assert annual_inflow == pytest.approx(153, rel=0.02)


def test_rejects_invalid_s0_and_negative_inputs():
    with pytest.raises(ValueError, match="s0"):
        simulate(series(0), series(0), s0=5.0)
    with pytest.raises(ValueError, match="s0"):
        simulate(series(0), series(0), s0=P.s_max + 1)
    with pytest.raises(ValueError, match="negatif"):
        simulate(series(-1), series(0), s0=100.0)
