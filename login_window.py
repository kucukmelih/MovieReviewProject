import tkinter as tk
from tkinter import messagebox
from database import check_login, add_user
import session  # current_user_id ve current_username değişkenleri için

# Pencere Konumu
def set_window_position(window, width=500, height=700, x=500, y=100):
    window.geometry(f"{width}x{height}+{x}+{y}")

# Login penceresini açan fonksiyon
def open_login_window(previous_window=None):
    if previous_window:
        previous_window.destroy()

    login_window = tk.Toplevel()
    login_window.title("Login")
    set_window_position(login_window)

    frame = tk.Frame(login_window)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Başlık
    title_label = tk.Label(frame, text="Welcome to Movie Review Project", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=(0, 30))  # Üst boşluk yok, altta 30px boşluk

    # Form kısmı
    form_frame = tk.Frame(frame)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Username:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
    username_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(form_frame, text="Password:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
    password_entry = tk.Entry(form_frame, show="*", font=("Helvetica", 12), width=30)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Hatalı giriş mesajı
    message_label = tk.Label(frame, text="", fg="red", font=("Helvetica", 10))
    message_label.pack(pady=5)

    # Login işlemini gerçekleştiren iç fonksiyon
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

    # Butonlar
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=20)

    login_button = tk.Button(
        button_frame,
        text="Login",
        command=login,
        font=("Helvetica", 14),
        width=15,
        bg="#D1E7DD",     
        fg="black",
        activebackground="#A9D6C2"
    )
    login_button.grid(row=0, column=0, padx=10)

    register_button = tk.Button(
        button_frame,
        text="Register",
        command=lambda: open_register_window(login_window),
        font=("Helvetica", 14),
        width=15,
        bg="#CFE2FF",     
        fg="black",
        activebackground="#A7C8F2"
    )
    register_button.grid(row=0, column=1, padx=10)

# Register penceresini açan fonksiyon
def open_register_window(previous_window=None):
    if previous_window:
        previous_window.destroy()

    register_window = tk.Toplevel()
    register_window.title("Register")
    set_window_position(register_window)

    frame = tk.Frame(register_window)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(frame, text="Create New Account", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=(0, 30))

    form_frame = tk.Frame(frame)
    form_frame.pack(pady=10)

    fields = ["Username", "Email", "Password", "Age", "Gender", "Location"]
    entries = {}

    for idx, field in enumerate(fields):
        tk.Label(form_frame, text=field + ":", font=("Helvetica", 12)).grid(row=idx, column=0, padx=10, pady=10, sticky='e')
        entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        entry.grid(row=idx, column=1, padx=10, pady=10)
        entries[field] = entry

    def register():
        username = entries["Username"].get()
        email = entries["Email"].get()
        password = entries["Password"].get()
        age = entries["Age"].get()
        gender = entries["Gender"].get()
        location = entries["Location"].get()

        if not (username and email and password):
            messagebox.showerror("Error", "Username, Email and Password are required.")
            return

        try:
            age = int(age)
        except ValueError:
            age = None

        add_user(username, email, password, age, gender, location)
        messagebox.showinfo("Success", "Registration successful!")
        open_login_window(register_window)

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=20)

    register_button = tk.Button(
        button_frame,
        text="Register",
        command=register,
        font=("Helvetica", 14),
        width=15,
        bg="#D1E7DD",
        fg="black",
        activebackground="#A9D6C2"
    )
    register_button.grid(row=0, column=0, padx=10)

    back_button = tk.Button(
        button_frame,
        text="Back",
        command=lambda: open_login_window(register_window),
        font=("Helvetica", 14),
        width=15,
        bg="#F8D7DA",     
        fg="black",
        activebackground="#F1B0B7"
    )
    back_button.grid(row=0, column=1, padx=10)

# Login ekranını göster
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_login_window()
    root.mainloop()