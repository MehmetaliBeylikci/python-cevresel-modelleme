# roadmap.sh için yol haritası taslağı

roadmap.sh editörüne aktarılacak düğüm yapısı. Ana akış dikey ilerler; her başlığın alt konuları yanına bağlanır. "İsteğe bağlı" işaretli düğümler roadmap.sh'te "Optional" türünde çizilir.

Başlık: **Python ile Çevresel Modelleme: Tahtalı Barajı Su Bütçesi**
Açıklama: 3 günlük, açık kaynak Python eğitimi. Veri hazırlama, model kurulumu, görselleştirme ve senaryolar.

## Gün 0: Ön Hazırlık (~1 saat, kendi başına)

- Colab'ı tanıyalım
- Değişkenler
- f-string ile okunaklı çıktı
- Listeler
- `for` döngüsü ve `if` koşulu
- Sözlükler
- Fonksiyonlar
- Hazır mıyım? (5 görev)

Bağlantı: notebooks/00_on_hazirlik.ipynb (Colab)

## Gün 1: Veri Hazırlama (2 saat)

- Problem: İzmir'in suyu nereden geliyor?
- pandas temelleri
- Sweetviz ile kuşbakışı
- Veri temizliği
  - Tarihler
  - Tekrarlanan satırlar
  - Fiziksel olarak imkânsız değerler
  - Birim hatası
  - Eksik günler
- Günlükten aylığa: `resample`
- İlk grafik ve kaydetme
- İsteğe bağlı: Temizliğimiz ne kadar iyiydi?

Bağlantı: notebooks/01_veri_hazirlama.ipynb (Colab)

## Gün 2: Model Kurulumu (2 saat)

- Kavramsal model: baraj bir kovadır
  - Birimler: en sık hata kaynağı
- Modeli yazalım
  - Önce tek bir ay
  - Bir döngü ve bir fonksiyon
- Model gerçeğe yakın mı?
- Duyarlılık analizi
  - İnteraktif keşif (ipywidgets)
- Tartışma: modelin varsayımları
- İsteğe bağlı: Depolamaya bağlı göl alanı

Bağlantı: notebooks/02_model_kurulumu.ipynb (Colab)

## Gün 3: Görselleştirme ve Senaryolar (2 saat)

- matplotlib anatomisi
- Senaryolar (iklim ve talep)
- Sunuma hazır figürler
  - Çok panelli figür
  - Mevsimsel ısı haritası (seaborn)
  - İnteraktif grafik (plotly)
- Kapanış: Bu model neyi söyleyebilir, neyi söyleyemez?
- İsteğe bağlı: Kendi senaryonuz
- İsteğe bağlı: Sonuçlar parametrelere ne kadar bağlı?

Bağlantı: notebooks/03_gorsellestirme_senaryolar.ipynb (Colab)

## Bonus: Fizik mi, Veri mi? (isteğe bağlı)

- Hedef ve özellikler
- Eğitim ve test verisini zamana göre ayırmak
- Random Forest (scikit-learn)
- SHAP: Model neye bakıyor?
- Tartışma ve AutoML notu

Bağlantı: bonus/fizik-mi-veri-mi/fizik_mi_veri_mi.ipynb (Colab)
