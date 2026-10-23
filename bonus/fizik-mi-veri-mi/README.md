# Bonus — Fizik mi, Veri mi?

Ana eğitimden bağımsız, **kendi başına** çalışılacak bir modül (~1,5 saat).

Üç gün boyunca Tahtalı Barajı için kütle korunumuna dayanan **fiziksel bir model** kurduk. Bu modülde aynı soruyu bir **makine öğrenmesi** modeliyle (scikit-learn, Random Forest) soruyor, sonra **SHAP** ile ML modelinin neye baktığını açıyoruz.

[![Colab'da aç](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mehmetalibeylikci/python-cevresel-modelleme/blob/main/bonus/fizik-mi-veri-mi/fizik_mi_veri_mi.ipynb)

## Ön koşul

- Gün 1 (veri hazırlama) ve Gün 2 (model kurulumu)
- Temel pandas ve matplotlib bilgisi

## Neler öğreneceksiniz?

- Zaman serisinde eğitim ve test verisini **zamana göre** ayırmak (ve neden rastgele ayırmamak gerektiği)
- scikit-learn ile bir model kurmak: oluştur → `fit` → `predict`
- R² ve RMSE ile modeli değerlendirmek
- SHAP ile bir ML modelini yorumlamak
- Fiziksel ve veri güdümlü modellerin güçlü ve zayıf yanları

## Dürüstlük notu

Tahtalı'nın geçmiş doluluk serisi açık bir kaynakta bulunmadığı için ML modeli **gözlemlere değil, fiziksel modelimizin çıktısına** eğitiliyor. Bu kurgu notebook'un başında açıkça belirtiliyor ve bir tartışma sorusuna dönüştürülüyor.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `fizik_mi_veri_mi.ipynb` | Katılımcı notebook'u (boşluklu) |
| `cozum.ipynb` | Çözümlü sürüm |
| `requirements.txt` | Bu modülün ek paketleri (`scikit-learn`, `shap`) |

Yerelde çalıştırmak için ana paketlere ek olarak:

```bash
pip install -r bonus/fizik-mi-veri-mi/requirements.txt
```
