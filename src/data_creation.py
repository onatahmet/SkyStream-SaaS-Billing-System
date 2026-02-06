from faker import Faker
import csv

def generate_user_data(number):
    """
    Faker kütüphanesini kullanarak belirtilen sayıda 
    eşsiz kullanıcı adı ve e-posta adresi üretir.
    """
    fake = Faker()
    user_data = []

    for i in range(number):
        # Veritabanında UNIQUE kısıtlaması olduğu için .unique özelliğini kullanıyoruz.
        # Böylece aynı isim veya mailin iki kez üretilmesini engelliyoruz.
        user = {
            'User_name': fake.unique.user_name(),
            'Email': fake.unique.email()
        }
        user_data.append(user)

    return user_data

def save_to_csv(data, filename):
    """
    Üretilen sözlük listesini (list of dicts) alır ve 
    bir CSV dosyası olarak diske kaydeder.
    """
    # Eğer liste boşsa fonksiyonu sonlandırıyoruz.
    if not data:
        print("[-] Veri listesi boş, işlem yapılmadı.")
        return
    
    # Listenin ilk elemanındaki anahtarları (User_name, Email) alıp 
    # CSV'nin sütun başlıkları (fieldnames) olarak belirliyoruz.
    keys = data[0].keys()

    # Dosyayı yazma ('w') modunda açıyoruz. 
    # encoding='utf-8' Türkçe veya özel karakterlerin bozulmasını önler.
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        # DictWriter, sözlük yapısındaki verileri CSV'ye uygun hale getirir.
        writer = csv.DictWriter(output_file, fieldnames=keys)
        
        # Sütun isimlerini (User_name, Email) en başa yazar.
        writer.writeheader()
        
        # ÖNEMLİ: 'data' bir liste olduğu için 'writerows' (çoğul) kullanıyoruz.
        # Bu komut tüm listeyi tek seferde satır satır dosyaya işler.
        writer.writerows(data)
        
    print(f'[+] Veriler {filename} dosyasına başarıyla kaydedildi.')

# --- Çalıştırma Bölümü ---
if __name__ == "__main__":
    # 50 adet sahte veri oluşturuyoruz.
    num_users = 50
    generated_data = generate_user_data(num_users)
    
    # Oluşturulan veriyi CSV dosyasına kaydediyoruz.
    save_to_csv(generated_data, 'users_data.csv')

  
  
 
 
