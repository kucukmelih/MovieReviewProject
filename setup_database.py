# Daha önce oluşturduğumuz gerekli fonksiyonları kullanmak için import ediyoruz.
from database import create_tables, load_movies_from_csv 

# Veritabanını ve tabloları oluşturacak ana fonksiyon
def main():
    print("🔵 Setting up the database and creating tables...")
    create_tables()  # database içinde gerekli tabloları oluşturur
    print("✅ Tables created successfully.")

    # Örnek film verilerini veritabanına aktarma işlemi
    try:
        print("🔵 Loading movie data from movies.csv...")
        load_movies_from_csv('movies.csv')  # movies.csv dosyasındaki filmleri veritabanına yükler
        print("✅ Movie data loaded successfully.")
    except FileNotFoundError:
        # movies.csv dosyası bulunamazsa kullanıcıya uyarı mesajı gösterir
        print("⚠️ Warning: movies.csv not found. No movie data loaded.")

# Eğer dosya doğrudan çalıştırılırsa main() fonksiyonunu çağırıyoruz
if __name__ == "__main__":
    main()