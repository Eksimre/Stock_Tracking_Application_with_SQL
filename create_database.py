import sqlite3 # SQLite veritabanı modülü
import os      # Dosya işlemleri için modül

# Veri tabanı oluşturma foksiyonu
def create_database():
    # Aynı klasörde daha önce oluşturulmuş bir veritabanı varsa onu sil
    # Deneme projesi olduğu için her çalıştırmada temiz bir veritabanı ile başlanır
    # Proje başladığında bu satırlar iptal edilir
    if os.path.exists("database.db"):
        os.remove("database.db")

    # veri tabanını oluştur ve bağlantı kur
    conn = sqlite3.connect("database.db") # Veritabanı dosyasını oluşturur
    cursor = conn.cursor() # SQL kodlarını çalıştırmak için bir imleç oluştur (cursor)
    return conn, cursor # Veri bağlantısı ve imleci fonksiyon dışında döndür

# Ürünler ve stok hareketleri tablolarını oluşturan fonksiyon
def create_table(cursor):
    # Ürünler tablosu
    cursor.execute("""
                   CREATE TABLE Products(
                       id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       Ürün  VARCHAR(255) NOT NULL,
                       Stok  INTEGER DEFAULT 0,
                       Fiyat INTEGER DEFAULT 0       
                   )
                   """)
    # Stok harektlerinin tablosu
    cursor.execute("""
                   CREATE TABLE Stock(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       ürün_kodu INTEGER NOT NULL, 
                       miktar INTEGER,
                       entry_or_exit TEXT,
                       date TEXT
                   FOREIGN KEY(ürün_kodu) REFERENCES Products(id)    
                     
                   )
                   """)

# Veritabanı oluşturma ve tablo kurma işlemini başlatan ana fonksiyon   
def run():
    # Veri tabanını oluştur
    conn, cursor = create_database()
    try:
        create_table(cursor) # Tabloları oluşturur.
        conn.commit() # Değişiklikleri kaydet
    except sqlite3.OperationalError as e:
        print("Hata:", e) # Hata mesajını ekrana yaz
    finally:
        conn.close() # Bağlantıyı kapat

# Programı çalıştır
run()
    
    
