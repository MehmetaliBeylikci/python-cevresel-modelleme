# Tasarım: Python ile Çevresel Modelleme — Tahtalı Barajı Su Bütçesi

- **Tarih:** 2026-10-23
- **Hazırlayan:** @mehmetalibeylikci (İYTE Çevre Topluluğu)
- **Durum:** İncelemede
- **Repo:** `github.com/MehmetaliBeylikci/python-cevresel-modelleme` (açık kaynak)

## 1. Amaç ve başarı ölçütleri

İYTE Çevre Topluluğu için 3 günlük bir Python eğitimi. Eğitim, tek bir case study üzerinden çevresel modellemenin üç adımını öğretir: **veri hazırlama → model kurulumu → görselleştirme**.

**Hedef kitle:** Karışık bir grup. Bazı katılımcılar temel Python biliyor, bazıları hiç kod yazmamış. Seviye: başlangıçtan biraz ileri.

**Kısıtlar**
- Her gün 2 saat, toplam 6 saat ders.
- Ortam: Google Colab (kurulum yok). Yerel kurulum yalnızca yedek seçenek olarak destekleniyor.
- Tüm materyal GitHub'da açık kaynak; dışarıdan katkıya açık.

**Başarı ölçütleri**
1. Eğitimi tamamlayan bir katılımcı, kendi zaman serisi verisiyle benzer bir kütle dengesi modelini tek başına kurabilir: veriyi okur, temizler, toplulaştırır, modeli yazar, senaryoları karşılaştırıp grafiğe döker.
2. Hiç kod yazmamış bir katılımcı, Gün 0'ı tamamladıktan sonra her günün temel alıştırmalarını bitirebilir.
3. Tüm notebook'lar Colab'da tek tıkla açılır ve "Run all" ile hatasız çalışır. Bu, CI tarafından her push'ta doğrulanır.
4. Dışarıdan biri, yalnızca `CONTRIBUTING.md` dosyasını okuyarak yeni bir alıştırma ya da bonus modül ekleyebilir.

## 2. Case study: Tahtalı Barajı su bütçesi

**Neden bu konu:** Tahtalı, İzmir'in yüzey su kaynakları arasında kapasitesi en büyük baraj. 2025'te neredeyse tamamen boşaldı, 2026'da toparlandı. Yerel, güncel ve çevre topluluğu için motive edici bir konu.

### 2.1 Model

Aylık zaman adımlı, tek kutulu ("kova") bir kütle dengesi modeli:

```
S[t+1] = clip( S[t] + Q_in − E − W , S_min , S_max )

Q_in = C · P · A_havza          # havzadan gelen akış
     + P · A_göl                # göle doğrudan düşen yağış
E    = k_E · ET0 · A_göl        # göl yüzeyinden buharlaşma
taşma = S[t] + Q_in − E − W − S_max   (pozitifse; dolusavaktan çıkan su olarak raporlanır)
```

Birim dönüşümü: 1 mm × 1 km² = 0,001 hm³. Bu dönüşüm Gün 2'de açıkça işlenir.

| Sembol | Anlam | Değer | Kaynak |
|---|---|---|---|
| `S_maks` | Normal kottaki göl hacmi | 306,65 hm³ | İzmir Açık Veri CSV (`MAKSIMUM_SU_KAPASITESI`) |
| `S_min` | Ölü hacim | 19,6 hm³ | İzmir Açık Veri CSV (`MINIMUM_SU_KAPASITESI`) |
| `A_havza` | Yağış havzası alanı | 546 km² | İkincil kaynak; uygulamada birincil kaynakla (DSİ/İZSU) teyit edilir |
| `A_göl` | Normal kottaki göl alanı | 23,52 km² | İkincil kaynak; uygulamada teyit edilir |
| `W` | Aylık su çekimi | Temel değer 10,7 hm³/ay (yıllık 128 hm³) | Kaynaklarda yıllık 128–205 hm³ arasında çelişkili değerler var. Bu belirsizlik duyarlılık analizinin girdisi olur |
| `C` | Akış katsayısı | Temel değer 0,29 | Modelin yıllık ortalama girişi (havza akışı + göle düşen yağış) yıllık potansiyele (153 hm³) eşit olacak şekilde ERA5 ortalama yağışından türetildi; ayrıntı `docs/parametreler.md` |
| `k_E` | Açık su buharlaşma katsayısı (ET0 → göl) | 1,05 | FAO-56 Tablo 12 (açık su, yarı nemli iklim) |
| `S[0]` | Başlangıç depolaması | 237,76 hm³ (ağustos 2019 sonu, %76) | TRT Haber / İZSU verisi; 2014–2015 için kaynaklı değer bulunamadığından simülasyon 2019-09'da başlar |

**Kurallar**
- Kaynaksız parametre kullanılmaz. Her değer, kaynağıyla birlikte `docs/parametreler.md` dosyasına yazılır.
- Tabloda "teyit edilir" denen değerler uygulamanın ilk adımında kontrol edilir. Değer değişirse yalnızca `docs/parametreler.md` ve `src/model.py` güncellenir.

**Kalibrasyon yapılmıyor.** Tahtalı'nın geçmiş doluluk serisi açık bir kaynakta bulunmuyor. Kontrol edilenler: İzmir açık veri CSV'si yalnızca anlık durumu veriyor; Internet Archive'da bu dosyanın tek bir kaydı var. Kalibrasyonun yerini iki şey alıyor:
1. **Makullük kontrolü:** model, iki gerçek gözlemle karşılaştırılır. Bunlar Wayback Machine'deki kayıt (2 Eylül 2025'te arşivlenmiş, durum tarihi 11 Ağustos 2025: 40,98 hm³, %7,45) ve 14 Ekim 2026 tarihli güncel CSV (142,32 hm³, %42,75).
2. **Duyarlılık analizi:** `C` ve `W` için parametre taraması yapılır.

**Bilinçli olarak dışarıda bırakılanlar:** günlük zaman adımı, kar ve yeraltı suyu, birden fazla baraj, kalibrasyon/optimizasyon.

Depolamaya bağlı göl alanı (`A_göl = f(S)`) Gün 2'de ileri seviye bir alıştırma olarak yer alıyor; temel model sabit alanla çalışıyor.

### 2.2 Veri

| Dosya | İçerik | Kaynak / lisans |
|---|---|---|
| `data/raw/tahtali_era5_daily.csv` | 2014-01-01 → 2026-09-30 arası günlük `precipitation_sum` (mm) ve `et0_fao_evapotranspiration` (mm) | Open-Meteo Archive API (ERA5), CC BY 4.0. Koordinat: baraj (38.157434, 27.122630, İzmir Açık Veri CSV'sinden) |
| `data/raw/tahtali_era5_daily_kirli.csv` | Yukarıdaki dosyanın **eğitim için kasıtlı olarak bozulmuş** kopyası | `scripts/make_dirty_copy.py` ile, sabit seed kullanılarak üretiliyor |
| `data/raw/izsu_baraj_2026-10-14.csv` | İzmir barajlarının anlık durumu (sabitler + kontrol noktası) | İzmir Açık Veri Portalı, İBB Açık Veri Lisansı |
| `data/raw/izsu_baraj_2025-08-11_wayback.csv` | Aynı dosyanın Internet Archive kaydı (kontrol noktası) | web.archive.org kaydı, kaynak lisansı aynı |
| `data/processed/tahtali_monthly.csv` | Gün 1'in beklenen çıktısı (Gün 2 için yedek) | Türetilmiş veri |

**Kirli kopyada yapılan bozmalar** (hepsi `data/README.md` dosyasında belgeleniyor):
- ~%2 oranında rastgele silinmiş günler
- ~20 tekrarlanan satır
- Bir yıllık blokta yağış mm yerine cm olarak yazılmış (birim hatası)
- Birkaç fiziksel olarak imkânsız değer (negatif yağış, 900 mm/gün)
- Tarih sütununda karışık format (`2019-03-05` ve `05.03.2019`)

Ham veriler repoya dahil ediliyor. Böylece ders günü internet ya da API erişimine gerek kalmıyor. `scripts/download_era5.py` aynı veriyi yeniden indirebiliyor.

## 3. Ders akışı

**Ortak yapı:** Her gün için tek bir notebook var. Akış şöyle: kısa anlatım → birlikte canlı kodlama → alıştırmalar.
- Alıştırmalar (temel) ve (ileri) olarak işaretleniyor.
- Her notebook'ta bir **"Zaman kalırsa"** bölümü var; atlandığında akış bozulmuyor.
- Her gün, bir önceki günün çıktısını (`data/processed/` ve `src/model.py`) kullanarak başlıyor. Böylece bir günü kaçıran katılımcı da devam edebiliyor.

### Gün 0 — Ön hazırlık (ders öncesi, kendi başına, ~1 saat)
`00_on_hazirlik.ipynb` içeriği:
- Colab'ı kullanmak
- Değişkenler, listeler, sözlükler, `for`/`if`, fonksiyonlar
- f-string ile çıktı yazdırmak

Sonunda 5 soruluk bir "Hazır mıyım?" kontrolü var.

### Gün 1 — Veri hazırlama (120 dk) · `01_veri_hazirlama.ipynb`
| Süre | Konu |
|---|---|
| 0–15 | Problem: İzmir su krizi ve Tahtalı. **folium** ile baraj haritası. Colab turu |
| 15–45 | pandas temelleri: `read_csv`, `head`/`info`/`describe`, tarih sütunu, `DatetimeIndex` |
| 45–55 | **Sweetviz** ile otomatik keşif raporu (demo): "Raporun gösterdiği sorunları şimdi tek tek bulup düzelteceğiz" |
| 55–90 | Temizlik: tarih formatlarını birleştirme, tekrarları silme, imkânsız değerler, birim hatasını bulma (yıllık toplam grafiği), eksik günleri bulma ve doldurma |
| 90–105 | Günlükten aylığa `resample`: yağış ve ET0 için neden `sum`, sıcaklık için neden `mean` |
| 105–120 | İlk grafik + alıştırma. **Çıktı:** `tahtali_monthly.csv` |

### Gün 2 — Model kurulumu (120 dk) · `02_model_kurulumu.ipynb`
| Süre | Konu |
|---|---|
| 0–15 | Kavramsal model: kova çizimi, kütle korunumu, birim dönüşümü |
| 15–50 | Modeli fonksiyon olarak yazma: girdiler, döngü, `S_min`/`S_maks` sınırları, taşma |
| 50–70 | Modeli çalıştırma; iki gerçek gözlemle karşılaştırma ("makul mü?") |
| 70–100 | Duyarlılık analizi: `C` × `W` parametre taraması, sonuç tablosu. **ipywidgets** kaydırma çubuklarıyla interaktif keşif |
| 100–120 | Alıştırma + modelin varsayımları üzerine tartışma. Fonksiyonun hâli `src/model.py` dosyasına aktarılır |

### Gün 3 — Görselleştirme ve senaryolar (120 dk) · `03_gorsellestirme_senaryolar.ipynb`
| Süre | Konu |
|---|---|
| 0–30 | matplotlib anatomisi (`fig`/`ax`). Kötü bir grafiği adım adım düzeltmek |
| 30–70 | Senaryolar: yağış −%20, ET0 +%10, talep +%15. Metrik: kritik seviyenin (%10 aktif doluluk) altında geçen ay sayısı |
| 70–100 | Sunuma hazır figür: çok panelli grafik, **seaborn** ile mevsimsel ısı haritası, `savefig`. Senaryo grafiğinin **plotly** ile interaktif hâli |
| 100–120 | Kapanış: modelin sınırları; sıradaki adımlar (**xarray**/NetCDF, bonus modül). Herkes kendi senaryosunu kurup paylaşır |

### Bonus — Fizik mi, veri mi? (kendi başına, ders dışı)
`bonus/fizik-mi-veri-mi/` klasöründe, ana akıştan tamamen ayrı bir modül:
1. scikit-learn ile bir Random Forest eğitilir: aylık `P`, `ET0` ve ayın kendisi → modelin hesapladığı aylık depolama değişimi `ΔS`.
2. Random Forest'ın tahmini, kova modeliyle karşılaştırılır.
3. **SHAP** ile "model neye bakıyor?" sorusu sorulur.

Gözlem serisi olmadığı için hedef değişken, kova modelinin çıktısıdır. Bu durum notebook'ta açıkça belirtiliyor ve tartışma sorusuna dönüştürülüyor: "ML modeli fiziği yeniden keşfedebilir mi? Gerçek gözlem olsaydı ne değişirdi?"

PyCaret ve diğer AutoML araçları kapanışta yalnızca bir paragrafla anılıyor.

## 4. Repo yapısı

```
python-cevresel-modelleme/
├── README.md                  # Türkçe: amaç, program, Colab rozetleri, yerel kurulum, kaynaklar
├── LICENSE                    # MIT (kod)
├── LICENSE-CONTENT.md         # CC BY 4.0 (ders metinleri ve figürler)
├── CONTRIBUTING.md            # katkı rehberi, notebook yazım kuralları, yeni modül ekleme
├── CODE_OF_CONDUCT.md         # Contributor Covenant (Türkçe)
├── CITATION.cff
├── requirements.txt           # ana ders: pandas, numpy, matplotlib, seaborn, plotly, ipywidgets, folium, sweetviz
├── .pre-commit-config.yaml    # nbstripout: notebook çıktıları commit'ten önce temizlenir
├── notebooks/                 # boşluklu katılımcı notebook'ları (00–03)
├── cozumler/                  # çözümlü notebook'lar (00–03)
├── src/model.py               # su bütçesi fonksiyonu + parametre sabitleri
├── data/{README.md, raw/, processed/}
├── scripts/{download_era5.py, make_dirty_copy.py}
├── docs/{egitmen_notlari.md, parametreler.md, superpowers/specs/}
├── bonus/fizik-mi-veri-mi/{README.md, fizik_mi_veri_mi.ipynb, cozum.ipynb, requirements.txt}
└── .github/
    ├── workflows/test.yml     # çözüm + bonus notebook'ları çalıştırır; katılımcı notebook'larını sözdizimi kontrolünden geçirir
    ├── ISSUE_TEMPLATE/{hata.yml, icerik-onerisi.yml}
    └── pull_request_template.md
```

**Kararlar**
- **Colab kurulum hücresi:** Her notebook'un ilk hücresi, Colab'da çalıştığını algılarsa repoyu klonlayıp çalışma dizinine geçiyor; yerelde hiçbir şey yapmıyor. Gerekirse eksik paketleri `pip install -q` ile kuruyor (Sweetviz gibi). Repo adresi bu hücrede ve README'de geçiyor; adres değişirse yalnızca bu iki yer güncelleniyor.
- **Dil:** Anlatım ve yorumlar Türkçe. Değişken ve fonksiyon isimleri İngilizce (`storage`, `runoff_coef`). Gün 1'de kısa bir terim sözlüğü veriliyor.
- **Çözüm ve katılımcı notebook'ları:** İki ayrı dosya olarak tutuluyor. Katılımcı notebook'unda boşluklar `# TODO:` yorumu ve `...` ile işaretleniyor.
- **Bağımlılıklar:** Bonus modülün bağımlılıkları (scikit-learn, shap) kendi `requirements.txt` dosyasında duruyor; ana derse yük getirmiyor.
- **Sweetviz uyumluluğu:** Uygulamanın ilk adımında Colab'ın güncel ortamında denenir. Uyumsuzsa yerine `ydata-profiling` kullanılır ve spec'in bu satırı güncellenir.

## 5. Kalite ve test

- **CI (GitHub Actions, Python 3.12):** `cozumler/*.ipynb` ve `bonus/*/cozum.ipynb` dosyaları `nbconvert --execute` ile baştan sona çalıştırılır. Katılımcı notebook'ları çalıştırılmaz; yalnızca JSON ve Python sözdizimi geçerliliği kontrol edilir. Boşlukları işaretleyen `...` geçerli bir Python ifadesi olduğu için bu kontrolden geçer.
- **`src/model.py` için birkaç assert tabanlı kontrol:** sıfır yağış ve sıfır çekimde hacim değişmez; çıktı her zaman `[S_min, S_maks]` aralığında kalır; kütle dengesi kapanır. CI'da çalıştırılır.
- **Kirli kopya tekrarlanabilir:** sabit seed sayesinde script her çalıştırıldığında aynı dosyayı üretir.
- **Eğitmen provası:** Her notebook, ders öncesi gerçek bir Colab oturumunda süre tutularak denenir. Bulgular `docs/egitmen_notlari.md` dosyasına yazılır.

## 6. Kapsam dışı

Web sitesi veya Jupyter Book, Python paketi olarak dağıtım, İngilizce çeviri, video kayıtları, birden fazla case study. Bunlar ileride katkı olarak eklenebilir; `CONTRIBUTING.md` bu yolu tarif ediyor.
