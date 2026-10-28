# roadmap.sh düğüm içerikleri

Bu dosya roadmap.sh'teki yol haritasının ("Python ile Çevresel Modelleme: Tahtalı Barajı") düğüm açıklamalarının kaynağıdır. Her `##` (gün) ve `###` (alt konu) başlığı, roadmap'teki bir düğümün etiketiyle birebir aynıdır. Başlığın altındaki paragraf düğümün açıklaması, liste ise bağlantılarıdır.

Bağlantı satırı biçimi: `- [tür] Başlık: URL`. Tür, roadmap.sh'teki bağlantı türlerinden biridir: `official`, `article`, `video`.

## Gün 0: Ön Hazırlık

Eğitimden önce kendi başına tamamlanan, yaklaşık bir saatlik bir Python girişi. Hiç kod yazmamış olanlar için değişkenler, listeler, döngüler, sözlükler ve fonksiyonlar Tahtalı Barajı örnekleriyle anlatılır. Sonundaki "Hazır mıyım?" görevlerini yapabiliyorsan eğitime hazırsın.

- [official] Gün 0 notebook'u (Colab): https://colab.research.google.com/github/mehmetalibeylikci/python-cevresel-modelleme/blob/main/notebooks/00_on_hazirlik.ipynb
- [official] Python resmi eğitimi (Türkçe değil): https://docs.python.org/3/tutorial/index.html

### Colab'ı tanıyalım

Google Colab, tarayıcıda çalışan ücretsiz bir Jupyter ortamıdır; kurulum gerekmez. Kod hücresi Shift + Enter ile çalışır ve hücreler yukarıdan aşağı sırayla çalıştırılmalıdır. Bir şeyler karışırsa "Çalışma zamanı → Tümünü çalıştır" ile baştan başlanır, değişiklikler "Dosya → Drive'a kopya kaydet" ile saklanır.

- [official] Colab'a genel bakış: https://colab.research.google.com/notebooks/basic_features_overview.ipynb

### Değişkenler

Değişken, bir değere verilen isimdir ve `=` işareti "ata" anlamına gelir. Eğitimde en sık kullanılan türler tam sayı (`int`), ondalıklı sayı (`float`, ondalık ayracı noktadır), metin (`str`) ve doğru/yanlış (`bool`) değerleridir. Bir değerin türü `type()` ile öğrenilir.

- [official] Python eğitimi: Python'u hesap makinesi olarak kullanmak: https://docs.python.org/3/tutorial/introduction.html

### f-string ile okunaklı çıktı

Bir metnin başına `f` konursa süslü parantez içine değişken yazılabilir: `f"{dam_name} Barajı %{fill:.1f} dolu"`. `:.1f` gibi biçim belirteçleri ondalık basamak sayısını ayarlar. Model sonuçlarını raporlarken sürekli kullanılır.

- [official] Python eğitimi: biçimlendirilmiş metinler: https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals

### Listeler

Liste, sıralı bir değerler topluluğudur: `[150, 50, 55, ...]`. Elemanlara sıra numarasıyla (0'dan başlayarak) erişilir; `len()`, `sum()`, `max()` ve `.index()` en çok kullanılan araçlardır. Gün 0'da Tahtalı'nın 2024 aylık yağışları bir listede tutulur.

- [official] Python eğitimi: listeler: https://docs.python.org/3/tutorial/introduction.html#lists

### for döngüsü ve if koşulu

`for` bir listedeki her eleman için aynı işi tekrarlar; `if`, `elif` ve `else` koşula göre farklı işler yapar. Döngünün ve koşulun içindeki satırlar dört boşlukla girintilenir. İki listeyi birlikte dolaşmak için `zip` kullanılır.

- [official] Python eğitimi: akış kontrolü: https://docs.python.org/3/tutorial/controlflow.html

### Sözlükler

Sözlük (`dict`), değerleri isimle saklar: `{"lake_area_km2": 23.52}`. Barajın sabit özellikleri (hacim, göl alanı, havza alanı) gibi birbirine ait bilgileri bir arada tutmak için idealdir. Yeni anahtar `sozluk["anahtar"] = deger` ile eklenir.

- [official] Python eğitimi: sözlükler: https://docs.python.org/3/tutorial/datastructures.html#dictionaries

### Fonksiyonlar

Aynı hesabı defalarca yapacaksak onu `def` ile bir fonksiyona çeviririz; sonuç `return` ile döner. Gün 0'daki `rain_to_volume` fonksiyonu yağışı (mm) ve alanı (km²) hacme (hm³) çevirir. Gün 2'deki su bütçesi modeli de bir fonksiyon olarak yazılır.

- [official] Python eğitimi: fonksiyon tanımlamak: https://docs.python.org/3/tutorial/controlflow.html#defining-functions

### Hazır mıyım? (5 görev)

Dört temel ve bir ileri görevden oluşan kısa bir sınav: toplam yağış, en yağışlı ay, kurak aylar, aktif doluluk fonksiyonu ve yağmursuz bir barajın kaç ayda boşalacağı. Her görevin altındaki kontrol hücresi hata vermiyorsa görev doğrudur. Son görevde aslında küçük bir çevresel model kurulur.

## Gün 1: Veri Hazırlama

Modeli besleyecek günlük yağış ve buharlaşma potansiyeli (ET0) verisi okunur, incelenir, temizlenir ve aylığa çevrilir. Veri, eğitim için kasıtlı olarak bozulmuş bir ERA5 kopyasıdır: yanlış biçimli tarihler, tekrarlanan satırlar, imkânsız değerler, bir birim hatası ve eksik günler içerir. Gün sonunda temiz aylık seri bir CSV dosyasına kaydedilir.

- [official] Gün 1 notebook'u (Colab): https://colab.research.google.com/github/mehmetalibeylikci/python-cevresel-modelleme/blob/main/notebooks/01_veri_hazirlama.ipynb
- [official] pandas'a 10 dakikada giriş: https://pandas.pydata.org/docs/user_guide/10min.html

### Problem: İzmir'in suyu nereden geliyor?

Tahtalı Barajı, İzmir'in yüzey su kaynakları arasında kapasitesi en büyük barajdır ve kent merkezindeki 11 ilçenin suyunun yaklaşık %40'ını karşılar. 11 Ağustos 2025'te aktif doluluk %7,45'e düştü, 14 Ekim 2026'da %42,75'e çıktı. Üç gün boyunca sorulan soru şu: barajın doluluğu yağışa, buharlaşmaya ve şehrin su çekimine nasıl bağlı?

- [official] İzmir Büyükşehir Belediyesi Açık Veri Portalı: https://acikveri.bizizmir.com
- [article] BirGün: İZSU'dan Tahtalı Barajı için uyarı: https://www.birgun.net/haber/izsu-dan-tahtali-baraji-icin-onemli-uyari-izmir-in-can-damarini-korumak-zorundayiz-306578

### pandas temelleri

pandas, tablo biçimindeki veriyle çalışmanın standart yoludur: tablonun tamamı `DataFrame`, tek sütunu `Series` olarak adlandırılır. `read_csv` ile okunan veri `head()`, `info()` ve `describe()` ile hızlıca tanınır. Sütun seçmek, koşula göre satır filtrelemek ve yeni sütun eklemek temel hareketlerdir.

- [official] pandas'a 10 dakikada giriş: https://pandas.pydata.org/docs/user_guide/10min.html
- [official] Open-Meteo geçmiş hava durumu API'si (ERA5): https://open-meteo.com/en/docs/historical-weather-api

### Sweetviz ile kuşbakışı

Sweetviz tek satırla her sütunun dağılımını, eksik değerleri ve sütunlar arası ilişkileri gösteren bir keşifsel analiz raporu üretir. Rapor sorunlara dair ipucu verir ama onları çözmez; bulunan sorunlar sonraki adımda tek tek düzeltilir.

- [official] Sweetviz (GitHub): https://github.com/fbdesignpro/sweetviz

### Veri temizliği

Gerçek veriler nadiren temiz gelir. Bu bölümde beş tipik sorun sırayla bulunur ve düzeltilir: karışık tarih biçimleri, tekrarlanan satırlar, fiziksel olarak imkânsız değerler, bir yıla ait birim hatası ve eksik günler. Her adımda "bu değeri silmeli miyim, düzeltmeli miyim, eksik mi saymalıyım?" sorusu tartışılır.

- [official] pandas: eksik veriyle çalışmak: https://pandas.pydata.org/docs/user_guide/missing_data.html

### Tarihler

Bazı satırlarda tarih `2019-03-05` yerine `05.03.2019` biçiminde yazılmıştır. İki biçim `pd.to_datetime(..., errors="coerce")` ile ayrı ayrı çevrilip birleştirilir; çevrilemeyen değerler hata yerine `NaT` olur. Ardından tarih, zaman serisi araçlarının beklediği gibi indeks yapılır.

- [official] pandas.to_datetime: https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html

### Tekrarlanan satırlar

Aynı günün birden fazla kez geçmesi toplamları şişirir. `duplicated()` tekrarları sayar, `drop_duplicates()` siler. Temizlikten sonra her tarihin tabloda yalnızca bir kez geçtiği kontrol edilir.

- [official] pandas.DataFrame.drop_duplicates: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html

### Fiziksel olarak imkânsız değerler

Yağış negatif olamaz, İzmir'de bir günde 900 mm yağış da gerçekçi değildir. Bu değerlerin aslında ne olduğu bilinemediği için silinmez, eksik (`NaN`) olarak işaretlenir ve diğer eksiklerle birlikte doldurulur. Fiziksel sınırları bilmek, veri temizliğinin en güçlü aracıdır.

### Birim hatası

En sinsi hata türüdür: değerler makul görünür ama yanlıştır. Yıllık toplam yağış grafiğinde 2019 diğer yılların yaklaşık onda biri çıkar; o yıl yağış büyük olasılıkla santimetre cinsinden kaydedilmiştir ve 10 ile çarpılarak düzeltilir. Gerçek hayatta böyle bir düzeltmeden önce veri sağlayıcısının belgelerine bakılır.

### Eksik günler

`pd.date_range` ile olması gereken tüm günler üretilir, `reindex` eksik günleri tabloya `NaN` olarak ekler. Doldurma seçenekleri `fillna(0)`, `ffill()` ve `interpolate(method="time")` karşılaştırılır. ET0 yavaş değiştiği için interpolasyona uygundur; yağış ani bir olay olduğu için her seçim bir miktar hata taşır.

- [official] pandas.DataFrame.interpolate: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.interpolate.html

### Günlükten aylığa: resample

Model aylık çalıştığı için günlük veri `resample("MS")` ile ay başlarına göre gruplanır. Yağış ve ET0 birer miktar (mm) olduğundan `sum()` ile toplanır; sıcaklık gibi bir durum büyüklüğü olsaydı `mean()` kullanılırdı. Bu ayrım, zaman serisi dönüşümlerindeki en yaygın hatayı önler.

- [official] pandas: zaman serilerinde yeniden örnekleme: https://pandas.pydata.org/docs/user_guide/timeseries.html#resampling

### İlk grafik ve kaydetme

Aylık yağış çubuk, ET0 çizgi olarak aynı grafikte gösterilir: yağış kışın, buharlaşma yazın yoğunlaşır. İleri alıştırmada her takvim ayının ortalaması alınarak aylık klimatoloji çıkarılır. Temiz seri `to_csv` ile `data/processed/tahtali_monthly.csv` dosyasına kaydedilir ve Gün 2'de kullanılır.

- [official] pandas.DataFrame.to_csv: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html

### Zaman kalırsa: Temizliğimiz ne kadar iyiydi?

Bozulmamış orijinal dosya elimizde olduğu için temizlenen aylık veri onunla karşılaştırılır. Toplam hata %1'in altında kalır ama tek bir ayda yağış onlarca mm sapabilir, çünkü eksik bırakılan gün yağmurlu bir gün olabilir. İleri alıştırmada eksik yağış günlerini `fillna(0)` ile doldurmanın farkı ölçülür.

## Gün 2: Model Kurulumu

Temiz aylık veriyle Tahtalı Barajı'nın su bütçesi modeli sıfırdan yazılır ve gözlemlerle karşılaştırılır. Kaynaklardan alınan parametrelerle model 2022–2025 kuraklığının derinliğini yakalayamaz. Duyarlılık analizi bunun nedenini gösterir: sonuç, belirsiz iki parametreye son derece hassastır.

- [official] Gün 2 notebook'u (Colab): https://colab.research.google.com/github/mehmetalibeylikci/python-cevresel-modelleme/blob/main/notebooks/02_model_kurulumu.ipynb
- [official] Parametreler ve kaynakları: https://github.com/MehmetaliBeylikci/python-cevresel-modelleme/blob/main/docs/parametreler.md

### Kavramsal model: baraj bir kovadır

Baraj, havzadan gelen akış ve göle düşen yağmurla dolan; buharlaşma, şehre verilen su ve taşmayla boşalan bir kova olarak düşünülür. Kütle korunumu bunu tek bir denkleme çevirir: ay sonundaki su = ay başındaki su + giren − çıkan. Depolama ölü hacmin (19,6 hm³) altına inemez, normal kottaki hacmin (306,65 hm³) üstüne çıkamaz.

- [official] Parametreler ve kaynakları: https://github.com/MehmetaliBeylikci/python-cevresel-modelleme/blob/main/docs/parametreler.md
- [official] FAO-56: Bitki su tüketimi (ET0 yöntemi): https://www.fao.org/4/x0490e/x0490e00.htm

### Birimler: en sık hata kaynağı

Yağış mm, alan km², hacim hm³ (milyon m³) cinsindendir. 1 mm × 1 km² = 1000 m³ = 0,001 hm³ dönüşümü modelin her satırında kullanılır. Bu hesapla, havzadan gelen suyun göle doğrudan düşen yağmurdan yaklaşık yedi kat fazla olduğu görülür.

### Modeli yazalım

Model önce Eylül 2019 için elle, tek adım olarak hesaplanır. Sonra aynı adım bir `for` döngüsüne, döngü de tekrar kullanılabilir bir fonksiyona dönüştürülür. Yazılan fonksiyon, repodaki test edilmiş sürümle (`src/model.py`) karşılaştırılarak doğrulanır.

- [official] Test edilmiş model kodu (src/model.py): https://github.com/MehmetaliBeylikci/python-cevresel-modelleme/blob/main/src/model.py

### Önce tek bir ay

Başlangıç depolaması, Ağustos 2019 ortasındaki %76'lık İZSU gözleminden hesaplanır. Eylül 2019'un yağışı ve ET0'ı ile giren su, buharlaşma ve çekim tek tek hesaplanıp ay sonu depolaması bulunur. Eylül kurak bir ay olduğu için çıkan su gireni aşar ve seviye düşer.

### Bir döngü ve bir fonksiyon

`my_simulate` fonksiyonu her ay için giren suyu ve buharlaşmayı hesaplar, depolamayı günceller ve sınırları uygular: depolama üst sınırı aşarsa fazlası taşma olarak kaydedilir, alt sınırın altına inerse ölü hacme eşitlenir. Parametreler varsayılan değerli argümanlar olduğu için aynı fonksiyon farklı senaryolarla tekrar tekrar çağrılabilir.

### Model gerçeğe yakın mı?

Model çıktısı, farklı kaynaklardan derlenen birkaç doluluk gözlemiyle karşılaştırılır. Temel parametrelerle modelde doluluk hiç %40'ın altına inmez; gerçekte Ağustos 2025'te %7,45'e düşmüştü. Modeli çöpe atmadan önce sorulması gereken soru: parametrelerden ne kadar eminiz?

### Duyarlılık analizi

Akış katsayısı (C) ve aylık çekim (W) bir aralıkta taranır ve her kombinasyon için model yeniden çalıştırılır; sonuç seaborn ile bir ısı haritasında gösterilir. C'deki 0,05'lik bir değişiklik bile barajı "boş" ile "dolu" arasında gidip getirir. Gözlemle uyumlu kombinasyonlar dar bir köşegen şerit oluşturur: birkaç gözlem iki parametreyi ayrı ayrı belirlemeye yetmez (eşsonuçluluk).

- [official] dataclasses.replace: https://docs.python.org/3/library/dataclasses.html#dataclasses.replace
- [official] seaborn.heatmap: https://seaborn.pydata.org/generated/seaborn.heatmap.html

### İnteraktif keşif (ipywidgets)

ipywidgets'ın `interact` fonksiyonu, model fonksiyonunu kaydırma çubuklarına bağlar. C ve W değiştirildikçe doluluk grafiği anında yeniden çizilir; parametre hassasiyeti böylece sezgisel olarak görülür. Colab'da çubuklar hücre çalıştırıldıktan sonra görünür.

- [official] ipywidgets belgeleri: https://ipywidgets.readthedocs.io/en/stable/

### Tartışma: modelin varsayımları

Model neden gerçeği tam yakalayamıyor? Tek bir ERA5 hücresinin 546 km²'lik havzayı temsil etmesi, sabit akış katsayısı, sabit çekim, sabit göl alanı ve sızma ile yeraltı suyu gibi eksik süreçler tartışılır. Bu eksikleri bilmek modeli değersiz kılmaz; modelin hangi sorulara cevap verebileceğini belirler.

### Zaman kalırsa: Depolamaya bağlı göl alanı

Gerçekte göl, baraj boşaldıkça küçülür ve buharlaşma azalır. Göl alanı depolamanın 2/3 kuvvetiyle ölçeklenerek (hacim üç, alan iki boyutludur) modele eklenir ve sabit alanlı modelle aynı grafikte karşılaştırılır.

## Gün 3: Görselleştirme ve Senaryolar

Mutlak tahmin için güvenilir olmayan model, "ya şöyle olursa?" sorusu için kullanılır. İklim ve talep senaryoları kurulur, sonuçlar tek bir metrikle özetlenir ve anlaşılır, dürüst, sunuma hazır grafiklerle anlatılır. Gün, modelin neyi söyleyip neyi söyleyemeyeceğinin tartışmasıyla kapanır.

- [official] Gün 3 notebook'u (Colab): https://colab.research.google.com/github/mehmetalibeylikci/python-cevresel-modelleme/blob/main/notebooks/03_gorsellestirme_senaryolar.ipynb
- [official] matplotlib hızlı başlangıç: https://matplotlib.org/stable/users/explain/quick_start.html

### matplotlib anatomisi

matplotlib'de her grafik iki nesneden oluşur: `fig` kâğıdın kendisi, `ax` üzerindeki grafik alanıdır. Başlıksız, birimsiz, lejantsız ve ilgisiz büyüklükleri aynı eksende gösteren kötü bir grafik adım adım düzeltilir. Altın kural: her grafik tek bir soruya cevap vermelidir.

- [official] matplotlib hızlı başlangıç: https://matplotlib.org/stable/users/explain/quick_start.html

### Senaryolar: iklim ve talep

IPCC'nin Akdeniz raporundaki eğilimler üç basit çarpanla temsil edilir: yağış −%20, ET0 +%10 ve çekim +%15. Her senaryo aynı modele farklı girdi vermekten ibarettir ve bir sözlükte tanımlanır. Sonuçlar "kritik seviyenin altında geçen ay sayısı" gibi anlaşılır bir metrikle karşılaştırılır.

- [official] IPCC AR6, Akdeniz bölgesi (Cross-Chapter Paper 4): https://www.ipcc.ch/report/ar6/wg2/chapter/ccp4/

### Sunuma hazır figürler

Statik grafikler rapor ve sunum için, interaktif grafikler keşif içindir. Bu bölümde üç figür üretilir: hikâye anlatan çok panelli bir figür, mevsimsel ve yıllar arası yapıyı birlikte gösteren bir ısı haritası ve üzerine gelince değer gösteren interaktif bir grafik.

### Çok panelli figür

`plt.subplots(3, 1, sharex=True)` ile aynı zaman eksenini paylaşan üç panel bir hikâye anlatır: baraj ne durumda, neden ve senaryolar ne diyor. Figür `savefig(..., dpi=200)` ile yüksek çözünürlükte kaydedilir.

- [official] matplotlib.pyplot.subplots: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html

### Mevsimsel ısı haritası (seaborn)

Satırları yıllar, sütunları aylar olan bir ısı haritası, doluluğun hem mevsimsel hem yıllar arası değişimini tek bakışta gösterir. Renk ölçeği `vmin=0, vmax=100` ile sabitlenir; böylece farklı senaryoların haritaları birbiriyle karşılaştırılabilir. Kırmızı tehlikeyi, mavi suyu çağrıştırır.

- [official] seaborn.heatmap: https://seaborn.pydata.org/generated/seaborn.heatmap.html

### İnteraktif grafik (plotly)

plotly ile çizilen grafiklerde bir çizginin üzerine gelince değer görünür, yakınlaştırma yapılabilir ve lejanttaki bir senaryoya tıklanarak o çizgi gizlenebilir. Keşif aşamasında statik grafiklerden çok daha hızlı sonuç verir.

- [official] plotly: Python'da çizgi grafikleri: https://plotly.com/python/line-charts/

### Kapanış: model neyi söyleyebilir?

Model, su bütçesinin hangi bileşenlerinin önemli olduğunu ve senaryoların birbirine göre ne kadar tehlikeli olduğunu söyleyebilir. Barajın gelecek ay tam olarak kaç hm³ olacağını ya da yağış dağılımındaki değişimin etkisini söyleyemez. Sıradaki adımlar: NetCDF ve xarray ile gerçek iklim projeksiyonları, bonus ML modülü ve aynı yöntemi kendi probleminize uygulamak.

- [official] xarray belgeleri: https://docs.xarray.dev/en/stable/

### Zaman kalırsa: Kendi senaryonuz

Kendi senaryonuzu tasarlayıp sonucunu grupla paylaşın: örneğin kuraklıkta çekimin %30 azaltılması ya da talebin her yıl biraz artması. Senaryo, mevcut sözlüğe yeni bir girdi eklenerek tanımlanır.

### Zaman kalırsa: Sonuçlar parametrelere ne kadar bağlı?

Senaryo karşılaştırması farklı bir parametre setiyle (örneğin C = 0,20, W = 8,0) tekrarlanır. Mutlak değerler değişse bile senaryoların birbirine göre sıralaması korunuyorsa, sonuç parametre belirsizliğine karşı sağlamdır.

## Bonus: Fizik mi, Veri mi?

Aynı problem bir makine öğrenmesi modeliyle çözülür ve SHAP ile modelin neye baktığı açılır. Tahtalı'nın geçmiş doluluk serisi açık olmadığı için ML modeli gözlemlere değil fiziksel modelin çıktısına eğitilir; amaç ML'nin elle yazılan fiziği veriden yeniden keşfedip keşfedemeyeceğini görmektir. Ön koşul: Gün 1 ve Gün 2. Kendi başına yaklaşık 1,5 saat.

- [official] Bonus notebook'u (Colab): https://colab.research.google.com/github/mehmetalibeylikci/python-cevresel-modelleme/blob/main/bonus/fizik-mi-veri-mi/fizik_mi_veri_mi.ipynb

### Hedef ve özellikler

Hedef (y), bir aydaki depolama değişimidir (ΔS, hm³). Özellikler (X), o ayın yağışı, ET0'ı ve takvim ayıdır. Baraj taşmadığı ve ölü hacme inmediği sürece fiziksel modelde ΔS bu üç bilgiyle belirlenir.

### Zamana göre eğitim/test ayrımı

Zaman serilerinde eğitim ve test verisi rastgele ayrılmaz: rastgele ayırmak, modelin test ayının öncesini ve sonrasını görmesine yol açar (bilgi sızıntısı). Doğrusu geçmişle eğitmek, gelecekle test etmektir; burada 2024 öncesi eğitim, sonrası test için kullanılır.

- [official] scikit-learn: zaman serisi çapraz doğrulama (TimeSeriesSplit): https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

### Random Forest (scikit-learn)

Random Forest, çok sayıda karar ağacının ortalamasını alan bir modeldir; scikit-learn'de her model oluştur → `fit` → `predict` adımlarıyla çalışır. Model en çok, eğitimde benzeri az görülen çok yağışlı aylarda yanılır ve eğitimde görmediği aralığa çıkamaz (dışdeğerleme yapamaz). Fiziksel denklemde böyle bir sınır yoktur.

- [official] sklearn.ensemble.RandomForestRegressor: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html

### SHAP: model neye bakıyor?

SHAP, her tahmini özelliklerin katkılarına ayırır: "bu ayın tahmini +5 hm³; +7'si yağıştan, −2'si ET0'dan". Beeswarm grafiği özelliklerin genel önemini, scatter grafiği yağışın etkisinin şeklini gösterir. ML modelinin öğrendiği yağış eğimi, fiziksel modeldeki katsayıyla (yaklaşık 0,18 hm³/mm) karşılaştırılır.

- [official] SHAP belgeleri: https://shap.readthedocs.io/en/latest/

### Tartışma ve AutoML notu

ML modeli yağışın etkisini neredeyse birebir bulur, ama yalnızca eğitimde gördüğü aralıkta; taşma gibi eşik davranışlarını depolama bilgisi verilmeden öğrenemez. Az veri ve bilinen süreçler fiziksel modelleri, çok veri ve karmaşık süreçler ML'yi öne çıkarır; modern çalışmalar ikisini birleştirir. PyCaret gibi AutoML araçları hızlı bir ilk bakış sunar, ama neyin neden seçildiği anlaşılmadan alınan "en iyi skor" yanıltıcı olabilir.

- [official] PyCaret (GitHub): https://github.com/pycaret/pycaret
