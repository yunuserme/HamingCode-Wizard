import tkinter as tk
from tkinter import ttk, messagebox
import random
from hamming_core import hamming_kod_hesapla, hata_olustur, hata_duzelt, veri_cikar

class HammingSimulatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hamming SEC-DED Kod Simülatörü")
        self.geometry("900x650")
        self.configure(bg="#f0f0ff")  # Açık mavi-gri arkaplan
        
        # Değişkenleri tanımlıyoruz
        self.veri_uzunluk = tk.IntVar(value=8)
        self.random_hata = tk.BooleanVar(value=True)
        self.hata_poz = tk.IntVar(value=0)
        self.kodlanmis_veri = []
        
        self.arayuz_olustur()
        
    def arayuz_olustur(self):
        # Ana frame'i oluşturuyoruz
        main_frame = tk.Frame(self, bg="#f0f0ff", padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık koyuyoruz
        baslik = tk.Label(main_frame, text="Hamming SEC-DED Kod Simülatörü", 
                           font=("Arial", 18, "bold"), bg="#f0f0ff", fg="#2c3e50")
        baslik.pack(pady=(0, 20))
        
        # Üst paneli oluşturuyoruz - buraya giriş alanları gelecek
        ust_panel = tk.Frame(main_frame, bg="#e0e0f5", relief=tk.RAISED, bd=2)
        ust_panel.pack(fill=tk.X, padx=10, pady=10)
        
        # Veri uzunluğu seçenekleri
        uzunluk_frame = tk.LabelFrame(ust_panel, text="Veri Uzunluğu", bg="#e0e0f5", fg="#2c3e50", font=("Arial", 10, "bold"))
        uzunluk_frame.pack(fill=tk.X, padx=15, pady=(10, 5))
        
        for uzunluk, text in [(8, "8 bit"), (16, "16 bit"), (32, "32 bit")]:
            rb = tk.Radiobutton(uzunluk_frame, text=text, variable=self.veri_uzunluk, 
                               value=uzunluk, bg="#e0e0f5", fg="#2c3e50", 
                               selectcolor="#c0c0f0", font=("Arial", 9))
            rb.pack(side=tk.LEFT, padx=20, pady=5)
        
        # Veri giriş alanı
        veri_frame = tk.LabelFrame(ust_panel, text="Veri Girişi", bg="#e0e0f5", fg="#2c3e50", font=("Arial", 10, "bold"))
        veri_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self.veri_entry = tk.Entry(veri_frame, font=("Consolas", 11), width=40)
        self.veri_entry.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Button(veri_frame, text="Rastgele Veri", command=self.random_veri_olustur, 
                 bg="#4a86e8", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=5, pady=10)
        
        # Hata oluşturma ayarları
        hata_frame = tk.LabelFrame(ust_panel, text="Hata Oluşturma", bg="#e0e0f5", fg="#2c3e50", font=("Arial", 10, "bold"))
        hata_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Checkbutton(hata_frame, text="Rastgele Hata", variable=self.random_hata, 
                      bg="#e0e0f5", fg="#2c3e50", selectcolor="#c0c0f0", 
                      font=("Arial", 9)).pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Label(hata_frame, text="Hata Pozisyonu:", bg="#e0e0f5", fg="#2c3e50", 
                font=("Arial", 9)).pack(side=tk.LEFT, padx=(20, 5), pady=5)
        
        self.poz_spinbox = tk.Spinbox(hata_frame, from_=0, to=38, textvariable=self.hata_poz, 
                                     width=5, font=("Arial", 9))
        self.poz_spinbox.pack(side=tk.LEFT, padx=5, pady=5)
        
        # İşlem butonları
        buton_frame = tk.Frame(ust_panel, bg="#e0e0f5")
        buton_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Button(buton_frame, text="Hamming Kodu Hesapla", command=self.hamming_hesapla,
                 bg="#4a86e8", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Button(buton_frame, text="Hata Oluştur", command=self.hata_olustur,
                 bg="#e67c73", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Button(buton_frame, text="Hatayı Tespit Et/Düzelt", command=self.hata_tespit,
                 bg="#57bb8a", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Bitleri gösterme alanı
        bit_frame = tk.LabelFrame(main_frame, text="Bit Gösterimi", bg="#e0e0f5", fg="#2c3e50", font=("Arial", 10, "bold"))
        bit_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Canvas üzerinde bitleri göstereceğiz
        self.bit_canvas = tk.Canvas(bit_frame, height=80, bg="white", bd=1, relief=tk.SUNKEN)
        self.bit_canvas.pack(fill=tk.X, padx=10, pady=10)
        
        # Sonuçları gösterdiğimiz kısım
        sonuc_frame = tk.LabelFrame(main_frame, text="Simülasyon Sonuçları", bg="#e0e0f5", fg="#2c3e50", font=("Arial", 10, "bold"))
        sonuc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Grid layout için frame
        sonuc_grid = tk.Frame(sonuc_frame, bg="#e0e0f5")
        sonuc_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sonuçlar için etiketler ve giriş kutuları
        etiketler = ["Orijinal Veri:", "Hamming Kodu:", "Hatalı Veri:", "Sendrom:", "Düzeltilmiş Veri:", "Hata Biti (varsa):"]
        self.sonuc_kutulari = {}
        
        for i, etiket in enumerate(etiketler):
            tk.Label(sonuc_grid, text=etiket, bg="#e0e0f5", fg="#2c3e50", 
                    font=("Arial", 10, "bold"), anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            entry = tk.Entry(sonuc_grid, font=("Consolas", 10), width=60, bd=2, relief=tk.SUNKEN)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.sonuc_kutulari[etiket] = entry
        
        sonuc_grid.columnconfigure(1, weight=1)
        
        # En altta durum çubuğu
        self.status_bar = tk.Label(self, text="Hazır", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#d0d0f0", fg="#2c3e50")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def random_veri_olustur(self):
        # Rastgele 0 ve 1'lerden oluşan veri oluşturuyoruz
        uzunluk = self.veri_uzunluk.get()
        veri = ''.join(str(random.randint(0, 1)) for _ in range(uzunluk))
        self.veri_entry.delete(0, tk.END)
        self.veri_entry.insert(0, veri)
        self.status_bar.config(text=f"Rastgele {uzunluk} bit veri oluşturuldu")
    
    def hamming_hesapla(self):
        # Kullanıcının girdiği veriyi alıp hamming kodunu buluyoruz
        veri_str = self.veri_entry.get().strip()
        uzunluk = self.veri_uzunluk.get()
        
        # Önce basit kontroller yapıyoruz
        if not veri_str:
            messagebox.showerror("Hata", "Lütfen veri girin!")
            return
            
        if not all(bit in '01' for bit in veri_str):
            messagebox.showerror("Hata", "Veri sadece 0 ve 1 içermelidir!")
            return
            
        if len(veri_str) != uzunluk:
            messagebox.showerror("Hata", f"Veri uzunluğu {uzunluk} bit olmalıdır!")
            return
        
        # Hamming kodunu hesaplıyoruz
        self.kodlanmis_veri = hamming_kod_hesapla(veri_str, uzunluk)
        
        # Bitleri görsel olarak gösteriyoruz
        self.bitleri_goster(self.kodlanmis_veri)
        
        # Sonuçları ekrandaki kutucuklara yazıyoruz
        self.sonuc_kutulari["Orijinal Veri:"].delete(0, tk.END)
        self.sonuc_kutulari["Orijinal Veri:"].insert(0, veri_str)
        
        self.sonuc_kutulari["Hamming Kodu:"].delete(0, tk.END)
        self.sonuc_kutulari["Hamming Kodu:"].insert(0, ''.join(map(str, self.kodlanmis_veri)))
        
        # Diğer alanları temizleyelim
        self.sonuc_kutulari["Hatalı Veri:"].delete(0, tk.END)
        self.sonuc_kutulari["Sendrom:"].delete(0, tk.END)
        self.sonuc_kutulari["Düzeltilmiş Veri:"].delete(0, tk.END)
        self.sonuc_kutulari["Hata Biti (varsa):"].delete(0, tk.END)
        
        self.status_bar.config(text=f"Hamming SEC-DED kodu hesaplandı. Toplam {len(self.kodlanmis_veri)} bit.")
    
    def hata_olustur(self):
        # Kodda yapay hata oluşturuyoruz
        if not self.kodlanmis_veri:
            messagebox.showerror("Hata", "Önce Hamming kodunu hesaplamalısınız!")
            return
        
        # Hatanın nerede olacağını belirliyoruz
        if self.random_hata.get():
            # Rastgele bir yerde hata oluşturuyoruz
            hata_poz = random.randint(0, len(self.kodlanmis_veri)-1)
            self.hata_poz.set(hata_poz)
        else:
            # Kullanıcının seçtiği pozisyonda hata oluşturuyoruz
            hata_poz = self.hata_poz.get()
            if hata_poz >= len(self.kodlanmis_veri):
                messagebox.showerror("Hata", f"Hata pozisyonu 0-{len(self.kodlanmis_veri)-1} arasında olmalıdır!")
                return
        
        # Hata oluştur - seçilen biti tersine çeviriyoruz
        self.kodlanmis_veri = hata_olustur(self.kodlanmis_veri, hata_poz)
        
        # Bitleri gösterirken hatayı vurguluyoruz
        self.bitleri_goster(self.kodlanmis_veri, hata_poz)
        
        # Sonuçları güncelliyoruz
        self.sonuc_kutulari["Hatalı Veri:"].delete(0, tk.END)
        self.sonuc_kutulari["Hatalı Veri:"].insert(0, ''.join(map(str, self.kodlanmis_veri)))
        
        self.sonuc_kutulari["Hata Biti (varsa):"].delete(0, tk.END)
        self.sonuc_kutulari["Hata Biti (varsa):"].insert(0, str(hata_poz))
        
        self.status_bar.config(text=f"{hata_poz}. pozisyonda bit hatası oluşturuldu")
    
    def hata_tespit(self):
        # Oluşturduğumuz hatayı bulup düzeltmeye çalışıyoruz
        if not self.kodlanmis_veri:
            messagebox.showerror("Hata", "Önce Hamming kodunu hesaplamalısınız!")
            return
        
        # Hatayı tespit edip düzeltiyoruz
        duzeltilmis, mesaj, sendrom, hata_biti = hata_duzelt(self.kodlanmis_veri)
        
        # Kodlanmış veriyi düzeltilmiş haliyle güncelliyoruz
        self.kodlanmis_veri = duzeltilmis
        
        # Bitleri gösterirken hata pozisyonunu vurguluyoruz
        self.bitleri_goster(self.kodlanmis_veri, hata_biti)
        
        # Parity bitleri çıkarıp orijinal veriyi bulalım
        orijinal_veri = veri_cikar(duzeltilmis, self.veri_uzunluk.get())
        
        # Sonuçları kutucuklara yazıyoruz
        self.sonuc_kutulari["Sendrom:"].delete(0, tk.END)
        self.sonuc_kutulari["Sendrom:"].insert(0, str(sendrom))
        
        self.sonuc_kutulari["Düzeltilmiş Veri:"].delete(0, tk.END)
        self.sonuc_kutulari["Düzeltilmiş Veri:"].insert(0, ''.join(map(str, orijinal_veri)))
        
        self.status_bar.config(text=mesaj)
    
    def bitleri_goster(self, bits, highlight_pos=-1):
        # Canvas'ı temizliyoruz
        self.bit_canvas.delete("all")
        
        if not bits:
            return
        
        # Toplam bit sayısı
        bit_count = len(bits)
        
        # Canvas genişliğini alıyoruz
        canvas_width = self.bit_canvas.winfo_width()
        if canvas_width < 100:  # İlk çağrıda canvas boyutu belli olmayabiliyor
            canvas_width = 800
        
        # Bit kutularının boyutlarını hesaplıyoruz
        box_width = min(30, canvas_width // bit_count)
        box_height = 30
        
        # İlk kutu için başlangıç x koordinatı
        start_x = (canvas_width - (box_width * bit_count)) // 2
        
        # Her bit için bir kutu çiziyoruz
        for i, bit in enumerate(bits):
            x1 = start_x + (i * box_width)
            y1 = 10
            x2 = x1 + box_width
            y2 = y1 + box_height
            
            # Bit türüne göre kutu rengini belirliyoruz
            if i == highlight_pos:
                color = "#e74c3c"  # Hata biti - kırmızı
            elif i == len(bits) - 1:
                color = "#f1c40f"  # Genel parity biti - sarı
            elif (i+1) & i == 0:
                color = "#2ecc71"  # Parity biti - yeşil
            else:
                color = "#3498db"  # Veri biti - mavi
            
            # Kutuyu çiziyoruz
            self.bit_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#34495e")
            
            # Bitin değerini yazıyoruz (0 veya 1)
            self.bit_canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(bit), font=("Arial", 9, "bold"))
            
            # Bit numarasını kutuların altına yazıyoruz
            self.bit_canvas.create_text((x1+x2)//2, y2 + 10, text=str(i), font=("Arial", 7))

if __name__ == "__main__":
    app = HammingSimulatorApp()
    app.mainloop()