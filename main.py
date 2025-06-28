# Kullanılan kütüphaneler
import sqlite3
from datetime import datetime

# Ürün ekleme fonksiyonu
def urun_ekle():   
    conn = sqlite3.connect('database.db') # Veri tabanına bağlan
    cursor = conn.cursor()                # Cursor (imleç) oluştur.

    # Kullanıcının gireceği yanlış girdiyi kontrol et
    ad = input("Ürün adı: ")
    try:   
        stok = int(input("Stok adedi: "))
        fiyat = float(input("Fiyat: "))
    except ValueError:
        print("Hatalı giriş. Lütfen sayısal değer giriniz.")
        return
       
    # Veri tabanına girdileri ekle
    print("----------Ürün Eklendi----------")
    cursor.execute("INSERT INTO Products (Ürün, Stok, Fiyat) VALUES (?, ?, ?)", (ad, stok, fiyat))  
    
    conn.commit()    # Verileri kalıcı hale getir
    conn.close()     # Veri tabanı ile bağlantıyı kes

# Ürünleri listeleme fonksiyonu
def urunleri_listele():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Okuma
    print("----------Ürün Listesi----------")
    cursor.execute("SELECT * FROM Products")
    records = cursor.fetchall()
    for row in records:
        print(f"ID: {row[0]}, Ürün: {row[1]}, Stok: {row[2]} Adet, Fiyat: {row[3]}TL")

    conn.close()

# Stok giriş fonksiyonu     
def urun_girisi():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    now = datetime.now() 

    try:
        urun_kodu = int(input("Ürün kodunu (ID) giriniz: "))
        miktar = int(input("Miktar: "))
    except ValueError:
        print("Hatalı giriş. Lütfen sayısal değer giriniz.")
        return
    
   # Ürün var mı? Kontrolunü yap
    cursor.execute("SELECT Stok FROM Products WHERE id = ?", (urun_kodu,))
    result = cursor.fetchone()
    if result is None:
        print("Ürün bulunamadı.")
        return

    entry_or_exit = "Giriş"
    data = now.strftime("%d-%m-%Y %H:%M:%S")
  
    print("----------Stok Girildi----------")
    cursor.execute("INSERT INTO Stock (ürün_kodu, miktar, entry_or_exit, date) VALUES (?, ?, ?, ?)", (urun_kodu, miktar, entry_or_exit, data))

    # Stoğu güncelle
    cursor.execute("UPDATE Products SET Stok = Stok + ? WHERE id = ?", (miktar, urun_kodu))
  
    conn.commit()    
    conn.close()

# Stok çıkış fonksiyonu  
def urun_cikisi():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    now = datetime.now() 

    try:
        urun_kodu = int(input("Ürün kodunu (ID) giriniz: "))
        miktar = int(input("Miktar: "))
    except ValueError:
        print("Hatalı giriş. Lütfen sayısal değer giriniz.")
        return
    
    # Ürün var mı? Kontrolunü yap
    cursor.execute("SELECT Stok FROM Products WHERE id = ?", (urun_kodu,))
    result = cursor.fetchone()
    if result is None:
        print("Ürün bulunamadı.")
        return
    # Ürün eksi değer olamayacağı için çıkış yapılacak ürünle ürün müktarını karılaştır.
    mevcut_stok = result[0]
    if miktar > mevcut_stok:
        print(f"Yetersiz stok! Mevcut stok: {mevcut_stok}")
        return  
    
    entry_or_exit = "Çıkış"
    data = now.strftime("%d-%m-%Y %H:%M:%S")
    
    print("----------Stok Girildi----------")
    cursor.execute("INSERT INTO Stock (ürün_kodu, miktar, entry_or_exit, date) VALUES (?, ?, ?, ?)", (urun_kodu, miktar, entry_or_exit, data))

    # Stoğu güncelle
    cursor.execute("UPDATE Products Set Stok = Stok - ? WHERE id = ?", (miktar, urun_kodu))
    
    conn.commit()    
    conn.close()

# Kullanıcı menüsü
def menu():
    while True:
        print("-----Stok takip Uygulamasına Hoş Geldiniz!-----\n" 
        "\nLütfen Yapmak istediğiniz işlemi seçiniz")
        
        print("1. Ürün Ekle" 
            "\n2. Ürünleri Listele"
            "\n3. Ürün Girişi"
            "\n4. Ürün Çıkışı"
            "\n5. Çıkış")

        secim = input("Seçiminiz: ")

        try:
            rakam = int(secim)  
            if rakam == 1:
                urun_ekle()
            elif rakam == 2:
                urunleri_listele()
            elif rakam == 3:
                urun_girisi()
            elif rakam == 4:
                urun_cikisi()
            elif rakam == 5:
                print("Programdan çıkış yapıldı!")
                break
            else:
                print("Lütfen 1 ile 5 arasında bir rakam giriniz!")
                
        except ValueError:
            print("Lütfen sayısal bir değer giriniz!")
            

# Çalıştır
if __name__ == "__main__":
    menu()