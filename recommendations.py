import tkinter as tk
from tkinter import messagebox
from model import get_trained_model, recommend_for_user
from database import get_movie_by_id
import session
from movie_details import open_movie_details
from colors import (
    BG_COLOR, FRAME_BG, TITLE_COLOR, TEXT_COLOR,
    BUTTON_BG_LIGHT, BUTTON_BG_MEDIUM, BUTTON_BG_WARN,
    BUTTON_BG_DANGER, BUTTON_BG_DELETE, BUTTON_BG_WARNING,
    BUTTON_BG_SUCCESS, BUTTON_HOVER_BG, BUTTON_FG, ERROR_COLOR
)

# Set the default window size and position
def set_window_position(window, width=500, height=700, x=500, y=100):
    window.geometry(f"{width}x{height}+{x}+{y}")

# Opens the recommendation window for the current user
def open_recommendations_window(previous_window=None):
    if previous_window:
        previous_window.destroy()

    recommend_window = tk.Toplevel()
    recommend_window.title("Recommendations")
    recommend_window.configure(bg=BG_COLOR)
    set_window_position(recommend_window)

    main_frame = tk.Frame(recommend_window, bg=FRAME_BG)
    main_frame.pack(expand=True, fill="both")

    container = tk.Frame(main_frame, bg=FRAME_BG)
    container.pack(expand=True)

    # Title
    title_label = tk.Label(container, text="Recommended Movies", font=("Helvetica", 18, "bold"),
                           fg=TITLE_COLOR, bg=FRAME_BG)
    title_label.pack(pady=(0, 30))

    try:
        # Get the trained model and user id
        user_id = session.current_user_id
        model, trainset, movies_df = get_trained_model()

        # Get recommendations for the user
        try:
            recommendations = recommend_for_user(user_id, model, trainset, movies_df, n=5)
        except Exception:
            recommendations = None

        # If no recommendations are found
        if not recommendations:
            tk.Label(container, text="Please rate some movies first to get recommendations.",
                     font=("Helvetica", 12), fg=TEXT_COLOR, bg=FRAME_BG).pack(pady=10)
        else:
            for movie_id, predicted_rating in recommendations:
                title_row = movies_df[movies_df['id'] == movie_id]
                if not title_row.empty:
                    title = title_row.iloc[0]['title']

                    row_frame = tk.Frame(container, bg=FRAME_BG)
                    row_frame.pack(fill="x", pady=5, padx=20)

                    # Callback to view detailed info
                    def handle_view_details(m_id):
                        recommend_window.destroy()
                        open_movie_details(None, m_id, return_to=open_recommendations_window)

                    # Movie title with predicted rating
                    tk.Label(
                        row_frame,
                        text=f"{title} (Predicted Rating: {predicted_rating:.2f})",
                        font=("Helvetica", 12),
                        wraplength=300,
                        justify="left",
                        fg=TEXT_COLOR,
                        bg=FRAME_BG
                    ).pack(side="left", fill="x", expand=True, anchor="w")

                    # View details button
                    tk.Button(
                        row_frame,
                        text="View Details",
                        font=("Helvetica", 10),
                        bg=BUTTON_BG_LIGHT,
                        fg="black",
                        activebackground="#A9D6C2",
                        command=lambda m_id=movie_id: handle_view_details(m_id)
                    ).pack(side="right", padx=(10, 0))

    except Exception as e:
        tk.Label(container, text=f"Error: {e}", font=("Helvetica", 12),
                 fg="red", bg=FRAME_BG).pack(pady=10)

    # Back button to main menu
    back_button = tk.Button(
        container,
        text="Back",
        font=("Helvetica", 12),
        bg=BUTTON_BG_DANGER,
        fg="black",
        activebackground="#F1B0B7",
        command=lambda: (
            recommend_window.destroy(),
            __import__("main_menu").open_main_menu()
        )
    )
    back_button.pack(pady=20)
