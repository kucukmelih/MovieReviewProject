import sqlite3
import csv
import random
from faker import Faker
from datetime import datetime
from model import train_model
import string  

fake = Faker()

NUM_USERS = 50
NUM_MOVIES = 100
REVIEWS_PER_MOVIE = 20

# Database connection
def get_connection():
    return sqlite3.connect("movies.db")

# Create database tables
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

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

# Add a new user
def add_user(username, email, password, age, gender, location):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Users (username, email, password, age, gender, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, email, password, age, gender, location))
    conn.commit()
    conn.close()

# Validate user login
def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Users WHERE username=? AND password=?
    """, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Retrieve all movies
def get_all_movies():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title FROM Movies
    """)
    movies = cursor.fetchall()
    conn.close()
    return movies

# Retrieve a specific movie by ID
def get_movie_by_id(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Movies WHERE id=?
    """, (movie_id,))
    movie = cursor.fetchone()
    conn.close()
    return movie

# Add a user review
def add_review(user_id, movie_id, rating, comment, date_now=None):
    conn = get_connection()
    cursor = conn.cursor()
    if not date_now:
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        cursor.execute("""
            INSERT INTO Reviews (user_id, movie_id, rating, comment, date)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, movie_id, rating, comment, date_now))
        conn.commit()
        train_model()  # ✅ Update model after adding review
    except sqlite3.IntegrityError:
        pass
    conn.close()

# Retrieve all reviews for a specific movie
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

# Check if a user has already reviewed a movie
def has_user_reviewed_movie(user_id, movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM Reviews WHERE user_id=? AND movie_id=?
    """, (user_id, movie_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Calculate average rating of a movie
def get_average_rating(movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AVG(rating) FROM Reviews WHERE movie_id=?
    """, (movie_id,))
    avg = cursor.fetchone()[0]
    conn.close()
    return avg

# Load movie data from CSV file
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
                row['star1'], row['star2'], row['star3'], row['star4'],
                int(row['votes']) if row['votes'] else None,
                row['gross']
            ))
    conn.commit()
    conn.close()

# Get username by user ID
def get_username_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username FROM Users WHERE id=?
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Unknown"

# Search movies by title
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

# Add a new movie
def add_movie(title, year, certificate, runtime, genre, imdb_rating, overview, meta_score, director, star1, star2, star3, star4, votes, gross):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Movies (title, year, certificate, runtime, genre, imdb_rating, overview, meta_score, director, star1, star2, star3, star4, votes, gross)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, year, certificate, runtime, genre, imdb_rating, overview, meta_score, director, star1, star2, star3, star4, votes, gross))
    conn.commit()
    conn.close()

# Update an existing review
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
    train_model()  # Update model after updating review

# Delete a review
def delete_review(user_id, movie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM Reviews
        WHERE user_id=? AND movie_id=?
    """, (user_id, movie_id))
    conn.commit()
    conn.close()

# Filter movies by genre
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

# List movies sorted by average rating
def get_movies_ordered_by_rating():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Movies.id, Movies.title, AVG(Reviews.rating) as avg_rating
        FROM Movies
        LEFT JOIN Reviews ON Movies.id = Reviews.movie_id
        GROUP BY Movies.id
        ORDER BY avg_rating DESC
    """)
    movies = cursor.fetchall()
    conn.close()
    return movies

# Get all user IDs
def get_user_ids():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

# Generate a strong valid password
def generate_valid_password(length=8):
    letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%^&*()"

    # At least 1 letter, 1 digit, and 1 symbol
    password = [
        random.choice(letters),
        random.choice(digits),
        random.choice(symbols),
    ]

    all_chars = letters + digits + symbols
    password += random.choices(all_chars, k=length - 3)

    random.shuffle(password)
    return ''.join(password)

# Generate dummy users and reviews
def generate_dummy_data():
    create_tables()
    for _ in range(NUM_USERS):
        add_user(
            username=fake.user_name(),
            email=fake.email(),
            password=generate_valid_password(),
            age=random.randint(18, 65),
            gender=random.choice(["Male", "Female"]),
            location=fake.city()
        )

    user_ids = get_user_ids()
    for movie_id in range(1, NUM_MOVIES + 1):
        selected_users = random.sample(user_ids, REVIEWS_PER_MOVIE)
        for user_id in selected_users:
            rating = random.randint(1, 10)
            comment = fake.sentence(nb_words=random.randint(8, 15))
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
            add_review(user_id, movie_id, rating, comment, date_now)

# Entry point
if __name__ == "__main__":
    generate_dummy_data()
    print("\nAll data has been successfully generated and saved to the database.")
