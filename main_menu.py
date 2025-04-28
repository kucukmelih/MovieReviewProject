import tkinter as tk
from tkinter import messagebox
from database import (
    get_all_movies, get_movie_by_id, has_user_reviewed_movie,
    add_review, get_average_rating, get_reviews_by_movie_id, get_username_by_id
)
import session
from login_window import open_login_window

# Ana menü penceresini açar
def open_main_menu(previous_window=None):
    if previous_window:
        previous_window.destroy()  # Önceki pencereyi kapat

    main_menu = tk.Toplevel()  # Yeni pencere oluştur
    main_menu.title("Main Menu")
    main_menu.geometry("800x600")

    # Hoşgeldin mesajı
    welcome_label = tk.Label(main_menu, text=f"Welcome, {session.current_username}!", font=("Helvetica", 16))
    welcome_label.pack(pady=30)

    # Filmleri görüntüleme butonu
    view_movies_button = tk.Button(main_menu, text="View Movies", width=20, height=2,
                                   command=lambda: open_movie_list(main_menu))
    view_movies_button.pack(pady=10)

    # Çıkış yapma butonu
    logout_button = tk.Button(main_menu, text="Logout", width=20, height=2,
                              command=lambda: logout(main_menu))
    logout_button.pack(pady=10)

# Film listesini gösteren pencereyi açar
def open_movie_list(previous_window=None):
    if previous_window:
        previous_window.destroy()  # Önceki pencereyi kapat

    movie_window = tk.Toplevel()
    movie_window.title("Movies List")
    movie_window.geometry("600x500")

    movies = get_all_movies()  # Veritabanından tüm filmleri al

    # Listeyi ve çerçeveyi oluştur
    list_frame = tk.Frame(movie_window)
    list_frame.pack(fill="both", expand=True, pady=10)

    movie_listbox = tk.Listbox(list_frame, width=50, height=15)
    movie_listbox.pack(pady=10)

    # Film listesine filmleri ekle
    for movie in movies:
        movie_listbox.insert(tk.END, f"{movie[0]} - {movie[1]}")  # Film ID ve Adı

    # Butonları yerleştir
    button_frame = tk.Frame(movie_window)
    button_frame.pack(pady=10)

    # Seçilen filmi detaylarıyla gösteren fonksiyon
    def show_movie_details():
        selected = movie_listbox.curselection()
        if selected:
            selected_index = selected[0]
            movie_id = movies[selected_index][0]
            open_movie_details(movie_window, movie_id)

    # "View Details" butonu
    details_button = tk.Button(button_frame, text="View Details", command=show_movie_details)
    details_button.pack()

    # Geri dön butonu
    back_button = tk.Button(button_frame, text="Back", command=lambda: open_main_menu(movie_window))
    back_button.pack(pady=10)

# Film detaylarını gösteren pencereyi açar
def open_movie_details(previous_window=None, movie_id=None):
    if previous_window:
        previous_window.destroy()  # Önceki pencereyi kapat

    movie = get_movie_by_id(movie_id)  # ID'ye göre filmi getir

    if not movie:
        messagebox.showerror("Error", "Movie not found!")  # Film bulunamazsa hata ver
        return

    details_window = tk.Toplevel()
    details_window.title("Movie Details")
    details_window.geometry("500x800")

    # Ortalama puan bilgisini al ve göster
    average_rating = get_average_rating(movie_id)
    if average_rating is not None:
        avg_text = f"Average Rating: {average_rating:.2f} / 10"
    else:
        avg_text = "Average Rating: No ratings yet."

    avg_label = tk.Label(details_window, text=avg_text, font=("Helvetica", 14, "bold"))
    avg_label.pack(pady=10)

    # Film bilgilerini sıralı şekilde göster
    fields = ["Title", "Year", "Certificate", "Runtime", "Genre",
              "IMDB Rating", "Overview", "Meta Score", "Director",
              "Star 1", "Star 2", "Star 3", "Star 4", "Votes", "Gross"]

    for idx, field in enumerate(fields):
        value = movie[idx + 1] if idx + 1 < len(movie) else ""
        text = f"{field}: {value}"
        label = tk.Label(details_window, text=text, anchor="w", justify="left", wraplength=450, font=("Helvetica", 12))
        label.pack(padx=10, pady=5)

    # İnceleme ekleme işlemini yöneten iç fonksiyon
    def handle_add_review():
        if has_user_reviewed_movie(session.current_user_id, movie_id):
            messagebox.showerror("Error", "You have already reviewed this movie.")
        else:
            open_add_review_window(details_window, movie_id)

    # İnceleme ekleme butonu
    add_review_button = tk.Button(details_window, text="Add Review", width=20, height=2,
                                  command=handle_add_review)
    add_review_button.pack(pady=10)

    # İncelemeleri görüntüleme butonu
    see_reviews_button = tk.Button(details_window, text="See Reviews", width=20, height=2,
                                   command=lambda: open_reviews_window(details_window, movie_id))
    see_reviews_button.pack(pady=10)

    # Geri dön butonu
    back_button = tk.Button(details_window, text="Back", command=lambda: open_movie_list(details_window))
    back_button.pack(pady=10)

# İnceleme ekleme penceresini açar
def open_add_review_window(previous_window=None, movie_id=None):
    if previous_window:
        previous_window.destroy()

    review_window = tk.Toplevel()
    review_window.title("Add Review")
    review_window.geometry("400x300")

    # Puan giriş alanı
    tk.Label(review_window, text="Rating (1-10):", font=("Helvetica", 12)).pack(pady=10)
    rating_spinbox = tk.Spinbox(review_window, from_=1, to=10, width=5)
    rating_spinbox.pack()

    # Yorum giriş alanı
    tk.Label(review_window, text="Comment:", font=("Helvetica", 12)).pack(pady=10)
    comment_text = tk.Text(review_window, width=40, height=5)
    comment_text.pack()

    # İncelemeyi kaydeden iç fonksiyon
    def submit_review():
        try:
            rating = int(rating_spinbox.get())  # Puanı integer'a çevir
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for rating.")
            return

        comment = comment_text.get("1.0", tk.END).strip()

        if rating < 1 or rating > 10:
            messagebox.showerror("Error", "Rating must be between 1 and 10.")
            return

        try:
            add_review(session.current_user_id, movie_id, rating, comment)
            messagebox.showinfo("Success", "Review submitted successfully!")
            open_movie_details(review_window, movie_id)  # Başarılı eklemeden sonra detaylara geri dön
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit review.\n{e}")

    # Submit butonu
    submit_button = tk.Button(review_window, text="Submit Review", command=submit_review)
    submit_button.pack(pady=20)

    # Geri dön butonu
    back_button = tk.Button(review_window, text="Back", command=lambda: open_movie_details(review_window, movie_id))
    back_button.pack(pady=10)

# Filmin yorumlarını gösteren pencereyi açar
def open_reviews_window(previous_window=None, movie_id=None):
    if previous_window:
        previous_window.destroy()

    reviews_window = tk.Toplevel()
    reviews_window.title("Reviews")
    reviews_window.geometry("500x400")

    reviews = get_reviews_by_movie_id(movie_id)  # Veritabanından yorumları al

    # Yorumları gösterecek text alanı ve scrollbar
    text_frame = tk.Frame(reviews_window)
    text_frame.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    review_textbox = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set)
    review_textbox.pack(fill="both", expand=True)

    scrollbar.config(command=review_textbox.yview)

    # Yorumlar ekrana yazdırılır
    if not reviews:
        review_textbox.insert(tk.END, "No reviews yet.\n")
    else:
        for review in reviews:
            user_id, rating, comment, date = review
            username = get_username_by_id(user_id)
            review_textbox.insert(tk.END, f"Username: {username}\nRating: {rating}/10\nComment: {comment}\n\n")

    review_textbox.config(state="disabled")  # Kullanıcı yorumları değiştiremesin

    # Geri dön butonu
    back_button = tk.Button(reviews_window, text="Back", command=lambda: open_movie_details(reviews_window, movie_id))
    back_button.pack(pady=10)

# Kullanıcıyı çıkış yaptırır ve login ekranına yönlendirir
def logout(previous_window=None):
    if previous_window:
        previous_window.destroy()
    open_login_window()
