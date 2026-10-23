# Tahtalı Su Bütçesi Eğitimi — Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 3 günlük, Colab'da çalışan, açık kaynak bir Python eğitim reposu kurmak: Tahtalı Barajı aylık su bütçesi modeli üzerinden veri hazırlama, model kurulumu ve görselleştirme.

**Architecture:**
- Modelin tek doğruluk kaynağı `src/model.py` dosyasıdır; pytest ile test edilir.
- Notebook'lar yalnızca çözümlü hâlleriyle elle yazılır. Katılımcı notebook'ları bunlardan `scripts/make_student_notebooks.py` ile otomatik üretilir; böylece iki sürüm hiçbir zaman birbirinden kopmaz.
- CI, çözüm notebook'larını baştan sona çalıştırır ve katılımcı notebook'larının güncel olduğunu doğrular.

**Tech Stack:**
- Python 3.12 (CI ve Colab ile aynı)
- pandas, numpy, matplotlib, seaborn, plotly, ipywidgets, folium, sweetviz
- Bonus modül: scikit-learn, shap
- Geliştirme: pytest, nbformat, nbconvert, nbclient, pre-commit + nbstripout, uv

**Spec:** `docs/superpowers/specs/2026-10-23-tahtali-su-butcesi-egitimi-design.md`

## Global Constraints

- Repo adresi: `https://github.com/mehmetalibeylikci/python-cevresel-modelleme`. Bu adres yalnızca `README.md`, `CITATION.cff` ve Colab kurulum hücresinde geçer (hücre metni Task 5'te tanımlanıyor).
- Dil: anlatım ve yorumlar Türkçe; değişken ve fonksiyon isimleri İngilizce.
- Lisans: kod MIT, içerik CC BY 4.0. Veri dosyaları kendi kaynak lisanslarıyla kullanılır ve `data/README.md` dosyasında atıf yapılır.
- Kaynaksız parametre kullanılmaz. Her sabit, kaynağıyla birlikte `docs/parametreler.md` dosyasına yazılır.
- Sabitler (spec 2.1):
  - `S_max = 306.65` hm³, `S_min = 19.6` hm³
  - `A_havza = 546` km², `A_göl = 23.52` km²
  - `C = 0.33`, `k_E = 1.05` (C, Task 4'te kaynaktan türetildi)
  - `W = 10.7` hm³/ay
- Birim dönüşümü: 1 mm × 1 km² = 0,001 hm³.
- Doluluk oranı her yerde **aktif doluluk** olarak hesaplanır: `(S − S_min) / (S_max − S_min) × 100`. Kontrol: İZSU CSV'sinde 142,323 hm³ → %42,75.
- Kritik seviye: %10 aktif doluluk.
- ERA5 verisi: 2014-01-01 → 2026-09-30, koordinat (38.157434, 27.122630), değişkenler `precipitation_sum` ve `et0_fao_evapotranspiration`, saat dilimi `Europe/Istanbul`.
- Rastgelelik gereken her yerde seed = 42.
- Her ders notebook'u 120 dakikalık akışa sığar; her birinde bir "Zaman kalırsa" bölümü bulunur.
- Geliştirme ortamı: `uv venv -p 3.12 .venv`. Makinedeki Python 3.14 kullanılmaz.

## Review Focus

1. **Gün 1 çıktısının doğruluğu:** Kirli veriyi temizleyen çözüm notebook'unun ürettiği `tahtali_monthly.csv`, temiz ERA5 verisinin doğrudan aylık toplamıyla aynı olmalı (her ay için yağışta ±%1 tolerans). Aksi hâlde katılımcılar yanlış bir "doğru cevap" öğrenir. Test: Task 7, `test_processed_matches_clean`.
2. **Kuraklıkta su çekimi:** Depolama `S_min` seviyesine indiğinde model negatif hacim üretmemeli. Karşılanamayan çekim `shortfall` sütununda görünmeli ve kütle dengesi yine kapanmalı. Test: Task 4, `test_shortfall_when_dry` ve `test_mass_balance_closes`.
3. **Eksik ay ve hizasız seriler:** `simulate`, yağış ve ET0 serilerinin indeksleri farklıysa ya da içlerinde NaN varsa sessizce yanlış sonuç vermek yerine Türkçe, açıklayıcı bir `ValueError` fırlatmalı. Katılımcı hatası en çok burada olur. Test: Task 4, `test_rejects_misaligned_or_nan`.
4. **Colab'da ikinci kez çalıştırma:** Kurulum hücresi iki kez çalıştırıldığında (ya da "Run all" tekrarlandığında) repo ikinci kez klonlanmamalı ve iç içe klasörler oluşmamalı. Test: Task 5, `test_setup_cell_idempotent`.
5. **Katılımcı notebook'larında çözüm sızıntısı:** Üretilen katılımcı notebook'larında `# BEGIN SOLUTION` ile `# END SOLUTION` arasındaki hiçbir satır kalmamalı ve çıktılar temizlenmiş olmalı. Test: Task 5, `test_student_has_no_solution` ve CI'daki güncellik kontrolü.

---

### Task 1: Repo iskeleti ve topluluk dosyaları

**Files:**
- Create: `.gitignore`, `requirements.txt`, `requirements-dev.txt`, `.pre-commit-config.yaml`
- Create: `LICENSE`, `LICENSE-CONTENT.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `CITATION.cff`
- Create: `.github/ISSUE_TEMPLATE/hata.yml`, `.github/ISSUE_TEMPLATE/icerik-onerisi.yml`, `.github/pull_request_template.md`
- Create: `README.md` (iskelet; tam içerik Task 11'de)
- Test: `tests/test_repo_files.py`

**Interfaces:**
- Produces: `requirements.txt` ve `requirements-dev.txt`. Sonraki tüm görevler `.venv` ortamını bunlardan kurar.

- [ ] **Step 1: Geliştirme ortamını kur**

Run: `uv venv -p 3.12 .venv && uv pip install -p .venv pytest pyyaml`
Expected: `.venv/bin/python --version` → `Python 3.12.x`

- [ ] **Step 2: Başarısız testi yaz.** `tests/test_repo_files.py`:
  - `test_required_files_exist`: listedeki her dosya var mı?
  - `test_yaml_files_parse`: `CITATION.cff`, `.pre-commit-config.yaml` ve iki issue şablonu `yaml.safe_load` ile hatasız okunuyor mu?
  - `test_citation_fields`: `cff-version == "1.2.0"`, `repository-code` alanı Global Constraints'teki repo adresine eşit mi?

- [ ] **Step 3: Testi çalıştır.** `.venv/bin/pytest tests/test_repo_files.py -v` → FAIL (dosyalar yok)

- [ ] **Step 4: Dosyaları yaz**
  - `requirements.txt`: `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `ipywidgets`, `folium`, `sweetviz`. Alt sürüm sınırı koy, üst sınır koyma.
  - `requirements-dev.txt`: `-r requirements.txt`, `pytest`, `pyyaml`, `nbformat`, `nbclient`, `nbconvert`, `ipykernel`, `pre-commit`, `nbstripout`, `requests`, `scikit-learn`, `shap`
  - `.pre-commit-config.yaml`: yalnızca `nbstripout` hook'u
  - `.gitignore`: `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`, `*.html` (Sweetviz raporu), `figures/`
  - `CODE_OF_CONDUCT.md`: Contributor Covenant 2.1'in Türkçe çevirisi; iletişim adresi olarak GitHub issue'ları
  - `CONTRIBUTING.md` (Türkçe): kurulum, pre-commit, "notebook'ları yalnızca `cozumler/` altında düzenle, sonra `make_student_notebooks.py` çalıştır", `# BEGIN SOLUTION`/`# END SOLUTION` kuralı, yeni bir bonus modül nasıl eklenir, PR kontrol listesi
  - Issue formları (GitHub Forms YAML): hata bildirimi (hangi notebook, hangi hücre, hata mesajı, Colab mı yerel mi) ve içerik önerisi
  - `README.md`: şimdilik yalnızca başlık, tek paragraflık özet ve lisans bölümü. Program tablosu ve diğer bölümler Task 11'de eklenir.

- [ ] **Step 5: Testleri ve pre-commit'i çalıştır**

Run: `.venv/bin/pytest tests/test_repo_files.py -v` → PASS
Run: `uv pip install -p .venv -r requirements-dev.txt && .venv/bin/pre-commit install` → hatasız

- [ ] **Step 6: Commit** — `git commit -m "chore: repo iskeleti ve topluluk dosyaları"`

---

### Task 2: Ham veri ve indirme scripti

**Files:**
- Create: `scripts/download_era5.py`, `data/raw/tahtali_era5_daily.csv`
- Create: `data/raw/izsu_baraj_2026-10-14.csv`, `data/raw/izsu_baraj_2025-08-11_wayback.csv`
- Create: `data/README.md`
- Test: `tests/test_raw_data.py`

**Interfaces:**
- Produces: `data/raw/tahtali_era5_daily.csv`. Sütunlar: `date` (ISO `YYYY-MM-DD`), `precipitation_mm`, `et0_mm`. Her gün için tek satır.
- Produces: `fetch_era5(start: str, end: str, lat: float, lon: float) -> pd.DataFrame`, `scripts/download_era5.py` içinde; dönen tablo yukarıdaki sütunlara sahip.

- [ ] **Step 1: Başarısız testi yaz.** `tests/test_raw_data.py`:
  - `test_era5_shape`: ilk tarih `2014-01-01`, son tarih `2026-09-30`, satır sayısı = gün sayısı (4656), tekrarlı tarih yok
  - `test_era5_values`: NaN yok, `precipitation_mm >= 0`, `et0_mm >= 0`, yıllık ortalama yağış 300–1200 mm aralığında (İzmir için makullük kontrolü)
  - `test_izsu_snapshots`: iki CSV de `;` ayraçla okunuyor; `Tahtalı Barajı` satırı var; 2026 dosyasında `SU_DURUMU == 142323000` ve `DOLULUK_ORANI == 42.75`

- [ ] **Step 2: Testi çalıştır.** → FAIL

- [ ] **Step 3: `fetch_era5` fonksiyonunu ve CLI'ı yaz**
  - Uç nokta: `https://archive-api.open-meteo.com/v1/archive`, parametreler: `daily=precipitation_sum,et0_fao_evapotranspiration` ve `timezone=Europe/Istanbul`
  - Sütunları `precipitation_mm` ve `et0_mm` olarak yeniden adlandır
  - CLI çıktısı varsayılan olarak `data/raw/tahtali_era5_daily.csv` dosyasına yazılır

- [ ] **Step 4: Verileri indir**
  - ERA5: `.venv/bin/python scripts/download_era5.py`
  - Güncel İZSU dosyası: `https://openfiles.izmir.bel.tr/309436/docs/izsu-baraj-doluluk-oranlari.csv` adresinden indir, `izsu_baraj_2026-10-14.csv` olarak kaydet. İçindeki `DURUM_TARIHI` değerinin 2026-10-14 olduğunu kontrol et; farklıysa dosya adını o tarihe göre değiştir ve spec'teki kontrol noktası tarihini güncelle.
  - Arşiv kaydı: `https://web.archive.org/web/20250902152857id_/https://openfiles.izmir.bel.tr/309436/docs/izsu-baraj-doluluk-oranlari.csv` adresinden indir (`id_` eki, ham dosyayı verir)

- [ ] **Step 5: `data/README.md` dosyasını yaz.** Her dosya için kaynak URL, indirme tarihi, lisans (ERA5/Open-Meteo CC BY 4.0, İBB Açık Veri Lisansı), sütun açıklamaları ve birimler. Kirli kopya için bir bölüm başlığı aç; içeriği Task 3'te doldurulacak.

- [ ] **Step 6: Testi çalıştır.** → PASS

- [ ] **Step 7: Commit** — `git commit -m "data: ERA5 günlük veri ve İZSU anlık kayıtları"`

---

### Task 3: Eğitim için kirli kopya

**Files:**
- Create: `scripts/make_dirty_copy.py`, `data/raw/tahtali_era5_daily_kirli.csv`
- Modify: `data/README.md` (kirli kopya bölümü)
- Test: `tests/test_dirty_copy.py`

**Interfaces:**
- Consumes: Task 2'deki temiz CSV
- Produces: `make_dirty(clean: pd.DataFrame, seed: int = 42) -> pd.DataFrame`. Dönen tablodaki `date` sütunu string tipinde.
- Produces: `UNIT_ERROR_YEAR = 2019`. Bu yılda `precipitation_mm` değerleri 10'a bölünür (cm cinsinden yazılmış gibi). Day 1 çözümü bu yılı veri üzerinden bulur, sabiti import etmez.

- [ ] **Step 1: Başarısız testi yaz.** `tests/test_dirty_copy.py`, `clean` = temiz CSV, `dirty = make_dirty(clean)`:
  - `test_deterministic`: aynı seed ile iki çağrı birebir aynı tabloyu verir
  - `test_missing_days`: tekilleştirilmiş tarih sayısı, temiz veriye göre %1,5–%2,5 daha az
  - `test_duplicates`: `dirty.duplicated().sum() == 20`
  - `test_unit_error`: 2019 yağış toplamı, temiz 2019 toplamının 1/10'u (±%1)
  - `test_impossible_values`: tam olarak 3 negatif yağış ve 2 adet 900 mm değeri var
  - `test_mixed_dates`: `date` değerlerinin %5–%15'i `DD.MM.YYYY`, geri kalanı `YYYY-MM-DD` formatında
  - `test_recoverable`: tüm bozmalar geri alındığında (iki tarih formatını da ayrıştır, tekrarları sil, imkânsız değerleri at, 2019 yağışını 10 ile çarp), kalan her günün değerleri temiz veriyle eşleşir

- [ ] **Step 2: Testi çalıştır.** → FAIL

- [ ] **Step 3: `make_dirty` fonksiyonunu yaz.** Uygulama sırası: birim hatası → imkânsız değerler → gün silme → tekrar ekleme → tarih formatını karıştırma → `date` sütununa göre sırala (tekrarlar komşu kalsın). Tüm seçimler tek bir `np.random.default_rng(seed)` üzerinden yapılır. Gün silme ve tekrar ekleme, imkânsız değer atanmış satırları seçmez. Böylece 3 negatif ve 2 adet 900 mm değeri her zaman tam olarak bir kez bulunur.

- [ ] **Step 4: Kirli CSV'yi üret, `data/README.md` dosyasına bozmaları tablo olarak yaz.** Uyarı: "eğitim için kasıtlı olarak bozulmuştur, analizde kullanmayın"

- [ ] **Step 5: Testi çalıştır.** → PASS

- [ ] **Step 6: Commit** — `git commit -m "data: Gün 1 için tekrarlanabilir kirli kopya"`

---

### Task 4: Su bütçesi modeli ve parametre kaynakları

**Files:**
- Create: `src/__init__.py`, `src/model.py`, `docs/parametreler.md`
- Test: `tests/test_model.py`

**Interfaces:**
- Produces (Task 8, 9 ve 10 bunu import eder):
  ```python
  @dataclass(frozen=True)
  class Params:
      catchment_km2: float = 546.0
      lake_km2: float = 23.52
      s_max: float = 306.65   # hm³
      s_min: float = 19.6     # hm³
      runoff_coef: float = 0.33
      evap_coef: float = 1.05
      withdrawal: float = 10.7  # hm³/ay

  def simulate(precip_mm: pd.Series, et0_mm: pd.Series, s0: float,
               params: Params = Params()) -> pd.DataFrame
  # index: girdilerle aynı (aylık). Sütunlar (hm³):
  # storage (ay sonu), inflow, evaporation, withdrawal (gerçekleşen), spill, shortfall

  def active_fill_pct(storage, params: Params = Params())  # float veya Series döner

  S0_DATE: str      # simülasyonun başladığı ay, örn. "2014-01"
  S0_HM3: float     # o ayın başındaki depolama
  ```

- [ ] **Step 1: Parametreleri teyit et ve `docs/parametreler.md` dosyasını yaz.** Her sabit için değer, birim ve kaynak (URL + erişim tarihi) yazılır.
  - `A_havza` ve `A_göl` için DSİ veya İZSU kaynağı aranır.
  - `C` için bir Akdeniz havzası kaynağı aranır.
  - `k_E` için FAO-56 kaynağı gösterilir.
  - `S0_HM3`: 2014–2015 arasında İZSU kaynaklı bulunabilen en erken aylık doluluk değeri. `S0_DATE` o ay olur.
  - Teyit edilen bir değer spec'tekinden farklıysa, spec'teki tablo ve Global Constraints da aynı commit'te güncellenir.

- [ ] **Step 2: Başarısız testi yaz.** `tests/test_model.py`, sabit 12 aylık sentetik seriler kullanarak:
  - `test_no_forcing_no_change`: `P = 0`, `ET0 = 0`, `withdrawal = 0` → storage her ay `s0` değerinde kalır
  - `test_bounds`: rastgele seriler için (seed 42, `P` 0–400 mm) `s_min <= storage <= s_max`
  - `test_spill_when_full`: `s0 = s_max`, `P = 300` mm → `spill > 0` ve storage == `s_max`
  - `test_shortfall_when_dry`: `s0 = s_min + 5`, `P = 0` → ilk ayda `shortfall > 0`, storage == `s_min`
  - `test_mass_balance_closes`: her ay için `Δstorage == inflow − evaporation − withdrawal − spill` (1e-9 tolerans)
  - `test_unit_conversion`: 100 mm yağış, `C = 0.25`, `ET0 = 0` → `inflow == 0.25·100·546·0.001 + 100·23.52·0.001`
  - `test_active_fill_pct`: `active_fill_pct(142.323) ≈ 42.75` (0,01 tolerans); `s_min` → 0, `s_max` → 100
  - `test_rejects_misaligned_or_nan`: indeksleri farklı ya da NaN içeren seriler `ValueError` fırlatır; mesaj Türkçe

- [ ] **Step 3: Testi çalıştır.** → FAIL

- [ ] **Step 4: `src/model.py` dosyasını yaz.** Her ay için: hamle = `S + inflow − evaporation − withdrawal`. Hamle `s_max` üstündeyse fark `spill` olur. Hamle `s_min` altındaysa fark `shortfall` olur ve gerçekleşen `withdrawal` o kadar azaltılır. Döngü açık bir `for` döngüsü olarak yazılır (Gün 2'de aynısı birlikte yazılacak). Docstring'ler Türkçe.

- [ ] **Step 5: Testi çalıştır.** → PASS

- [ ] **Step 6: Commit** — `git commit -m "feat: aylık su bütçesi modeli ve kaynaklı parametreler"`

---

### Task 5: Notebook araç zinciri ve CI

**Files:**
- Create: `scripts/make_student_notebooks.py`, `scripts/setup_cell.py`
- Create: `.github/workflows/test.yml`
- Test: `tests/test_notebook_tools.py`

**Interfaces:**
- Produces: `make_student(nb: nbformat.NotebookNode) -> nbformat.NotebookNode`.
  - Kod hücrelerinde `# BEGIN SOLUTION` ile `# END SOLUTION` arasındaki satırları, aynı girintiyle `# TODO: kendin yaz` + `...` ile değiştirir.
  - `solution-only` etiketli hücreleri siler.
  - Tüm çıktıları temizler.
- Produces: CLI kullanımı `python scripts/make_student_notebooks.py [--check]`.
  - Eşlemeler: `cozumler/NN_*.ipynb` → `notebooks/NN_*.ipynb` ve `bonus/*/cozum.ipynb` → `bonus/*/fizik_mi_veri_mi.ipynb`.
  - `--check` modunda dosya yazmaz; güncel olmayan dosya varsa exit 1 döner.
- Produces: `SETUP_CELL: str` (`scripts/setup_cell.py` içinde). Her notebook'un ilk kod hücresi birebir bu metindir:
  ```python
  # Kurulum: Colab'da repoyu indirir, yerelde hiçbir şey yapmaz.
  import os, sys
  REPO = "https://github.com/mehmetalibeylikci/python-cevresel-modelleme"
  if "google.colab" in sys.modules:
      if not os.path.exists("/content/python-cevresel-modelleme"):
          !git clone -q {REPO} /content/python-cevresel-modelleme
      %cd /content/python-cevresel-modelleme
      %pip install -q sweetviz
  else:
      while not os.path.exists("src/model.py") and os.getcwd() != "/":
          os.chdir("..")
  sys.path.insert(0, os.getcwd())
  ```

- [ ] **Step 1: Başarısız testi yaz.** `tests/test_notebook_tools.py`:
  - `test_student_has_no_solution`: iki çözüm bloğu, bir `solution-only` hücre ve bir çıktı içeren bir test notebook'u → üretilen notebook'ta "BEGIN SOLUTION" geçmez, `solution-only` hücre yoktur, çıktılar boştur, `...` satırı doğru girintiyle yer alır
  - `test_student_is_valid_python`: üretilen her kod hücresi (IPython `!`/`%` satırları çıkarıldıktan sonra) `ast.parse` ile hatasız ayrıştırılır
  - `test_setup_cell_idempotent`: `SETUP_CELL`'in Colab dalı bir geçici dizinde iki kez simüle edilir (`git clone` yerine `os.makedirs` kullanılarak). İkinci çalıştırma yeni bir klasör oluşturmaz.
  - `test_check_mode_detects_drift`: güncel olmayan bir katılımcı notebook'u varken `--check` exit 1 döner

- [ ] **Step 2: Testi çalıştır.** → FAIL

- [ ] **Step 3: `make_student` fonksiyonunu, CLI'ı ve `SETUP_CELL` sabitini yaz**

- [ ] **Step 4: Testi çalıştır.** → PASS

- [ ] **Step 5: `.github/workflows/test.yml` dosyasını yaz.** Ubuntu ve Python 3.12 üzerinde şu adımlar:
  1. `pip install -r requirements-dev.txt`
  2. `pytest`
  3. `python scripts/make_student_notebooks.py --check`
  4. `jupyter nbconvert --to notebook --execute --output-dir /tmp/out cozumler/*.ipynb bonus/*/cozum.ipynb` (hücre zaman aşımı 600 sn)

- [ ] **Step 6: Commit** — `git commit -m "ci: katılımcı notebook üretici ve CI"`

---

### Notebook görevleri için ortak kurallar (Task 6–10)

- Yalnızca çözüm notebook'u elle yazılır. Ardından `make_student_notebooks.py` çalıştırılır ve iki dosya birlikte commit'lenir.
- İlk kod hücresi `SETUP_CELL`'dir. İkinci hücre bir başlık, öğrenme hedefleri ve süre tablosudur (spec Bölüm 3'teki tablo aynen kullanılır).
- Alıştırma başlıkları `### 🟢 Alıştırma N` ve `### 🔵 Alıştırma N` formatındadır. Her alıştırmanın altında bir çözüm hücresi vardır; çözüm `# BEGIN SOLUTION` bloğunun içindedir.
- Canlı kodlama sırasında katılımcının dolduracağı satırlar da `# BEGIN SOLUTION` bloğu içindedir.
- Her notebook'ta "## Zaman kalırsa" başlıklı bölüm bulunur; atlanması sonraki hücreleri bozmamalıdır.
- Grafiklerin başlık ve eksen etiketleri Türkçedir; eksen etiketlerinde birim yazılır.
- Her görevin doğrulaması:
  1. `.venv/bin/jupyter nbconvert --execute` hatasız biter
  2. `make_student_notebooks.py --check` → exit 0
  3. Görevde belirtilen ek test geçer

### Task 6: Gün 0 — Ön hazırlık

**Files:** `cozumler/00_on_hazirlik.ipynb`, `notebooks/00_on_hazirlik.ipynb`

- [ ] **Step 1: Notebook'u yaz.** İçerik: Colab kullanımı; değişkenler, listeler, sözlükler, `for`/`if`, fonksiyonlar, f-string. Örneklerde aylık yağış listesi kullanılır (örneğin "en yağışlı ayı bul" görevi). Sonunda 5 soruluk "Hazır mıyım?" bölümü: her soru küçük bir kod görevi + `assert` ile kendi kendini kontrol eden bir hücre.
- [ ] **Step 2: Doğrula** (ortak kurallardaki 1–2) → PASS
- [ ] **Step 3: Commit** — `git commit -m "content: Gün 0 ön hazırlık"`

### Task 7: Gün 1 — Veri hazırlama

**Files:** `cozumler/01_veri_hazirlama.ipynb`, `notebooks/01_veri_hazirlama.ipynb`, `data/processed/tahtali_monthly.csv`, `tests/test_processed.py`

**Interfaces:**
- Consumes: `data/raw/tahtali_era5_daily_kirli.csv`, İZSU CSV'si (harita koordinatları için)
- Produces: `data/processed/tahtali_monthly.csv`. Sütunlar: `month` (`YYYY-MM`), `precipitation_mm`, `et0_mm`. Toplam 153 satır (2014-01 → 2026-09).

- [ ] **Step 1: Sweetviz uyumluluğunu kontrol et.** `.venv` içinde `sweetviz.analyze(df).show_html("rapor.html", open_browser=False)` çalıştır.
  - Hata verirse `sweetviz` yerine `ydata-profiling` kullan. Bu durumda `requirements.txt`, `SETUP_CELL`'deki `%pip` satırı ve spec'in ilgili satırı aynı commit'te güncellenir.
- [ ] **Step 2: Başarısız testi yaz.** `tests/test_processed.py`:
  - `test_processed_matches_clean`: `tahtali_monthly.csv` dosyası 153 satır içerir. Her ay için `precipitation_mm` ve `et0_mm`, temiz günlük verinin `resample("MS").sum()` sonucuyla ±%1 toleransta eşleşir. Eksik günler doldurulduğu için birebir eşleşme beklenmez.
- [ ] **Step 3: Testi çalıştır.** → FAIL
- [ ] **Step 4: Notebook'u spec'teki Gün 1 süre tablosuna göre yaz.**
  - Açılışta bir Türkçe–İngilizce terim sözlüğü tablosu yer alır (örn. depolama/storage, akış katsayısı/runoff_coef, çekim/withdrawal, taşma/spill, buharlaşma/evaporation).
  - folium haritası barajın koordinatlarını İZSU CSV'sinden okur.
  - Eksik günler `interpolate(method="time")` ile doldurulur. Neden ileri doldurma değil de interpolasyon seçildiği markdown'da açıklanır.
  - Birim hatası, yıllık toplam çubuk grafiğinde 2019'un aykırı görünmesiyle bulunur.
  - Notebook son hücrede `data/processed/tahtali_monthly.csv` dosyasını yazar.
- [ ] **Step 5: Notebook'u çalıştır, testi çalıştır.** → PASS
- [ ] **Step 6: Commit** — `git commit -m "content: Gün 1 veri hazırlama"`

### Task 8: Gün 2 — Model kurulumu

**Files:** `cozumler/02_model_kurulumu.ipynb`, `notebooks/02_model_kurulumu.ipynb`

**Interfaces:**
- Consumes: `data/processed/tahtali_monthly.csv`, `src.model` (`Params`, `simulate`, `active_fill_pct`, `S0_DATE`, `S0_HM3`)

- [ ] **Step 1: Notebook'u spec'teki Gün 2 süre tablosuna göre yaz.**
  - Katılımcı modeli notebook içinde `my_simulate` adıyla kendisi yazar.
  - Ardından bir hücre `assert np.allclose(my_simulate(...)["storage"], simulate(...)["storage"])` ile kendi fonksiyonunu `src.model.simulate` ile karşılaştırır.
  - Makullük kontrolü:
    - 2025-07 ay sonu model değeri, Wayback kaydındaki 2025-08-11 durumuyla (40,98 hm³, %7,45) karşılaştırılır.
    - 2026-09 ay sonu model değeri, 2026-10-14 kaydıyla karşılaştırılır; iki hafta fark olduğu belirtilir.
    - Fark tablo olarak gösterilir.
  - Duyarlılık analizi:
    - Tarama: `runoff_coef ∈ {0.10, 0.15, …, 0.40}` × `withdrawal ∈ {8, 10.7, 13, 17.1}` hm³/ay. Buradaki 17,1 değeri, yıllık 205 hm³'e karşılık gelir.
    - Sonuç: 2026-09 ay sonu aktif doluluğu, pivot tablo ve ısı haritası olarak gösterilir.
  - ipywidgets bölümü: `interact` ile `runoff_coef` ve `withdrawal` için kaydırma çubukları ve anlık güncellenen depolama grafiği.
  - 🔵 ileri alıştırma: depolamaya bağlı göl alanı, `A_göl = lake_km2 · (S / s_max)^(2/3)`.
- [ ] **Step 2: Doğrula** (ortak kurallardaki 1–2). `interact` hücresi nbconvert altında hata vermemeli; widget görüntülenemese de yürütme devam etmeli. → PASS
- [ ] **Step 3: Commit** — `git commit -m "content: Gün 2 model kurulumu"`

### Task 9: Gün 3 — Görselleştirme ve senaryolar

**Files:** `cozumler/03_gorsellestirme_senaryolar.ipynb`, `notebooks/03_gorsellestirme_senaryolar.ipynb`

**Interfaces:**
- Consumes: Task 8 ile aynı
- Produces: `figures/` klasörüne yazılan PNG dosyaları. Bu klasör `.gitignore` içinde.

- [ ] **Step 1: Notebook'u spec'teki Gün 3 süre tablosuna göre yaz.**
  - "Kötü grafik" örneği: varsayılan ayarlarla çizilmiş, etiketsiz, birimsiz, spagetti hâlinde bir grafik. Bu grafik 5 adımda düzeltilir.
  - Senaryolar: temel, yağış ×0.8, ET0 ×1.1, `withdrawal` ×1.15. Senaryolar, `Params` üzerinde `dataclasses.replace` ve girdi serilerinin çarpılmasıyla kurulur.
  - Metrik: aktif doluluğun %10'un altında kaldığı ay sayısı. Senaryo başına bir tablo.
  - Görseller:
    - 3 panelli figür: depolama, aylık giriş/çıkış ve senaryo karşılaştırması
    - seaborn ile yıl × ay ısı haritası (aktif doluluk)
    - plotly ile senaryo grafiğinin interaktif hâli
    - `savefig("figures/...png", dpi=200)`
  - Kapanış markdown'ı: modelin sınırları, xarray/NetCDF'ye yönlendirme, bonus modüle bağlantı.
- [ ] **Step 2: Doğrula** (ortak kurallardaki 1–2) → PASS
- [ ] **Step 3: Commit** — `git commit -m "content: Gün 3 görselleştirme ve senaryolar"`

### Task 10: Bonus — Fizik mi, veri mi?

**Files:** `bonus/fizik-mi-veri-mi/README.md`, `bonus/fizik-mi-veri-mi/requirements.txt`, `bonus/fizik-mi-veri-mi/cozum.ipynb`, `bonus/fizik-mi-veri-mi/fizik_mi_veri_mi.ipynb`

**Interfaces:**
- Consumes: `src.model`, `data/processed/tahtali_monthly.csv`

- [ ] **Step 1: README ve requirements dosyalarını yaz.** README'de amaç, ön koşul (Gün 1–2) ve kendi başına çalışma süresi (~1,5 saat) yer alır. `requirements.txt` içeriği: `scikit-learn`, `shap`. `SETUP_CELL`'den sonraki ilk hücre bunları `%pip install -q` ile kurar.
- [ ] **Step 2: Notebook'u yaz.**
  - Hedef değişken: `simulate` çıktısından `ΔS = storage.diff()`.
  - Özellikler: `precipitation_mm`, `et0_mm`, `month_of_year`.
  - Bölme: zamana göre, 2024-01 öncesi eğitim, sonrası test. Rastgele bölme kullanılmaz ve nedeni (zaman serisinde bilgi sızıntısı) markdown'da açıklanır.
  - Model: `RandomForestRegressor(random_state=42)`.
  - Değerlendirme: test dönemi için R² ve RMSE; tahmin ile kova modelinin karşılaştırma grafiği.
  - SHAP: `shap.TreeExplainer`, özet grafiği ve bağımlılık grafiği.
  - Spec'teki iki tartışma sorusu ve "AutoML araçları (örn. PyCaret)" paragrafı.
  - Hedef değişkenin bir model çıktısı olduğu notebook'un başında açıkça yazılır.
- [ ] **Step 3: Doğrula** (ortak kurallardaki 1–2) → PASS
- [ ] **Step 4: Commit** — `git commit -m "content: bonus Fizik mi, veri mi? modülü"`

---

### Task 11: README, eğitmen notları ve son kontrol

**Files:**
- Modify: `README.md`
- Create: `docs/egitmen_notlari.md`

- [ ] **Step 1: `README.md` dosyasını tamamla**
  - Proje özeti, hedef kitle
  - Program tablosu: her gün için Colab rozeti, rozet bağlantısı `https://colab.research.google.com/github/mehmetalibeylikci/python-cevresel-modelleme/blob/main/notebooks/<dosya>`
  - Bonus modül bağlantısı
  - Yerel kurulum (uv veya pip)
  - Katkı bağlantısı, lisanslar, veri atıfları, "Nasıl atıf yapılır"

- [ ] **Step 2: `docs/egitmen_notlari.md` dosyasını yaz.** Her gün için:
  - Hazırlık listesi
  - Dakika dakika akış (spec tablolarıyla aynı)
  - Beklenen sık hatalar ve çözümleri (örneğin tarih ayrıştırma, `resample` kullanımı, birim karışıklığı)
  - Tartışma sorularının olası cevapları
  - "Zaman yetmezse neyi atla" notu
  - "Prova bulguları" başlığı (eğitmen provadan sonra doldurur)

- [ ] **Step 3: Tüm doğrulamayı çalıştır**
  - `.venv/bin/pytest` → tüm testler PASS
  - `.venv/bin/python scripts/make_student_notebooks.py --check` → exit 0
  - CI'daki `nbconvert` komutunun aynısı → tüm notebook'lar hatasız
  - `.venv/bin/pre-commit run --all-files` → PASS

- [ ] **Step 4: Spec'e karşı son okuma.** Spec'teki her bölümün bir dosyada karşılığı var mı kontrol et; eksik varsa tamamla.

- [ ] **Step 5: Commit** — `git commit -m "docs: README ve eğitmen notları"`

**Bu planın kapsamı dışında, kullanıcının onayını gerektirenler:**
- GitHub'da reponun oluşturulması ve push edilmesi (dışarıya yayın)
- Gerçek bir Colab oturumunda eğitmen provası
