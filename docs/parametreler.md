# Model Parametreleri ve Kaynakları

`src/model.py` içindeki her sabitin değeri, birimi ve kaynağı. Bu repoda **kaynaksız parametre kullanılmaz**.
Bir değeri değiştirirseniz bu tabloyu da güncelleyin.

| Parametre | Kodda | Değer | Birim | Kaynak | Güvenilirlik |
|---|---|---|---|---|---|
| Normal kottaki göl hacmi | `s_max` | 306,65 | hm³ | [İzmir Açık Veri — Barajların Güncel Doluluk Oranları](https://acikveri.bizizmir.com/dataset/barajlarin-doluluk-oranlari), `MAKSIMUM_SU_KAPASITESI` (erişim 2026-10-23) | Birincil (İZSU) |
| Ölü hacim | `s_min` | 19,6 | hm³ | Aynı dosya, `MINIMUM_SU_KAPASITESI` | Birincil (İZSU) |
| Yağış havzası alanı | `catchment_km2` | 546 | km² | [Yeni Bakış: Tahtalı Barajı hakkında bilinmesi gerekenler](https://www.yenibakishaber.com/izmirde-tahtali-baraji-hakkinda-bilinmesi-gerekenler) (erişim 2026-10-23) | İkincil; DSİ belgesiyle teyit edilemedi |
| Normal kottaki göl alanı | `lake_km2` | 23,52 | km² | Aynı kaynak | İkincil; DSİ belgesiyle teyit edilemedi |
| Su çekimi | `withdrawal` | 10,7 | hm³/ay | Aynı kaynak: "çekilebilecek yıllık ortalama su miktarı 128 milyon m³" → 128 / 12 | İkincil. Bu bir **tasarım değeri**; gerçek çekim farklı olabilir. Aynı haber sitesinde yıllık 205 hm³ de geçiyor; bu değer yalnızca duyarlılık analizinde üst sınır olarak kullanılır. |
| Akış katsayısı | `runoff_coef` | 0,29 | — | **Türetilmiş:** modelin yıllık ortalama girişi, kaynaktaki yıllık ortalama potansiyele (153 hm³) eşit olacak şekilde: C = (153 − P̄·A_göl) / (P̄·A_havza), P̄ = ERA5 2014–2025 ortalama yağışı 836 mm → C = (153 − 19,7) / 456,6 = 0,29 | Türetilmiş. DSİ'nin uzun dönem ortalaması ile ERA5'in 2014–2025 dönemi karşılaştırıldığı için kaba bir tahmin. |
| Açık su buharlaşma katsayısı | `evap_coef` | 1,05 | — | [FAO-56, Tablo 12](https://www.fao.org/4/x0490e/x0490e0b.htm): "Open Water, < 2 m depth or in subhumid climates or tropics", Kc = 1,05 | Birincil kaynak, ama kaba bir seçim: Tahtalı derin bir rezervuar. FAO-56, derin sular için mevsime göre değişen değerler (0,65–1,25) veriyor ve dikkatli kullanılmasını öneriyor. |

## Başlangıç koşulu

| | Değer | Kaynak |
|---|---|---|
| `S0_DATE` | `"2019-09"` (ilk simüle edilen ay) | — |
| `S0_HM3` | 19,6 + 0,76 × (306,65 − 19,6) = 237,76 hm³ | [TRT Haber, 17.08.2023](https://www.trthaber.com/haber/turkiye/tahtali-barajinda-doluluk-son-14-yilin-en-dusuk-seviyesinde-789121.html), İZSU verisi: 2019'un aynı döneminde (ağustos ortası) aktif doluluk %76. Bu değer ağustos sonu depolaması kabul edilir. |

2014–2015 için kaynaklı bir doluluk değeri bulunamadı. Bu yüzden simülasyon 2019'dan başlar. 2014–2019 arası veri Gün 1'de ve iklim karşılaştırmalarında kullanılır.

## Gözlemler (makullük kontrolü)

`data/raw/tahtali_gozlemler.csv` dosyasında bulunur. Her gözlem, tarihine **en yakın ay sonu** model değeriyle karşılaştırılır:

| Gözlem tarihi | Aktif doluluk | Karşılaştırılan model ayı | Kaynak |
|---|---|---|---|
| 2019-08-17 | %76 | (başlangıç koşulu) | TRT Haber / İZSU |
| 2022-08-17 | %50 | 2022-08 | TRT Haber / İZSU |
| 2023-08-17 | %35 | 2023-08 | TRT Haber / İZSU |
| 2025-08-11 | %7,45 | 2025-07 | İzmir Açık Veri, Internet Archive kaydı |
| 2026-10-14 | %42,75 | 2026-09 | İzmir Açık Veri |

## Bilinen durum: model parametrelere çok hassas

Temel parametrelerle model 2022–2025 kuraklığının **derinliğini yakalamaz**; doluluk hiç %37'nin altına inmez. (Aşağıdaki değerler temiz ERA5 verisiyle hesaplandı; Gün 1 çıktısıyla birkaç puan farklı olabilir.)
Küçük değişiklikler ise tabloyu tamamen değiştirir:

| `runoff_coef` | `withdrawal` (hm³/ay) | 2022-08 / 2023-08 / 2025-07 / 2026-09 (%) |
|---|---|---|
| 0,29 | 10,7 | 53 / 51 / 46 / 53 |
| 0,29 | 13 | 24 / 12 / 0 / 6 |
| 0,25 | 10,7 | 35 / 26 / 9 / 7 |
| 0,20 | 8 | 46 / 41 / 29 / 29 |
| Gözlem | | 50 / 35 / 7,45 / 42,75 |

Bu durum bir hata değil, Gün 2'nin ana dersidir: belirsiz parametrelerle kurulan bir modelin sonucu, o parametrelerin belirsizliğinden bağımsız okunamaz.
Olası nedenler: tek bir ERA5 noktasının havza yağışını temsil etmemesi, çekimin tasarım değerinden yüksek olması, sızma ve yeraltı suyu kayıplarının modelde bulunmaması.
