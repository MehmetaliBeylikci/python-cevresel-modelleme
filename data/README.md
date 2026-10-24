# Veri

Ders sırasında internete ya da bir API'ye ihtiyaç kalmasın diye tüm ham veriler bu klasörde duruyor.

## `raw/tahtali_era5_daily.csv`

Tahtalı Barajı noktası için günlük meteoroloji verisi.

| Sütun | Birim | Açıklama |
|---|---|---|
| `date` | — | Tarih, `YYYY-MM-DD` (Europe/Istanbul saat dilimine göre gün) |
| `precipitation_mm` | mm/gün | Günlük toplam yağış (`precipitation_sum`) |
| `et0_mm` | mm/gün | FAO-56 Penman-Monteith referans evapotranspirasyon (`et0_fao_evapotranspiration`) |

- **Kapsam:** 2014-01-01 → 2026-09-30 (4656 gün)
- **Konum:** 38.157434 K, 27.122630 D (barajın koordinatı, İZSU CSV'sinden)
- **Kaynak:** [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), ERA5 reanaliz verisi (Copernicus Climate Change Service)
- **Lisans:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Atıf: *Weather data by Open-Meteo.com*; Hersbach, H. et al. (2023): ERA5 hourly data on single levels from 1940 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS), DOI: 10.24381/cds.adbb2d47
- **İndirme tarihi:** 2026-10-23
- **Yeniden indirmek için:** `python scripts/download_era5.py`

> ERA5 yaklaşık 25 km çözünürlüklü bir reanaliz ürünüdür. Bu nedenle tek bir noktanın değeri, havzanın tamamındaki yağışı yalnızca yaklaşık olarak temsil eder. Modelin varsayımları arasında bunu da tartışıyoruz.

## `raw/tahtali_era5_daily_kirli.csv`

> **Bu dosya eğitim için kasıtlı olarak bozulmuştur. Analizde kullanmayın.** Gün 1'de bu dosyayı temizlemeyi öğreniyoruz.

`tahtali_era5_daily.csv` dosyasından `python scripts/make_dirty_copy.py` ile üretilir (seed = 42, her seferinde aynı dosya).

| Bozma | Ayrıntı | Gün 1'de nasıl bulunur? |
|---|---|---|
| Karışık tarih biçimi | Satırların ~%10'unda tarih `GG.AA.YYYY` biçiminde | `pd.to_datetime` hata verir ya da `NaT` üretir |
| Tekrarlanan satırlar | 20 satır birebir tekrar | `df.duplicated()` |
| İmkânsız değerler | 3 negatif yağış, 2 adet 900 mm/gün | `describe()`, kutu grafiği |
| Birim hatası | 2019 yılında yağış cm cinsinden yazılmış (10'a bölünmüş) | Yıllık toplam çubuk grafiğinde 2019 aykırı görünür |
| Eksik günler | Günlerin ~%2'si silinmiş | Tam tarih aralığıyla karşılaştırma (`reindex`) |

## `raw/izsu_baraj_2026-10-14.csv`

İzmir barajlarının 14 Ekim 2026 tarihli anlık durumu. Kullanım amacı iki:

1. Tahtalı'nın sabitleri: maksimum hacim 306,65 hm³ ve minimum (ölü) hacim 19,6 hm³
2. Makullük kontrolü için gerçek bir gözlem: 142,32 hm³, %42,75 aktif doluluk

- **Kaynak:** [İzmir Büyükşehir Belediyesi Açık Veri Portalı — Barajların Güncel Doluluk Oranları](https://acikveri.bizizmir.com/dataset/barajlarin-doluluk-oranlari) (veri sahibi: İZSU)
- **Doğrudan dosya:** `https://openfiles.izmir.bel.tr/309436/docs/izsu-baraj-doluluk-oranlari.csv`
- **Lisans:** [İzmir Büyükşehir Belediyesi Açık Veri Lisansı](https://acikveri.bizizmir.com/en/license). Veri, kaynak belirtilerek kopyalanabilir, değiştirilebilir ve ticari amaçla da dağıtılabilir. Bu repo veriyi bu koşulla yeniden dağıtır.
- **Biçim:** `;` ile ayrılmış, UTF-8 (BOM'lu). Okumak için: `pd.read_csv(path, sep=";", encoding="utf-8-sig")`

Önemli sütunlar: `SU_DURUMU` (göldeki su, m³), `DOLULUK_ORANI` (aktif doluluk, %), `MAKSIMUM_SU_KAPASITESI` / `MINIMUM_SU_KAPASITESI` (m³), `ENLEM` / `BOYLAM`.

**Aktif doluluk:** `(SU_DURUMU − MINIMUM) / (MAKSIMUM − MINIMUM) × 100`.
Örnek: (142,323 − 19,6) / (306,65 − 19,6) × 100 = %42,75.

## `raw/izsu_baraj_2025-08-11_wayback.csv`

Aynı dosyanın [Internet Archive](https://web.archive.org/web/20250902152857/https://openfiles.izmir.bel.tr/309436/docs/izsu-baraj-doluluk-oranlari.csv) kaydı.

- **Arşivlenme tarihi:** 2025-09-02
- **İçindeki durum tarihi:** 2025-08-11
- **Tahtalı:** 40,98 hm³, %7,45 aktif doluluk (2025 kuraklığı)

Bu kayıtta `ENLEM` ve `BOYLAM` sütunları boştur. Lisansı kaynak dosyayla aynıdır.

## `processed/tahtali_monthly.csv`

Gün 1 notebook'unun çıktısı: temizlenmiş **aylık** yağış ve ET0 toplamları. Gün 1'i atlayan ya da tamamlayamayan katılımcılar Gün 2'ye bu dosyayla başlayabilir.

| Sütun | Birim | Açıklama |
|---|---|---|
| `month` | — | Ay, `YYYY-MM` |
| `precipitation_mm` | mm/ay | Aylık toplam yağış |
| `et0_mm` | mm/ay | Aylık toplam ET0 |

- **Kapsam:** 2014-01 → 2026-09 (153 ay)
- Kirli kopyanın temizlenmesiyle üretildiği için orijinal veriden biraz farklıdır: toplam yağış farkı %0,9; tek bir ayda en fazla ~29 mm.

## `raw/tahtali_gozlemler.csv`

Modelin makullük kontrolü için kullanılan, kaynaklı Tahtalı doluluk gözlemleri. Sütunlar: `date`, `active_fill_pct` (%), `storage_hm3` (varsa), `source`. Ayrıntılar: [docs/parametreler.md](../docs/parametreler.md).
