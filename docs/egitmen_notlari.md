# Eğitmen Notları

Bu belge, eğitimi verecek kişi için hazırlandı. Her gün için hazırlık listesi, akış, sık karşılaşılan hatalar ve tartışma sorularının olası cevapları var.

## Genel hazırlık (eğitimden 1 hafta önce)

- [ ] Gün 0 notebook'unun Colab bağlantısını katılımcılara gönderin. Cümleniz şu olabilir: "Eğitimden önce 1 saatinizi ayırın; en sondaki 5 görevi yapabiliyorsanız hazırsınız."
- [ ] Her notebook'u **gerçek bir Colab oturumunda** baştan sona çalıştırın ve süre tutun. Bulguları aşağıdaki "Prova bulguları" bölümüne yazın.
- [ ] Katılımcıların bir Google hesabı olduğundan emin olun (Colab için gerekli).
- [ ] Sınıftaki internet bağlantısını kontrol edin. İlk hücre repoyu GitHub'dan indirir (~birkaç MB).
- [ ] Takılan katılımcılar için sınıfta en az bir yardımcı bulunması çok işe yarar.

## Her günün başında

1. Katılımcılara günün notebook'unun Colab bağlantısını verin (README'deki rozetler).
2. **İlk hücreyi** (Kurulum) herkesin çalıştırdığından emin olun.
3. "Dosya → Drive'a kopya kaydet" adımını gösterin; yoksa değişiklikleri kaybolur.

---

## Gün 0 — Ön hazırlık

Katılımcının kendi başına yaptığı bir bölüm. Gün 1'in ilk 5 dakikasında kısaca sorun: "Görev 5'i kim yapabildi?" Cevap, grubun seviyesi hakkında hızlı bir fikir verir.

## Gün 1 — Veri hazırlama

| Süre | Konu | Not |
|---|---|---|
| 0–15 | Problem, folium haritası, terim sözlüğü | 2025 krizinden bir haber başlığı göstermek ilgiyi artırır |
| 15–45 | pandas temelleri | `info()` çıktısında `date` sütununun türüne dikkat çekin |
| 45–55 | Sweetviz | Rapor oluşturmak ~10 saniye sürer. Colab'da `report.show_notebook()` satırını açın |
| 55–90 | Temizlik | Günün kalbi; acele etmeyin |
| 90–105 | `resample` | `sum` ve `mean` farkını mutlaka tartışın |
| 105–120 | Grafik, kaydetme | Kaydetme hücresini herkes çalıştırmalı |

**Sık karşılaşılan hatalar**

- `FileNotFoundError: data/raw/...`: Kurulum hücresi çalıştırılmamış. Önce o çalıştırılmalı.
- `KeyError: 'date'`: `set_index("date")` iki kez çalıştırılmış. Çözüm: "Çalışma zamanı → Tümünü çalıştır".
- Alıştırma 2'de 2026'nın da düşük görünmesi: 2026 yalnızca 9 ay. `.loc[:2025]` kullanımını gösterin.
- `resample` hatası (`Only valid with DatetimeIndex`): indeks tarih değil. 4.2'deki `set_index` adımı atlanmış.

**Tartışma soruları**

- *`describe()` çıktısında tuhaf olan ne?* Negatif minimum yağış ve 900 mm maksimum.
- *Yağış ve ET0 hangi aylarda yoğun?* Yağış kışın, ET0 yazın. Baraj kışın dolar, yazın hem buharlaşma hem tüketim nedeniyle boşalır.
- *Neden tek bir ayda ~29 mm fark var?* Silinen gün yağmurlu bir gündü; interpolasyon komşu (kuru) günlere bakarak onu geri getiremez.

**Zaman yetmezse:** Sweetviz bölümünü kısaltın (sadece raporu gösterin), "Zaman kalırsa" bölümünü atlayın.

## Gün 2 — Model kurulumu

| Süre | Konu | Not |
|---|---|---|
| 0–15 | Kova çizimi, kütle korunumu | Tahtaya çizmek, ekrandaki ASCII çizimden daha etkili |
| 15–50 | `my_simulate` | Birlikte, satır satır yazın. `assert` hücresinin yeşil olması güzel bir an |
| 50–70 | Gözlemlerle karşılaştırma | **Günün en önemli anı:** model kuraklığı yakalayamıyor |
| 70–100 | Duyarlılık, ipywidgets | Kaydırma çubuklarıyla oynamaları için 5 dakika verin |
| 100–120 | Tartışma | Varsayımlar listesini birlikte tamamlayın |

**"Model tutmadı" anını nasıl yönetmeli?** Bunu bir başarısızlık gibi değil, bir **bulgu** gibi sunun. Gerçek modelcilik böyledir: model gözlemlere uymuyorsa ya model yapısı ya da parametreler eksiktir. Duyarlılık analizi bize hangisinin daha olası olduğu hakkında ipucu verir. Katılımcılara sorun: "Sizce hangi parametre en şüpheli?"

**Sık karşılaşılan hatalar**

- `my_simulate` içinde `spill` tanımsız hatası: `spill = 0.0` satırı `if` bloğunun **önüne** yazılmalı.
- `assert np.allclose` başarısız: en sık sebep birim dönüşümünün (`* MM_KM2_TO_HM3`) unutulması ya da göle düşen yağışın eklenmemesi.
- ipywidgets çubukları görünmüyor: Colab'da hücreyi yeniden çalıştırın. Yerel Jupyter'de `ipywidgets` kurulu olmalı.

**Tartışma soruları**

- *Neden havzadan gelen su, göle düşenden 8 kat fazla?* Havza alanı (546 km²) göl alanının (23,5 km²) ~23 katı; akış katsayısı 0,33 olunca 23 × 0,33 ≈ 7,7.
- *Isı haritasındaki köşegen ne anlatıyor?* Yüksek C ile yüksek W birbirini dengeliyor. Gözlemler ikisini ayrı ayrı belirlemeye yetmiyor (eşsonuçluluk).
- *Neden en iyi RMSE'yi seçip "kalibre ettik" demiyoruz?* 4 gözlem, 2 parametre, farklı kaynaklar. Uyum, açıklama gücü anlamına gelmez.

**Zaman yetmezse:** RMSE alıştırmasını (🔵 Alıştırma 3) atlayın; ipywidgets bölümünü eğitmen olarak siz gösterin.

## Gün 3 — Görselleştirme ve senaryolar

| Süre | Konu | Not |
|---|---|---|
| 0–30 | `fig`/`ax`, kötü grafiği düzeltme | Katılımcılara "bu grafikte ne yanlış?" diye sorun, cevapları toplayın |
| 30–70 | Senaryolar | Tabloyu yorumlamaya zaman ayırın |
| 70–100 | Çok panelli figür, ısı haritası, plotly | Çok panelli figür uzun; hazır kodu birlikte okuyun, satır satır yazdırmayın |
| 100–120 | Kapanış | Herkesin kendi senaryosunu kurup sonucunu söylemesi güzel bir kapanış olur |

**Sık karşılaşılan hatalar**

- `ModuleNotFoundError: No module named 'src'`: Kurulum hücresi çalıştırılmamış.
- plotly grafiği görünmüyor: yerel Jupyter'de ek ayar gerekebilir; Colab'da sorunsuz çalışır.

**Tartışma soruları**

- *Hangi değişiklik en tehlikeli?* Temel parametrelerle yağıştaki %20'lik düşüş, talepteki %15'lik artıştan ve ET0'daki %10'luk artıştan daha etkili. Hepsi birlikte olduğunda baraj defalarca kritik seviyenin altına iniyor.
- *Sıralama parametrelere bağlı mı?* 🔵 Alıştırma 5'te C = 0,20, W = 8 ile denendiğinde mutlak sayılar çok değişiyor, ama sıralama (kurak > yüksek talep > sıcak) aynı kalıyor. Model belirsiz olsa bile göreli sonuçlar daha sağlam.

**Zaman yetmezse:** plotly bölümünü atlayın; ısı haritasında yalnızca kurak senaryoyu gösterin.

---

## Bonus modül

Ders saatinde işlenmez. Kapanışta tanıtın ve ilgilenenlere bağlantıyı verin. Modülün dürüstlük notunu (hedef değişkenin model çıktısı olduğunu) mutlaka vurgulayın.

## Prova bulguları

*Eğitmen, notebook'ları gerçek bir Colab oturumunda çalıştırdıktan sonra buraya not alır: her bölümün gerçek süresi, takılınan yerler, Colab'a özgü sorunlar.*

| Tarih | Notebook | Bulgu |
|---|---|---|
| | | |
