def hamming_kod_hesapla(veri_str, veri_uzunlugu):
    # String'i bite çeviriyoruz
    veri = [int(bit) for bit in veri_str]
    
    # Parity bit sayısını bulalım
    r = 0
    while 2**r < veri_uzunlugu + r + 1:
        r += 1
    
    # Toplam kaç bit olacak onu hesaplayalım
    kodlanmis_uzunluk = veri_uzunlugu + r + 1
    kodlanmis = [0] * kodlanmis_uzunluk
    
    # Veri bitlerini yerleştiriyoruz, ama parity bitlerine dikkat
    veri_idx = 0
    for i in range(1, kodlanmis_uzunluk):
        # 2'nin kuvveti mi diye bakıyoruz, parity bitlerini atlamak için
        if not (i & (i-1) == 0):
            if veri_idx < len(veri):
                kodlanmis[i-1] = veri[veri_idx]
                veri_idx += 1
    
    # Şimdi parity bitleri hesaplayalım
    for i in range(r):
        parity_poz = 2**i - 1
        parity = 0
        for j in range(kodlanmis_uzunluk):
            if (j+1) & (2**i) and j != kodlanmis_uzunluk-1:
                parity ^= kodlanmis[j]
        kodlanmis[parity_poz] = parity
    
    # Son olarak genel parity bitini hesaplıyoruz
    genel_parity = 0
    for i in range(kodlanmis_uzunluk-1):
        genel_parity ^= kodlanmis[i]
    kodlanmis[kodlanmis_uzunluk-1] = genel_parity
    
    return kodlanmis

def hata_olustur(kodlanmis, pozisyon):
    # Burada seçilen biti tersine çeviriyoruz (0->1 veya 1->0)
    if 0 <= pozisyon < len(kodlanmis):
        hatali_veri = kodlanmis.copy()
        hatali_veri[pozisyon] = 1 - hatali_veri[pozisyon]
        return hatali_veri
    return kodlanmis

def sendrom_hesapla(kodlanmis):
    uzunluk = len(kodlanmis)
    
    # Kaç tane parity bit var acaba?
    r = 0
    while 2**r < uzunluk:
        r += 1
    
    # Önce genel parity'i kontrol edelim
    genel_parity_check = 0
    for bit in kodlanmis:
        genel_parity_check ^= bit
    
    # Şimdi sendromu hesaplayalım, sendrom hata pozisyonunu verecek
    sendrom = 0
    for i in range(r-1):
        parity_poz = 2**i - 1
        parity_check = 0
        for j in range(uzunluk-1):
            if (j+1) & (2**i):
                parity_check ^= kodlanmis[j]
        if parity_check != 0:
            sendrom += 2**i
    
    return sendrom, genel_parity_check != 0

def hata_duzelt(kodlanmis):
    # Hata tespiti için sendromu hesaplıyoruz
    sendrom, genel_parity_hatasi = sendrom_hesapla(kodlanmis)
    
    duzeltilmis = kodlanmis.copy()
    hata_biti = -1
    
    # Burası kritik, hangi hata durumu var karar veriyoruz
    if sendrom == 0 and not genel_parity_hatasi:
        # Hata yokmuş, oh be
        hata_mesaji = "Hata tespit edilmedi."
    elif sendrom != 0 and genel_parity_hatasi:
        # Tek bit hatası bulundu, düzeltebiliriz
        hata_biti = sendrom - 1
        if 0 <= hata_biti < len(duzeltilmis):
            duzeltilmis[hata_biti] = 1 - duzeltilmis[hata_biti]
            hata_mesaji = f"Tek bit hatası pozisyon {hata_biti}'de tespit edildi ve düzeltildi."
        else:
            hata_mesaji = "Geçersiz hata pozisyonu."
    elif sendrom == 0 and genel_parity_hatasi:
        # Genel parity bitinde hata var
        hata_mesaji = "Genel parity bitinde hata tespit edildi."
        hata_biti = len(duzeltilmis) - 1
        duzeltilmis[-1] = 1 - duzeltilmis[-1]
    else:
        # Eyvah, çift bit hatası - düzeltemeyiz :(
        hata_mesaji = "Çift bit hatası tespit edildi (düzeltilemez)."
    
    return duzeltilmis, hata_mesaji, sendrom, hata_biti

def veri_cikar(kodlanmis, veri_uzunlugu):
    # Şimdi parity bitleri atmamız lazım, sadece veriyi almak için
    veri = []
    veri_idx = 0
    
    for i in range(1, len(kodlanmis)):
        # 2'nin kuvveti pozisyonlar parity bit, onları atlıyoruz
        if not (i & (i-1) == 0):
            if veri_idx < veri_uzunlugu:
                veri.append(kodlanmis[i-1])
                veri_idx += 1
    
    return veri[:veri_uzunlugu]     