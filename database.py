import sqlite3
import csv
from datetime import datetime

# Veritabanı bağlantısı
def get_connection():
    return sqlite3.connect("movies.db")

# Veritabanı ve tabloları oluşturma
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Movies tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER,
            certificate TEXT,
            runtime INTEGER,
            genre TEXT,
            imdb_rating REAL,
            overview TEXT,
            meta_score INTEGER,
            director TEXT,
            star1 TEXT,
            star2 TEXT,
            star3 TEXT,
            star4 TEXT,
            votes INTEGER,
            gross TEXT
        )
    """)

    # Users tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            location TEXT
        )
    """)

    # Reviews tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            movie_id INTEGER,
            rating INTEGER,
            comment TEXT,
            date TEXT,
            UNIQUE(user_id, movie_id),
            FOREIGN KEY(user_id) REFERENCES Users(id),
            FOREIGN KEY(movie_id) REFERENCES Movies(id)
        )
    """)

    conn.commit()
    conn.close()

# Kullanıcı ekleme
def add_user(username, email, password, age, gender, location):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Users (username, email, password, age, gender, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, email, password, age, gender, location))
    conn.commit()
    conn.close()

# Kullanıcı girişi kontrolü
def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Users WHERE username=? AND password=?
    """, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Tüm filmleri listeleme
def get_all_movies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title FROM Movies
    """)
    movies = cursor.fetchall()
    conn.close()
    return movies

# Belirli bir filmin detaylarını çekme
def get_movie_by_id(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Movies WHERE id=?
    """, (movie_id,))
    movie = cursor.fetchone()
    conn.close()
    return movie

# Yorum ekleme
def add_review(user_id, movie_id, rating, comment):
    conn = get_connection()
    cursor = conn.cursor()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        cursor.execute("""
            INSERT INTO Reviews (user_id, movie_id, rating, comment, date)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, movie_id, rating, comment, date_now))
        conn.commit()
    except sqlite3.IntegrityError:
        print("This user has already reviewed this movie.")
    conn.close()

# Belirli bir filmin yorumlarını çekme
def get_reviews_by_movie_id(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, rating, comment, date 
        FROM Reviews 
        WHERE movie_id=?
        ORDER BY date DESC
    """, (movie_id,))
    reviews = cursor.fetchall()
    conn.close()
    return reviews

# Kullanıcının bir filme daha önce yorum yapıp yapmadığını kontrol etme
def has_user_reviewed_movie(user_id, movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM Reviews WHERE user_id=? AND movie_id=?
    """, (user_id, movie_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Filmin ortalama puanını hesaplama
def get_average_rating(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AVG(rating) FROM Reviews WHERE movie_id=?
    """, (movie_id,))
    avg = cursor.fetchone()[0]
    conn.close()
    return avg

# CSV dosyasından filmleri yükleme
def load_movies_from_csv(file_path):
    conn = get_connection()
    cursor = conn.cursor()

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO Movies (title, year, certificate, runtime, genre, imdb_rating, overview, meta_score,
                                    director, star1, star2, star3, star4, votes, gross)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['title'],
                int(row['year']) if row['year'] else None,
                row['certificate'],
                int(row['runtime']) if row['runtime'] else None,
                row['genre'],
                float(row['imdb_rating']) if row['imdb_rating'] else None,
                row['overview'],
                int(row['meta_score']) if row['meta_score'] else None,
                row['director'],
                row['star1'],
                row['star2'],
                row['star3'],
                row['star4'],
                int(row['votes']) if row['votes'] else None,
                row['gross']
            ))

    conn.commit()
    conn.close()

# Kullanıcı ID'den username çekme
def get_username_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username FROM Users WHERE id=?
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return "Unknown"
    
## Ekstra Ozellikler ##

# Film adına göre arama
def search_movies_by_title(search_term):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title FROM Movies
        WHERE title LIKE ?
    """, ('%' + search_term + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

# Yeni film ekleyebilme
def add_movie(title, year, certificate, runtime, genre, imdb_rating, overview, meta_score, director, star1, star2, star3, star4, votes, gross):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Movies (title, year, certificate, runtime, genre, imdb_rating, overview, meta_score, director, star1, star2, star3, star4, votes, gross)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, year, certificate, runtime, genre, imdb_rating, overview, meta_score, director, star1, star2, star3, star4, votes, gross))
    conn.commit()
    conn.close()

# Yorum düzenleme
def update_review(user_id, movie_id, new_rating, new_comment):
    conn = get_connection()
    cursor = conn.cursor()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        UPDATE Reviews
        SET rating=?, comment=?, date=?
        WHERE user_id=? AND movie_id=?
    """, (new_rating, new_comment, date_now, user_id, movie_id))
    conn.commit()
    conn.close()

# Yorum silme
def delete_review(user_id, movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM Reviews
        WHERE user_id=? AND movie_id=?
    """, (user_id, movie_id))
    conn.commit()
    conn.close()

# Genre (tür) filtresi ile filmleri listeleme
def get_movies_by_genre(genre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title FROM Movies
        WHERE genre LIKE ?
    """, ('%' + genre + '%',))
    movies = cursor.fetchall()
    conn.close()
    return movies

# Ortalama puana göre filmleri sıralama
def get_movies_ordered_by_rating():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Movies.id, Movies.title, AVG(Reviews.rating) as avg_rating
        FROM Movies
        LEFT JOIN Reviews ON Movies.id = Reviews.movie_id
        GROUP BY Movies.id
        ORDER BY avg_rating DESC NULLS LAST
    """)
    movies = cursor.fetchall()
    conn.close()
    return movies