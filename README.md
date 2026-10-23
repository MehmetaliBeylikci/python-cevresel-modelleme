# Python ile Çevresel Modelleme: Tahtalı Barajı Su Bütçesi

[![Testler](https://github.com/mehmetalibeylikci/python-cevresel-modelleme/actions/workflows/test.yml/badge.svg)](https://github.com/mehmetalibeylikci/python-cevresel-modelleme/actions/workflows/test.yml)
[![Kod: MIT](https://img.shields.io/badge/kod-MIT-blue.svg)](LICENSE)
[![İçerik: CC BY 4.0](https://img.shields.io/badge/i%C3%A7erik-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENT.md)

İYTE Çevre Topluluğu için hazırlanmış, **3 günlük, açık kaynak** bir Python eğitimi.

İzmir'in en büyük içme suyu kaynağı **Tahtalı Barajı** 2025 yazında neredeyse tamamen boşaldı ve 2026'da yeniden doldu. Bu eğitimde barajın aylık su bütçesini modelleyerek çevresel modellemenin üç temel adımını uyguluyoruz:

**veri hazırlama → model kurulumu → görselleştirme ve senaryolar**

## Kimler için?

Başlangıç seviyesinin biraz üzerindeki katılımcılar için tasarlandı. Hiç kod yazmamış olanlar **Gün 0**'ı tamamlayarak katılabilir. Alıştırmalar iki seviyeli: 🟢 temel, 🔵 ileri.

Kurulum gerekmez: her şey tarayıcıda, **Google Colab**'da çalışır.

## Program

| Gün | Konu | Süre | Notebook |
|---|---|---|---|
| 0 | **Ön hazırlık:** değişkenler, listeler, döngüler, fonksiyonlar | ~1 saat, kendi başına | [![Colab'da aç](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mehmetalibeylikci/python-cevresel-modelleme/blob/main/notebooks/00_on_hazirlik.ipynb) |
| 1 | **Veri hazırlama:** pandas, Sweetviz, kirli veriyi temizleme, `resample` | 2 saat | [![Colab'da aç](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mehmetalibeylikci/python-cevresel-modelleme/blob/main/notebooks/01_veri_hazirlama.ipynb) |
| 2 | **Model kurulumu:** kütle korunumu, modeli fonksiyon olarak yazma, duyarlılık analizi, ipywidgets | 2 saat | [![Colab'da aç](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mehmetalibeylikci/python-cevresel-modelleme/blob/main/notebooks/02_model_kurulumu.ipynb) |
| 3 | **Görselleştirme ve senaryolar:** matplotlib, seaborn, plotly, iklim ve talep senaryoları | 2 saat | [![Colab'da aç](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mehmetalibeylikci/python-cevresel-modelleme/blob/main/notebooks/03_gorsellestirme_senaryolar.ipynb) |

Çözümlü sürümler [`cozumler/`](cozumler/) klasöründe.

### Bonus modüller

| Modül | Konu | Notebook |
|---|---|---|
| [Fizik mi, veri mi?](bonus/fizik-mi-veri-mi/) | Aynı problemi scikit-learn (Random Forest) ile çözmek ve SHAP ile yorumlamak | [![Colab'da aç](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mehmetalibeylikci/python-cevresel-modelleme/blob/main/bonus/fizik-mi-veri-mi/fizik_mi_veri_mi.ipynb) |

## Model

Baraj, aylık adımlarla çalışan bir "kova" olarak modelleniyor:

$$S_{t+1} = S_t + C \cdot P \cdot A_{havza} + P \cdot A_{göl} - k_E \cdot ET_0 \cdot A_{göl} - W$$

Depolama, ölü hacim (19,6 hm³) ile normal kottaki hacim (306,65 hm³) arasında sınırlı. Kodu [`src/model.py`](src/model.py), parametreler ve kaynakları [`docs/parametreler.md`](docs/parametreler.md) dosyasında.

> **Eğitimin önemli bir dersi:** Kaynaklardan alınan parametrelerle model, 2022–2025 kuraklığını yakalayamıyor ve sonuç parametrelere son derece hassas. Gün 2 bu durumu bir duyarlılık analiziyle inceliyor; Gün 3 ise modeli mutlak tahmin için değil, senaryoları karşılaştırmak için kullanıyor.

## Yerel kurulum

Colab yerine kendi bilgisayarınızda çalışmak isterseniz (Python 3.12 önerilir):

```bash
git clone https://github.com/mehmetalibeylikci/python-cevresel-modelleme
cd python-cevresel-modelleme
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab                        # veya VS Code ile notebooks/ klasörünü açın
```

## Repo yapısı

```
notebooks/   katılımcı notebook'ları (boşluklu)
cozumler/    çözümlü notebook'lar
bonus/       ana akıştan bağımsız ileri modüller
src/         su bütçesi modeli (test edilmiş)
data/        ham ve işlenmiş veri, kaynaklarıyla
scripts/     veri indirme, kirli kopya ve katılımcı notebook üretici
docs/        parametre kaynakları, eğitmen notları
tests/       pytest testleri
```

## Eğitmenler için

Dakika dakika akış, sık karşılaşılan hatalar ve tartışma sorularının cevapları için: [`docs/egitmen_notlari.md`](docs/egitmen_notlari.md).

## Katkıda bulunun

Hata bildirimi, yeni alıştırma ya da yeni bir bonus modül: her katkı değerli. Başlamadan önce [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını okuyun. Topluluğumuz [Davranış Kuralları](CODE_OF_CONDUCT.md)'na bağlıdır.

## Veri kaynakları

- **Meteoroloji:** ERA5 reanalizi (Copernicus Climate Change Service), [Open-Meteo](https://open-meteo.com) üzerinden, CC BY 4.0
- **Baraj durumu:** İZSU, [İzmir Büyükşehir Belediyesi Açık Veri Portalı](https://acikveri.bizizmir.com), İBB Açık Veri Lisansı
- **Doluluk gözlemleri ve parametreler:** kaynakların tamamı [`docs/parametreler.md`](docs/parametreler.md) dosyasında

Ayrıntılar: [`data/README.md`](data/README.md).

## Lisans ve atıf

- Kod: [MIT](LICENSE)
- Ders içeriği: [CC BY 4.0](LICENSE-CONTENT.md)
- Veri: kaynak lisansları, bkz. [data/README.md](data/README.md)

Bu materyali kullanırsanız lütfen atıf yapın. GitHub'daki **"Cite this repository"** düğmesi [CITATION.cff](CITATION.cff) dosyasından hazır bir atıf üretir.
