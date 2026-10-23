"""Tahtalı Barajı için aylık "kova" su bütçesi modeli.

    S[t+1] = S[t] + Q_in − E − W        (S_min ile S_max arasında)
    Q_in   = C · P · A_havza + P · A_göl
    E      = k_E · ET0 · A_göl

Birim dönüşümü: 1 mm × 1 km² = 0,001 hm³.
Her sabitin kaynağı için: docs/parametreler.md
"""

from dataclasses import dataclass

import pandas as pd

MM_KM2_TO_HM3 = 0.001

# Simülasyonun başlangıcı: 17.08.2019 gözlemi (%76 aktif doluluk) ağustos sonu
# depolaması kabul edilir; ilk simüle edilen ay eylül 2019'dur.
S0_DATE = "2019-09"
S0_HM3 = 19.6 + 0.76 * (306.65 - 19.6)


@dataclass(frozen=True)
class Params:
    """Model parametreleri. Değiştirmek için: dataclasses.replace(Params(), runoff_coef=0.2)"""

    catchment_km2: float = 546.0   # yağış havzası alanı
    lake_km2: float = 23.52        # normal kottaki göl alanı
    s_max: float = 306.65          # hm³, normal kottaki göl hacmi
    s_min: float = 19.6            # hm³, ölü hacim
    runoff_coef: float = 0.29      # akış katsayısı C
    evap_coef: float = 1.05        # açık su katsayısı k_E (FAO-56)
    withdrawal: float = 10.7       # hm³/ay, İZSU'nun çektiği su


def simulate(precip_mm: pd.Series, et0_mm: pd.Series, s0: float,
             params: Params = Params()) -> pd.DataFrame:
    """Aylık yağış ve ET0 serilerinden baraj depolamasını hesaplar.

    precip_mm, et0_mm: aynı aylık indekse sahip seriler (mm/ay)
    s0: ilk ayın başındaki depolama (hm³)

    Dönen tablo (hepsi hm³, girdilerle aynı indeks):
        storage     ay sonundaki depolama
        inflow      havzadan gelen akış + göle düşen yağış
        evaporation göl yüzeyinden buharlaşma
        withdrawal  gerçekleşen su çekimi
        spill       dolusavaktan taşan su
        shortfall   baraj ölü hacme indiği için karşılanamayan çekim
    """
    if not precip_mm.index.equals(et0_mm.index):
        raise ValueError("Yağış ve ET0 serilerinin indeksleri aynı olmalı (aynı aylar, aynı sıra).")
    if precip_mm.isna().any() or et0_mm.isna().any():
        raise ValueError("Girdilerde eksik (NaN) değer var; önce veriyi temizleyin.")
    if (precip_mm < 0).any() or (et0_mm < 0).any():
        raise ValueError("Yağış ve ET0 negatif olamaz; önce veriyi temizleyin.")

    p = params
    if not p.s_min <= s0 <= p.s_max:
        raise ValueError(f"s0 = {s0} hm³, ölü hacim ({p.s_min}) ile en büyük hacim ({p.s_max}) arasında olmalı.")
    rows = []
    storage = s0
    for precip, et0 in zip(precip_mm, et0_mm):
        inflow = (p.runoff_coef * precip * p.catchment_km2 + precip * p.lake_km2) * MM_KM2_TO_HM3
        evaporation = p.evap_coef * et0 * p.lake_km2 * MM_KM2_TO_HM3
        withdrawal = p.withdrawal
        spill = 0.0
        shortfall = 0.0

        storage = storage + inflow - evaporation - withdrawal
        if storage > p.s_max:
            spill = storage - p.s_max
            storage = p.s_max
        elif storage < p.s_min:
            deficit = p.s_min - storage
            # Önce çekim kısılır; o da yetmezse buharlaşma ölü hacimden karşılanmaz.
            shortfall = min(deficit, withdrawal)
            withdrawal -= shortfall
            evaporation -= deficit - shortfall
            storage = p.s_min

        rows.append((storage, inflow, evaporation, withdrawal, spill, shortfall))

    columns = ["storage", "inflow", "evaporation", "withdrawal", "spill", "shortfall"]
    return pd.DataFrame(rows, index=precip_mm.index, columns=columns)


def active_fill_pct(storage, params: Params = Params()):
    """Aktif doluluk oranı (%): (S − S_min) / (S_max − S_min) × 100. İZSU'nun yayımladığı oran budur."""
    return (storage - params.s_min) / (params.s_max - params.s_min) * 100
