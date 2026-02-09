import sqlite3
import os
import random
from faker import Faker
from datetime import datetime, timedelta

# 1. Klasör ve Path Ayarları
current_dir = os.path.dirname(os.path.abspath(__file__)) # src klasörü
base_dir = os.path.dirname(current_dir) # SkyStream ana klasörü
sql_path = os.path.join(base_dir, "sql", "database.sql")
db_path = os.path.join(current_dir, "database.db")

fake = Faker()

def main():
    # 2. Bağlantı ve Başlatma
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    
    # SQLite'da Foreign Key ve Trigger desteğini her bağlantıda açman lazım
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 3. Şemayı Yükle (Tabloları Sıfırdan Oluştur)
    print("--- Tablolar oluşturuluyor ---")
    try:
        with open(sql_path, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
    except FileNotFoundError:
        print(f"Hata: {sql_path} bulunamadı!")
        return

    # 4. Planları Ekle
    print("--- Planlar ekleniyor ---")
    plans = [
        ('free', 0.0, 0),
        ('standart', 15.99, 3),
        ('premium', 29.99, 12)
    ]
    cursor.executemany('INSERT INTO account_plans (plan_name, price, duration_month) VALUES (?, ?, ?)', plans)

    # 5. Faker ile Toplu Veri Üretimi
    print("--- Kullanıcılar ve abonelikler basılıyor ---")
    user_count = 50
    
    for _ in range(user_count):
        # Kullanıcıyı ekle
        u_name = fake.user_name()
        u_email = fake.email()
        cursor.execute('INSERT INTO users (user_name, email) VALUES (?, ?)', (u_name, u_email))
        user_id = cursor.lastrowid

        # Rastgele bir plan seç (1: free, 2: standart, 3: premium)
        plan_id = random.randint(1, 3)
        
        # Rastgele tarihler (Son 1 yıl içinde başlamış olsun)
        start_date = fake.date_between(start_date='-1y', end_date='today')
        
        # Plan süresine göre bitiş tarihini hesapla (Free ise 1 ay öylesine verdik)
        duration = 1 if plan_id == 1 else (3 if plan_id == 2 else 12)
        end_date = start_date + timedelta(days=duration * 30)
        
        status = 'active' if end_date > datetime.now().date() else 'passive'

        # Aboneliği ekle
        cursor.execute('''INSERT INTO subscriptions (user_id, plans_id, start_date, end_date, status) 
                          VALUES (?, ?, ?, ?, ?)''', 
                       (user_id, plan_id, start_date.isoformat(), end_date.isoformat(), status))
        subs_id = cursor.lastrowid

        # Ödemeyi ekle (%80 paid, %20 unpaid bas ki trigger test edilsin)
        p_status = random.choices(['paid', 'unpaid'], weights=[80, 20])[0]
        # Plan fiyatını basitçe manuel eşleştirdik (Geliştirilebilir)
        price_map = {1: 0.0, 2: 15.99, 3: 29.99}
        
        cursor.execute('''INSERT INTO payments (subs_id, amount, payment_status) 
                          VALUES (?, ?, ?)''', (subs_id, price_map[plan_id], p_status))

    # 6. Değişiklikleri Kaydet ve Kapat
    db.commit()
    db.close()
    print(f"\nİşlem tamam {user_count} kullanıcı ve bağlı verileri basıldı.")
  

if __name__ == "__main__":
    main()

  
  
 
 
