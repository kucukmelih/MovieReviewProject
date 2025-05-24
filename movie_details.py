import tkinter as tk
from tkinter import messagebox
from database import (
    get_movie_by_id, get_average_rating, has_user_reviewed_movie,
    update_review, delete_review, add_review, get_reviews_by_movie_id, get_username_by_id
)
import session
from colors import (
    BG_COLOR, FRAME_BG, TITLE_COLOR, TEXT_COLOR,
    BUTTON_BG_LIGHT, BUTTON_BG_MEDIUM, BUTTON_BG_WARN,
    BUTTON_BG_DANGER, BUTTON_BG_DELETE
)

# Opens the movie details window with review options
def open_movie_details(previous_window=None, movie_id=None, return_to=None):
    if previous_window:
        previous_window.destroy()

    movie = get_movie_by_id(movie_id)
    if not movie:
        messagebox.showerror("Error", "Movie not found!")
        return

    # Setup window
    details_window = tk.Toplevel()
    details_window.title("Movie Details")
    details_window.configure(bg=BG_COLOR)
    details_window.geometry("500x700+500+100")

    frame = tk.Frame(details_window, bg=FRAME_BG)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Display average rating
    average_rating = get_average_rating(movie_id)
    avg_text = f"Average Rating: {average_rating:.2f} / 10" if average_rating is not None else "Average Rating: No ratings yet."
    tk.Label(frame, text=avg_text, font=("Helvetica", 14, "bold"),
             fg=TITLE_COLOR, bg=FRAME_BG).pack(pady=10)

    # Display movie metadata
    fields = ["Title", "Year", "Certificate", "Runtime", "Genre",
              "IMDB Rating", "Overview", "Meta Score", "Director",
              "Star 1", "Star 2", "Star 3", "Star 4", "Votes", "Gross"]

    for idx, field in enumerate(fields):
        value = movie[idx + 1] if idx + 1 < len(movie) else ""
        text = f"{field}: {value}"
        tk.Label(frame, text=text, anchor="w", justify="left", wraplength=450,
                 font=("Helvetica", 12), fg=TEXT_COLOR, bg=FRAME_BG).pack(padx=10, pady=5)

    # Button handlers
    def handle_add_review():
        if has_user_reviewed_movie(session.current_user_id, movie_id):
            messagebox.showerror("Error", "You have already reviewed this movie.")
        else:
            open_add_review_window(details_window, movie_id, return_to=lambda: open_movie_details(movie_id=movie_id, return_to=return_to))

    def handle_edit_review():
        if not has_user_reviewed_movie(session.current_user_id, movie_id):
            messagebox.showerror("Error", "You have not reviewed this movie yet.")
            return

        # Open edit window
        edit_window = tk.Toplevel()
        edit_window.title("Edit Your Review")
        edit_window.configure(bg=BG_COLOR)
        edit_window.geometry("400x400+600+200")

        edit_frame = tk.Frame(edit_window, bg=FRAME_BG)
        edit_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(edit_frame, text="New Rating (1-10):", font=("Helvetica", 12),
                 fg=TEXT_COLOR, bg=FRAME_BG).pack(pady=10)
        new_rating_spinbox = tk.Spinbox(edit_frame, from_=1, to=10, width=5, font=("Helvetica", 12))
        new_rating_spinbox.pack()

        tk.Label(edit_frame, text="New Comment:", font=("Helvetica", 12),
                 fg=TEXT_COLOR, bg=FRAME_BG).pack(pady=10)
        new_comment_text = tk.Text(edit_frame, width=40, height=5, font=("Helvetica", 12),
                                   bg=FRAME_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
        new_comment_text.pack()

        # Submit updated review
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
                open_movie_details(details_window, movie_id, return_to=return_to)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update review.\n{e}")

        tk.Button(edit_frame, text="Submit", font=("Helvetica", 12),
                  bg=BUTTON_BG_DANGER, fg="black", activebackground="#F1B0B7",
                  command=submit_edit).pack(pady=20)

    def handle_delete_review():
        if not has_user_reviewed_movie(session.current_user_id, movie_id):
            messagebox.showerror("Error", "You have not reviewed this movie yet.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete your review?")
        if confirm:
            try:
                delete_review(session.current_user_id, movie_id)
                messagebox.showinfo("Success", "Review deleted successfully!")
                open_movie_details(details_window, movie_id, return_to=return_to)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete review.\n{e}")

    # Action buttons
    button_frame = tk.Frame(frame, bg=FRAME_BG)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Add Review", width=15, font=("Helvetica", 12),
              bg=BUTTON_BG_LIGHT, fg="black", command=handle_add_review).grid(row=0, column=0, padx=5, pady=5)

    tk.Button(button_frame, text="See Reviews", width=15, font=("Helvetica", 12),
              bg=BUTTON_BG_MEDIUM, fg="black",
              command=lambda: open_reviews_window(details_window, movie_id, return_to=lambda: open_movie_details(movie_id=movie_id, return_to=return_to))
              ).grid(row=0, column=1, padx=5, pady=5)

    tk.Button(button_frame, text="Edit Your Review", width=15, font=("Helvetica", 12),
              bg=BUTTON_BG_WARN, fg="black", command=handle_edit_review).grid(row=1, column=0, padx=5, pady=5)

    tk.Button(button_frame, text="Delete Your Review", width=15, font=("Helvetica", 12),
              bg=BUTTON_BG_DELETE, fg="black", command=handle_delete_review).grid(row=1, column=1, padx=5, pady=5)

    tk.Button(frame, text="Back", width=20, font=("Helvetica", 12),
              bg=BUTTON_BG_DANGER, fg="black",
              command=lambda: (
                  details_window.destroy(),
                  return_to() if return_to else None
              )).pack(pady=10)

# Opens the window to submit a new review
def open_add_review_window(previous_window=None, movie_id=None, return_to=None):
    if previous_window:
        previous_window.destroy()

    review_window = tk.Toplevel()
    review_window.title("Add Review")
    review_window.configure(bg=BG_COLOR)
    review_window.geometry("500x400+500+150")

    frame = tk.Frame(review_window, bg=FRAME_BG)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Rating (1-10):", font=("Helvetica", 12),
             fg=TEXT_COLOR, bg=FRAME_BG).pack(pady=10)
    rating_spinbox = tk.Spinbox(frame, from_=1, to=10, width=5, font=("Helvetica", 12))
    rating_spinbox.pack()

    tk.Label(frame, text="Comment:", font=("Helvetica", 12),
             fg=TEXT_COLOR, bg=FRAME_BG).pack(pady=10)
    comment_text = tk.Text(frame, width=40, height=5, font=("Helvetica", 12),
                           bg=FRAME_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
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
            open_movie_details(review_window, movie_id, return_to=return_to)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit review.\n{e}")

    button_frame = tk.Frame(frame, bg=FRAME_BG)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Submit Review", width=15, font=("Helvetica", 12),
              bg=BUTTON_BG_LIGHT, fg="black", command=submit_review).grid(row=0, column=0, padx=10)

    tk.Button(button_frame, text="Back", width=15, font=("Helvetica", 12),
              bg=BUTTON_BG_DANGER, fg="black",
              command=lambda: (
                  review_window.destroy(),
                  return_to() if return_to else open_movie_details(movie_id=movie_id)
              )).grid(row=0, column=1, padx=10)

# Opens a scrollable window showing all reviews for a movie
def open_reviews_window(previous_window=None, movie_id=None, return_to=None):
    if previous_window:
        previous_window.destroy()

    reviews_window = tk.Toplevel()
    reviews_window.title("Reviews")
    reviews_window.configure(bg=BG_COLOR)
    reviews_window.geometry("500x600+500+100")

    frame = tk.Frame(reviews_window, bg=FRAME_BG)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Reviews", font=("Helvetica", 18, "bold"),
             fg=TITLE_COLOR, bg=FRAME_BG).pack(pady=(0, 20))

    reviews = get_reviews_by_movie_id(movie_id)

    text_frame = tk.Frame(frame, bg=FRAME_BG)
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
        bd=1,
        bg=FRAME_BG,
        fg=TEXT_COLOR,
        insertbackground=TEXT_COLOR
    )
    review_textbox.pack()
    scrollbar.config(command=review_textbox.yview)

    if not reviews:
        review_textbox.insert(tk.END, "No reviews yet.\n")
    else:
        for review in reviews:
            user_id, rating, comment, date = review
            username = get_username_by_id(user_id)
            review_textbox.insert(tk.END, f"Username: {username}\nRating: {rating}/10\nDate: {date}\nComment: {comment}\n\n")

    review_textbox.config(state="disabled")

    tk.Button(frame, text="Back", width=20, font=("Helvetica", 12),
              bg=BUTTON_BG_DANGER, fg="black",
              command=lambda: (
                  reviews_window.destroy(),
                  return_to() if return_to else open_movie_details(movie_id=movie_id)
              )).pack(pady=20)
