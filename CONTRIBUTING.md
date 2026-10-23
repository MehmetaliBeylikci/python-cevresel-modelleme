# Katkı Rehberi

Katkılarınızı memnuniyetle karşılıyoruz! Yazım hatası düzeltmek, yeni bir alıştırma eklemek ya da yepyeni bir bonus modül yazmak; hepsi değerli.
Katkıda bulunan herkesin [Davranış Kuralları](CODE_OF_CONDUCT.md)'na uyması beklenir.

## Nereden başlamalı?

- **Bir hata mı buldunuz?** "Hata bildir" şablonuyla bir issue açın.
- **Bir fikriniz mi var?** Önce "İçerik öner" şablonuyla bir issue açın. Böylece emek vermeden önce tartışabiliriz.
- **Küçük düzeltmeler** (yazım hatası, bozuk bağlantı) için doğrudan PR gönderebilirsiniz.

## Geliştirme ortamı

Python 3.12 kullanıyoruz (Colab ve CI ile aynı sürüm).

```bash
git clone https://github.com/mehmetalibeylikci/python-cevresel-modelleme
cd python-cevresel-modelleme
uv venv -p 3.12 .venv            # veya: python3.12 -m venv .venv
uv pip install -p .venv -r requirements-dev.txt
.venv/bin/pre-commit install     # notebook çıktılarını commit'ten önce temizler
.venv/bin/pytest                 # her şey yeşil olmalı
```

## Notebook'larla çalışmanın tek kuralı

Her notebook'un **iki sürümü** var:

| Klasör | Ne içerir | Kim düzenler |
|---|---|---|
| `cozumler/` | Çözümlü, tam sürüm | **Siz** — tüm değişiklikler burada yapılır |
| `notebooks/` | Katılımcıların açtığı, boşluklu sürüm | **Script** — elle düzenlemeyin |

Katılımcının dolduracağı kodu `# BEGIN SOLUTION` / `# END SOLUTION` arasına yazın:

```python
monthly = daily.resample("MS").sum()   # bu satır katılımcıda da görünür
# BEGIN SOLUTION
wettest = monthly["precipitation_mm"].idxmax()
# END SOLUTION
print(wettest)
```

Script bu bloğu katılımcı sürümünde şuna çevirir:

```python
monthly = daily.resample("MS").sum()
# TODO: kendin yaz
...
print(wettest)
```

Tamamen eğitmene özel bir hücre (ör. otomatik kontrol) için hücreye `solution-only` etiketi ekleyin; katılımcı sürümünden silinir.

Değişiklikten sonra:

```bash
.venv/bin/python scripts/make_student_notebooks.py
```

CI, katılımcı notebook'larının güncel olmadığını görürse PR'ı kırmızıya çevirir.

## Notebook yazım kuralları

- **İlk kod hücresi** her zaman `scripts/setup_cell.py` içindeki `SETUP_CELL` metnidir (Colab'da repoyu indirir).
- **Dil:** anlatım ve yorumlar Türkçe; değişken ve fonksiyon isimleri İngilizce (`storage`, `runoff_coef`).
- **Alıştırmalar:** `### 🟢 Alıştırma N` (temel) veya `### 🔵 Alıştırma N` (ileri) başlığıyla.
- **Grafikler:** Türkçe başlık ve eksen etiketleri; eksende birim yazın (`Depolama (hm³)`).
- **Kaynak:** Yeni bir sayı ya da parametre kullanıyorsanız kaynağını `docs/parametreler.md` dosyasına yazın. Kaynaksız parametre kabul edilmez.
- **Süre:** Ders notebook'ları 2 saate sığmalı. Fazlası "## Zaman kalırsa" bölümüne gider.

## Yeni bir bonus modül eklemek

1. `bonus/<modul-adi>/` klasörü açın (küçük harf, tire ile).
2. İçine şunları koyun:
   - `README.md`: amaç, ön koşullar, tahmini süre
   - `requirements.txt`: yalnızca bu modülün ek paketleri
   - `cozum.ipynb`: çözümlü notebook
3. Katılımcı sürümü için `scripts/make_student_notebooks.py` içindeki eşlemeye modülünüzü ekleyin.
4. Ana `README.md` dosyasındaki bonus listesine bir satır ekleyin.

## Pull request kontrol listesi

- [ ] `pytest` geçiyor
- [ ] Katılımcı notebook'ları güncel (`make_student_notebooks.py --check`)
- [ ] Değiştirdiğiniz notebook "Run all" ile baştan sona hatasız çalışıyor
- [ ] Yeni veri/parametre kaynakları belgelendi

Teşekkürler! 🌊
