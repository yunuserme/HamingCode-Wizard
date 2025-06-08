# **Hamming SEC-DED Kod Simülatörü**

Bu uygulama, BLM230 Bilgisayar Mimarisi dersi kapsamında geliştirdiğim, Hamming hata düzeltme kodlarını interaktif olarak öğrenme ve test etme amaçlı Python tabanlı bir simülatördür.

## 🔄 Temel Özellikleri

* **Çoklu Veri Boyutu Desteği**: 8, 16 veya 32-bit verilerle çalışabilme
* **Anlık Görselleştirme**: Kodlanmış verinin bit düzeyinde gösterimi
* **Hata Simülasyonu**: Manuel veya otomatik hata enjeksiyonu
* **Hata Düzeltme**: SEC-DED (Single Error Correction, Double Error Detection) özelliği

## 🎨 Görsel Öğeler

* **◻️ Mavi**: Veri bitleri
* **◼️ Yeşil**: Parity bitleri
* **🟨 Sarı**: Genel parity biti (SEC-DED için)
* **⭕ Kırmızı**: Hatalı olarak işaretlenen bit

## 💻 Sistem Gereksinimleri

* **Python**: 3.x veya üzeri sürüm
* **İşletim Sistemi**: Windows 10/11, macOS, Linux
* **Ek Paketler**: Tkinter (genellikle Python ile birlikte gelir)
* **Disk Alanı**: ~5MB

## 🛠️ Kurulum Adımları

1. Proje dosyalarını bilgisayarınıza kopyalayın:
```
git clone https://github.com/ogrenci/hamming-simulator.git
```

2. Proje dizinine gidin:
```
cd hamming-simulator
```

3. Uygulamayı başlatın:
```
python hamming_arayuz.py
```

## 📝 Çalışma Mantığı

1. **Parity Bit Hesaplama**:
   * 2'nin kuvveti olan pozisyonlara parity bitleri yerleştirilir
   * Her parity biti, belirli bit pozisyonlarını kontrol eder
   * Formül: 2^r ≥ veri_uzunluğu + r + 1 (r: parity bit sayısı)

2. **Hata Tespit Mekanizması**:
   * Sendrom = 0, Genel Parity OK → Hata yok
   * Sendrom ≠ 0, Genel Parity Hatalı → Tek bit hatası (düzeltilir)
   * Sendrom = 0, Genel Parity Hatalı → Genel parity bit hatası
   * Sendrom ≠ 0, Genel Parity OK → Çift bit hatası (tespit edilir ama düzeltilemez)

## 📋 Kullanım Talimatları

1. **Boyut Seçimi**: İlk olarak veri uzunluğunu belirleyin
2. **Veri Oluşturma**: "Rastgele Veri" butonu ile otomatik veri oluşturun veya kendiniz giriş yapın
3. **Kod Oluşturma**: "Hamming Kodu Hesapla" butonu ile veriyi kodlayın
4. **Hata Ekle**: "Hata Oluştur" butonu ile belirli bir bite hata ekleyin
5. **Düzeltme**: "Hatayı Tespit Et/Düzelt" butonu ile hata analizi yapın

## 💡 Örnek Kullanım Senaryoları

### Örnek 1: Veri Biti Hatası
* 8-bit veri girin (örn: `11001100`)
* Hamming kodunu hesaplayın
* Bir veri bitine hata ekleyin
* Hatayı tespit edin ve düzeltin

### Örnek 2: Parity Bit Hatası
* 16-bit veri oluşturun
* Hamming kodunu hesaplayın
* Bir parity bitinde hata oluşturun
* Sistemin bu hatayı da düzelttiğini görün

### Örnek 3: Çoklu Hata Senaryosu
* 8-bit veri ile başlayın
* İki farklı bit pozisyonunda hata oluşturun
* Sistemin çift hata tespiti yaptığını görün

## 🧩 Yazılım Mimarisi

* **hamming_core.py**: Algoritma kütüphanesi
  * `hamming_kod_hesapla()`: Kodlama algoritması
  * `sendrom_hesapla()`: Hata pozisyonu belirleyici
  * `hata_olustur()`: Bit hatası enjektörü
  * `hata_duzelt()`: Hata tespit ve düzeltme mekanizması

* **hamming_arayuz.py**: Kullanıcı arayüzü
  * Tkinter tabanlı GUI yapısı
  * Bit görselleştirme sistemi
  * Kullanıcı etkileşim kontrolcüleri

## 🎯 Eğitimsel Faydalar

* Hamming kodunun matematiksel temellerini anlama
* Bit manipülasyonu ve bitwise operatörleri kavrama
* Hata tespiti ve düzeltme algoritmaları hakkında bilgi edinme
* Bilgisayar belleğinde hata toleransının önemini öğrenme

## 🌟 Benzersiz Özellikler

* ⚡ Hızlı ve hafif tasarım
* ⚡  Eğitim odaklı görsel geri bildirim
* ⚡  Adım adım simülasyon imkanı
* ⚡ Detaylı sonuç analizi
* ⚡ Özelleştirilebilir hata senaryoları
* ⚡  Duyarlı arayüz tasarımı

## 📊 Teknik Performans

* **İşlem Hızı**: Milisaniyeler içinde kod hesaplama
* **Hata Oranı**: %100 tek bit hata düzeltme
* **Doğruluk**: %100 çift bit hata tespiti
* * **Doğruluk**: İstediğin bitte hata yaratma ve düzeltme desteği

## 📚 Teorik Altyapı

Hamming SEC-DED kodu, Richard Hamming tarafından 1950'lerde Bell Laboratuvarlarında geliştirilmiş ve bilgisayar belleğinde, veri iletiminde ve depolamada yaygın olarak kullanılan bir hata düzeltme kodudur. Parity bitleri ekleyerek tek bit hatalarını düzeltebilir ve çift bit hatalarını tespit edebilir.

## 📝 Geliştirme Süreci

Bu projeyi geliştirirken önce Hamming kodunun matematiksel temelini anlamaya çalıştım, daha sonra algoritmaları Python'da uyguladım ve son olarak kullanıcı dostu bir arayüz ekledim. Tkinter'in Canvas özelliğini kullanarak bitlerin görsel temsilini oluşturmak en zorlayıcı kısımdı.

* [Hamming Kodu Teorisi](https://en.wikipedia.org/wiki/Hamming_code)
* [Bilgisayar Belleğinde ECC](https://en.wikipedia.org/wiki/ECC_memory)
* [Python Bitwise İşlemler](https://wiki.python.org/moin/BitwiseOperators)



## 🎬 Video Tanıtım

Programın kullanımını gösteren video için aşağıdaki bağlantıyı ziyaret edebilirsiniz:
[Hamming Simülatörü Tanıtım Videosu](https://www.youtube.com/your-video-link)

