import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import (
    get_all_movies, get_movie_by_id, has_user_reviewed_movie,
    add_review, get_average_rating, get_reviews_by_movie_id, get_username_by_id,
    search_movies_by_title, get_movies_by_genre, get_movies_ordered_by_rating, # Ekstralar
    add_movie, update_review, delete_review, # Ekstralar
)
import session
from login_window import open_login_window

# Pencere Konumu
def set_window_position(window, width=500, height=700, x=500, y=100):
    window.geometry(f"{width}x{height}+{x}+{y}")

# Ana menü penceresini açar
def open_main_menu(previous_window=None):
    if previous_window:
        previous_window.destroy()

    main_menu = tk.Toplevel()
    main_menu.title("Main Menu")
    set_window_position(main_menu)

    frame = tk.Frame(main_menu)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(frame, text=f"Welcome, {session.current_username}!", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=(0, 30))

    view_movies_button = tk.Button(
        frame,
        text="View Movies",
        width=20,
        height=2,
        font=("Helvetica", 12),
        bg="#CFE2FF",
        fg="black",
        activebackground="#A7C8F2",
        command=lambda: open_movie_list(main_menu)
    )
    view_movies_button.pack(pady=10)

    add_movie_button = tk.Button(
        frame,
        text="Add Movie",
        width=20,
        height=2,
        font=("Helvetica", 12),
        bg="#D1E7DD",
        fg="black",
        activebackground="#A9D6C2",
        command=lambda: open_add_movie_window(main_menu)
    )
    add_movie_button.pack(pady=10)

    logout_button = tk.Button(
        frame,
        text="Logout",
        width=20,
        height=2,
        font=("Helvetica", 12),
        bg="#F8D7DA",
        fg="black",
        activebackground="#F1B0B7",
        command=lambda: logout(main_menu)
    )
    logout_button.pack(pady=10)

# Film listesini gösteren pencereyi açar
def open_movie_list(previous_window=None):
    if previous_window:
        previous_window.destroy()

    movie_window = tk.Toplevel()
    movie_window.title("Movies List")
    set_window_position(movie_window)

    frame = tk.Frame(movie_window)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(frame, text="Movies", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=(0, 20))

    # Search alanı
    search_frame = tk.Frame(frame)
    search_frame.pack(pady=(0, 10))

    search_entry = tk.Entry(search_frame, width=30, font=("Helvetica", 12))
    search_entry.grid(row=0, column=0, padx=5)

    search_button = tk.Button(
        search_frame,
        text="Search",
        font=("Helvetica", 10),
        bg="#D1E7DD",
        fg="black",
        activebackground="#A9D6C2",
        command=lambda: perform_search()
    )
    search_button.grid(row=0, column=1, padx=5)

    # Genre + Sort alanı
    filter_sort_frame = tk.Frame(frame)
    filter_sort_frame.pack(pady=(0, 10))

    genre_values = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime",
                    "Drama", "Family", "Fantasy", "History", "Horror", "Music",
                    "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]

    genre_combo = ttk.Combobox(filter_sort_frame, 
                               values=genre_values, 
                               width=20, 
                               font=("Helvetica", 11), 
                               state="readonly")
    genre_combo.set("Select Genre")
    genre_combo.grid(row=0, column=0, padx=5)

    genre_button = tk.Button(
        filter_sort_frame,
        text="Filter",
        font=("Helvetica", 10),
        bg="#D1E7DD",
        fg="black",
        activebackground="#A9D6C2",
        command=lambda: perform_genre_filter()
    )
    genre_button.grid(row=0, column=1, padx=5)

    sort_button = tk.Button(
        filter_sort_frame,
        text="Sort by Avg Rating",
        font=("Helvetica", 10),
        bg="#CFE2FF",
        fg="black",
        activebackground="#A7C8F2",
        command=lambda: sort_by_rating()
    )
    sort_button.grid(row=0, column=2, padx=5)

    reset_button = tk.Button(
        frame,
        text="Reset Filters",
        font=("Helvetica", 10),
        bg="#FFDDDD",
        fg="black",
        activebackground="#FFCCCC",
        command=lambda: perform_reset_filters()
    )
    reset_button.pack(pady=(0, 10))

    # Film Listesi
    listbox_frame = tk.Frame(frame)
    listbox_frame.pack()

    movie_listbox = tk.Listbox(listbox_frame, width=60, height=15, font=("Helvetica", 11))
    movie_listbox.pack(pady=10)

    # İlk veriler
    all_movies = get_all_movies()  # Orijinal liste
    displayed_movies = all_movies.copy()  # Şu an listede gösterilenler

    def refresh_list(movies_to_show):
        nonlocal displayed_movies
        displayed_movies = movies_to_show  # Güncelle
        movie_listbox.delete(0, tk.END)
        for movie in movies_to_show:
            movie_listbox.insert(tk.END, f"{movie[0]} - {movie[1]}")

    refresh_list(all_movies)

    # İşlevler
    def perform_search():
        search_term = search_entry.get().strip()
        if search_term:
            filtered_movies = search_movies_by_title(search_term)
        else:
            filtered_movies = get_all_movies()
        refresh_list(filtered_movies)

    def perform_genre_filter():
        selected_genre = genre_combo.get()
        if selected_genre == "Select Genre" or selected_genre == "":
            filtered_movies = get_all_movies()
        else:
            filtered_movies = get_movies_by_genre(selected_genre)
        refresh_list(filtered_movies)

    def sort_by_rating():
        sorted_movies = get_movies_ordered_by_rating()
        refresh_list([(movie[0], f"{movie[1]} (Avg: {movie[2]:.2f})" if movie[2] is not None else f"{movie[1]} (Avg: N/A)") for movie in sorted_movies])

    def perform_reset_filters():
        search_entry.delete(0, tk.END)
        genre_combo.set("Select Genre")
        refresh_list(get_all_movies())

    def show_movie_details():
        selected = movie_listbox.curselection()
        if selected:
            selected_index = selected[0]
            selected_movie = displayed_movies[selected_index]
            movie_id = selected_movie[0]
            open_movie_details(movie_window, movie_id)

    # View Details ve Back Butonları
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=20)

    details_button = tk.Button(
        button_frame,
        text="View Details",
        width=15,
        font=("Helvetica", 12),
        bg="#D1E7DD",
        fg="black",
        activebackground="#A9D6C2",
        command=show_movie_details
    )
    details_button.grid(row=0, column=0, padx=10)

    back_button = tk.Button(
        button_frame,
        text="Back",
        width=15,
        font=("Helvetica", 12),
        bg="#F8D7DA",
        fg="black",
        activebackground="#F1B0B7",
        command=lambda: open_main_menu(movie_window)
    )
    back_button.grid(row=0, column=1, padx=10)

# Film detaylarını gösteren pencereyi açar
def open_movie_details(previous_window=None, movie_id=None):
    if previous_window:
        previous_window.destroy()

    movie = get_movie_by_id(movie_id)
    if not movie:
        messagebox.showerror("Error", "Movie not found!")
        return

    details_window = tk.Toplevel()
    details_window.title("Movie Details")
    set_window_position(details_window)

    frame = tk.Frame(details_window)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    average_rating = get_average_rating(movie_id)
    avg_text = f"Average Rating: {average_rating:.2f} / 10" if average_rating is not None else "Average Rating: No ratings yet."

    avg_label = tk.Label(frame, text=avg_text, font=("Helvetica", 14, "bold"))
    avg_label.pack(pady=10)

    fields = ["Title", "Year", "Certificate", "Runtime", "Genre",
              "IMDB Rating", "Overview", "Meta Score", "Director",
              "Star 1", "Star 2", "Star 3", "Star 4", "Votes", "Gross"]

    for idx, field in enumerate(fields):
        value = movie[idx + 1] if idx + 1 < len(movie) else ""
        text = f"{field}: {value}"
        label = tk.Label(frame, text=text, anchor="w", justify="left", wraplength=450, font=("Helvetica", 12))
        label.pack(padx=10, pady=5)

    def handle_add_review():
        if has_user_reviewed_movie(session.current_user_id, movie_id):
            messagebox.showerror("Error", "You have already reviewed this movie.")
        else:
            open_add_review_window(details_window, movie_id)

    def handle_edit_review():
        if not has_user_reviewed_movie(session.current_user_id, movie_id):
            messagebox.showerror("Error", "You have not reviewed this movie yet.")
            return

        # Yeni pencere aç edit için
        edit_window = tk.Toplevel()
        edit_window.title("Edit Your Review")
        set_window_position(edit_window, width=400, height=400)

        edit_frame = tk.Frame(edit_window)
        edit_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(edit_frame, text="New Rating (1-10):", font=("Helvetica", 12)).pack(pady=10)
        new_rating_spinbox = tk.Spinbox(edit_frame, from_=1, to=10, width=5, font=("Helvetica", 12))
        new_rating_spinbox.pack()

        tk.Label(edit_frame, text="New Comment:", font=("Helvetica", 12)).pack(pady=10)
        new_comment_text = tk.Text(edit_frame, width=40, height=5, font=("Helvetica", 12))
        new_comment_text.pack()

        def submit_edit():
            try:
                new_rating = int(new_rating_spinbox.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for rating.")
                return

            new_comment = new_comment_text.get("1.0", tk.END).strip()

            if new_rating < 1 or new_rating > 10:
                messagebox.showerror("Error", "Rating must be between 1 and 10.")
                return

            try:
                update_review(session.current_user_id, movie_id, new_rating, new_comment)
                messagebox.showinfo("Success", "Review updated successfully!")
                edit_window.destroy()
                open_movie_details(details_window, movie_id)  # Sayfayı güncelle
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update review.\n{e}")

        tk.Button(edit_frame, text="Submit", font=("Helvetica", 12), bg="#F8D7DA", fg="black", command=submit_edit).pack(pady=20)

    def handle_delete_review():
        if not has_user_reviewed_movie(session.current_user_id, movie_id):
            messagebox.showerror("Error", "You have not reviewed this movie yet.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete your review?")
        if confirm:
            try:
                delete_review(session.current_user_id, movie_id)
                messagebox.showinfo("Success", "Review deleted successfully!")
                open_movie_details(details_window, movie_id)  # Sayfayı güncelle
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete review.\n{e}")

    # Ana butonlar
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=20)

    add_review_button = tk.Button(
        button_frame,
        text="Add Review",
        width=15,
        font=("Helvetica", 12),
        bg="#D1E7DD",
        fg="black",
        activebackground="#A9D6C2",
        command=handle_add_review
    )
    add_review_button.grid(row=0, column=0, padx=5, pady=5)

    see_reviews_button = tk.Button(
        button_frame,
        text="See Reviews",
        width=15,
        font=("Helvetica", 12),
        bg="#CFE2FF",
        fg="black",
        activebackground="#A7C8F2",
        command=lambda: open_reviews_window(details_window, movie_id)
    )
    see_reviews_button.grid(row=0, column=1, padx=5, pady=5)

    # Edit Review Butonu
    edit_review_button = tk.Button(
        button_frame,
        text="Edit Your Review",
        width=15,
        font=("Helvetica", 12),
        bg="#FFE699",
        fg="black",
        activebackground="#FFDD66",
        command=handle_edit_review
    )
    edit_review_button.grid(row=1, column=0, padx=5, pady=5)

    # Delete Review Butonu
    delete_review_button = tk.Button(
        button_frame,
        text="Delete Your Review",
        width=15,
        font=("Helvetica", 12),
        bg="#FFB6B6",
        fg="black",
        activebackground="#FF8080",
        command=handle_delete_review
    )
    delete_review_button.grid(row=1, column=1, padx=5, pady=5)

    back_button = tk.Button(
        frame,
        text="Back",
        width=20,
        font=("Helvetica", 12),
        bg="#F8D7DA",
        fg="black",
        activebackground="#F1B0B7",
        command=lambda: open_movie_list(details_window)
    )
    back_button.pack(pady=10)

# İnceleme ekleme penceresini açar
def open_add_review_window(previous_window=None, movie_id=None):
    if previous_window:
        previous_window.destroy()

    review_window = tk.Toplevel()
    review_window.title("Add Review")
    set_window_position(review_window)

    frame = tk.Frame(review_window)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Rating (1-10):", font=("Helvetica", 12)).pack(pady=10)
    rating_spinbox = tk.Spinbox(frame, from_=1, to=10, width=5, font=("Helvetica", 12))
    rating_spinbox.pack()

    tk.Label(frame, text="Comment:", font=("Helvetica", 12)).pack(pady=10)
    comment_text = tk.Text(frame, width=40, height=5, font=("Helvetica", 12))
    comment_text.pack()

    def submit_review():
        try:
            rating = int(rating_spinbox.get())
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
            open_movie_details(review_window, movie_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit review.\n{e}")

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=20)

    submit_button = tk.Button(
        button_frame,
        text="Submit Review",
        width=15,
        font=("Helvetica", 12),
        bg="#D1E7DD",
        fg="black",
        activebackground="#A9D6C2",
        command=submit_review
    )
    submit_button.grid(row=0, column=0, padx=10)

    back_button = tk.Button(
        button_frame,
        text="Back",
        width=15,
        font=("Helvetica", 12),
        bg="#F8D7DA",
        fg="black",
        activebackground="#F1B0B7",
        command=lambda: open_movie_details(review_window, movie_id)
    )
    back_button.grid(row=0, column=1, padx=10)

# Filmin yorumlarını gösteren pencereyi açar
def open_reviews_window(previous_window=None, movie_id=None):
    if previous_window:
        previous_window.destroy()

    reviews_window = tk.Toplevel()
    reviews_window.title("Reviews")
    set_window_position(reviews_window)

    frame = tk.Frame(reviews_window)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(frame, text="Reviews", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=(0, 20))

    reviews = get_reviews_by_movie_id(movie_id)

    # Scrollbar ve Text alanı birlikte
    text_frame = tk.Frame(frame)
    text_frame.pack(pady=10)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    review_textbox = tk.Text(
        text_frame,
        wrap="word",
        yscrollcommand=scrollbar.set,
        font=("Helvetica", 11),
        width=50,
        height=20,
        relief="solid",
        bd=1
    )
    review_textbox.pack()

    scrollbar.config(command=review_textbox.yview)

    # Yorumları ekle
    if not reviews:
        review_textbox.insert(tk.END, "No reviews yet.\n")
    else:
        for review in reviews:
            user_id, rating, comment, date = review
            username = get_username_by_id(user_id)
            review_textbox.insert(tk.END, f"Username: {username}\nRating: {rating}/10\nDate: {date}\nComment: {comment}\n\n")

    review_textbox.config(state="disabled")

    # Back butonu
    back_button = tk.Button(
        frame,
        text="Back",
        width=20,
        font=("Helvetica", 12),
        bg="#F8D7DA",
        fg="black",
        activebackground="#F1B0B7",
        command=lambda: open_movie_details(reviews_window, movie_id)
    )
    back_button.pack(pady=20)

# Kullanıcıyı çıkış yaptırır ve login ekranına yönlendirir
def logout(previous_window=None):
    if previous_window:
        previous_window.destroy()
    open_login_window()

# Add Movie Penceresini Açan Fonksiyon
def open_add_movie_window(previous_window=None):
    add_movie_window = tk.Toplevel()
    add_movie_window.title("Add New Movie")
    set_window_position(add_movie_window)

    frame = tk.Frame(add_movie_window)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(frame, text="Add New Movie", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=(0, 20))

    # Form alanı
    form_frame = tk.Frame(frame)
    form_frame.pack()

    fields = ["Title", "Year", "Certificate", "Runtime", "Genre", "IMDB Rating", "Overview",
              "Meta Score", "Director", "Star 1", "Star 2", "Star 3", "Star 4", "Votes", "Gross"]
    entries = {}

    for idx, field in enumerate(fields):
        label = tk.Label(form_frame, text=field + ":", font=("Helvetica", 11), anchor="w")
        label.grid(row=idx, column=0, padx=(0, 5), pady=5, sticky="e")
        
        entry = tk.Entry(form_frame, font=("Helvetica", 11), width=28)  # width biraz küçüldü (30 → 28)
        entry.grid(row=idx, column=1, padx=(0, 20), pady=5, sticky="w")  # padding ekledik
        entries[field] = entry

    # Submit işlemi
    def submit_movie():
        try:
            title = entries["Title"].get()
            year = int(entries["Year"].get()) if entries["Year"].get() else None
            certificate = entries["Certificate"].get()
            runtime = int(entries["Runtime"].get()) if entries["Runtime"].get() else None
            genre = entries["Genre"].get()
            imdb_rating = float(entries["IMDB Rating"].get()) if entries["IMDB Rating"].get() else None
            overview = entries["Overview"].get()
            meta_score = int(entries["Meta Score"].get()) if entries["Meta Score"].get() else None
            director = entries["Director"].get()
            star1 = entries["Star 1"].get()
            star2 = entries["Star 2"].get()
            star3 = entries["Star 3"].get()
            star4 = entries["Star 4"].get()
            votes = int(entries["Votes"].get()) if entries["Votes"].get() else None
            gross = entries["Gross"].get()

            if not title:
                messagebox.showerror("Error", "Title is required.")
                return

            add_movie(title, year, certificate, runtime, genre, imdb_rating, overview, meta_score,
                      director, star1, star2, star3, star4, votes, gross)

            messagebox.showinfo("Success", "Movie added successfully!")
            add_movie_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add movie.\n{e}")

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=20)

    submit_button = tk.Button(
        button_frame,
        text="Submit",
        width=15,
        font=("Helvetica", 12),
        bg="#F8D7DA",
        fg="black",
        activebackground="#F1B0B7",
        command=submit_movie
    )

    submit_button.grid(row=0, column=0, padx=10)

    back_button = tk.Button(
        button_frame,
        text="Cancel",
        width=15,
        font=("Helvetica", 12),
        bg="#F8D7DA",
        fg="black",
        activebackground="#F1B0B7",
        command=lambda: add_movie_window.destroy()
    )
    back_button.grid(row=0, column=1, padx=10)