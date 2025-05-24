import tkinter as tk
from tkinter import messagebox, ttk
import re
from database import check_login, add_user
import session  # For current_user_id and current_username

# Color palette
BG_COLOR = "#1E1E2F"          # Dark background
FRAME_BG = "#2A2A40"          # Frame background
TITLE_COLOR = "#FFD369"       # Yellow title text
BUTTON_BG = "#3F51B5"         # Blue button background
BUTTON_HOVER_BG = "#303F9F"   # Button hover background
BUTTON_FG = "#FFFFFF"         # Button text
TEXT_COLOR = "#E0E0E0"        # General text color
ERROR_COLOR = "#E53935"       # Error messages

def set_window_position(window, width=500, height=700, x=500, y=100):
    window.geometry(f"{width}x{height}+{x}+{y}")

# Email format validation
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

# Password format validation
def is_valid_password(password):
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>])[A-Za-z\d!@#$%^&*(),.?\":{}|<>]{6,}$"
    return re.match(pattern, password) is not None

# Configure consistent button style
def style_buttons():
    style = ttk.Style()
    style.theme_use('clam')  
    style.configure("TButton",
        background=BUTTON_BG,
        foreground=BUTTON_FG,
        font=("Helvetica", 14),
        padding=6,
        borderwidth=0
    )
    style.map("TButton",
        background=[('active', BUTTON_HOVER_BG)],
        foreground=[('disabled', '#a3a3a3')]
    )

# Login Window
def open_login_window(previous_window=None):
    if previous_window:
        previous_window.destroy()

    login_window = tk.Toplevel()
    login_window.title("Login")
    set_window_position(login_window)
    login_window.configure(bg=BG_COLOR)

    frame = tk.Frame(login_window, bg=FRAME_BG, padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Welcome to Movie Review Project", font=("Helvetica", 18, "bold"), fg=TITLE_COLOR, bg=FRAME_BG).pack(pady=(0, 30))

    form_frame = tk.Frame(frame, bg=FRAME_BG)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Username:", font=("Helvetica", 12), fg=TEXT_COLOR, bg=FRAME_BG).grid(row=0, column=0, padx=10, pady=10, sticky='e')
    username_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(form_frame, text="Password:", font=("Helvetica", 12), fg=TEXT_COLOR, bg=FRAME_BG).grid(row=1, column=0, padx=10, pady=10, sticky='e')
    password_entry = tk.Entry(form_frame, show="*", font=("Helvetica", 12), width=30)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    message_label = tk.Label(frame, text="", fg=ERROR_COLOR, font=("Helvetica", 10), bg=FRAME_BG)
    message_label.pack(pady=5)

    def login():
        username = username_entry.get()
        password = password_entry.get()

        user = check_login(username, password)

        if user:
            session.current_user_id = user[0]
            session.current_username = user[1]
            from main_menu import open_main_menu
            open_main_menu(login_window)
        else:
            message_label.config(text="Invalid username or password.")

    button_frame = tk.Frame(frame, bg=FRAME_BG)
    button_frame.pack(pady=20)

    style_buttons()

    ttk.Button(button_frame, text="Login", command=login, style="TButton").grid(row=0, column=0, padx=10)
    ttk.Button(button_frame, text="Register", command=lambda: open_register_window(login_window), style="TButton").grid(row=0, column=1, padx=10)

# Registration Window
def open_register_window(previous_window=None):
    if previous_window:
        previous_window.destroy()

    register_window = tk.Toplevel()
    register_window.title("Register")
    set_window_position(register_window)
    register_window.configure(bg=BG_COLOR)

    frame = tk.Frame(register_window, bg=FRAME_BG, padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Create New Account", font=("Helvetica", 18, "bold"), fg=TITLE_COLOR, bg=FRAME_BG).pack(pady=(0, 30))

    form_frame = tk.Frame(frame, bg=FRAME_BG)
    form_frame.pack(pady=10)

    entries = {}
    labels = ["Username", "Email", "Password", "Age", "Location"]
    for i, label in enumerate(labels):
        tk.Label(form_frame, text=f"{label}:", font=("Helvetica", 12), fg=TEXT_COLOR, bg=FRAME_BG).grid(row=i, column=0, padx=10, pady=10, sticky='e')
        show = "*" if label == "Password" else None
        entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30, show=show)
        entry.grid(row=i, column=1, padx=10, pady=10)
        entries[label.lower()] = entry

    # Gender field (combobox)
    tk.Label(form_frame, text="Gender:", font=("Helvetica", 12), fg=TEXT_COLOR, bg=FRAME_BG).grid(row=4, column=0, padx=10, pady=10, sticky='e')
    gender_combo = ttk.Combobox(form_frame, font=("Helvetica", 12), width=28, state="readonly")
    gender_combo['values'] = ("Male", "Female", "Other")
    gender_combo.grid(row=4, column=1, padx=10, pady=10)
    gender_combo.current(0)

    def register():
        username = entries["username"].get().strip()
        email = entries["email"].get().strip()
        password = entries["password"].get()
        age = entries["age"].get().strip()
        gender = gender_combo.get()
        location = entries["location"].get().strip()

        if not username or not email or not password:
            messagebox.showerror("Error", "Username, Email and Password are required.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        if not is_valid_password(password):
            messagebox.showerror("Error", "Password must be at least 6 characters, including letters, numbers, and symbols.")
            return

        try:
            age = int(age) if age else None
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
            return

        add_user(username, email, password, age, gender, location)
        messagebox.showinfo("Success", "Registration successful!")
        open_login_window(register_window)

    button_frame = tk.Frame(frame, bg=FRAME_BG)
    button_frame.pack(pady=20)

    style_buttons()

    ttk.Button(button_frame, text="Register", command=register, style="TButton").grid(row=0, column=0, padx=10)
    ttk.Button(button_frame, text="Back", command=lambda: open_login_window(register_window), style="TButton").grid(row=0, column=1, padx=10)

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_login_window()
    root.mainloop()
