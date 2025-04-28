import tkinter as tk
from tkinter import messagebox
from database import check_login, add_user
import session  # current_user_id ve current_username değişkenleri için

# Login penceresini açan fonksiyon
def open_login_window(previous_window=None):
    if previous_window:
        previous_window.destroy()  # Önceki pencereyi kapat

    login_window = tk.Toplevel()  # Yeni bir pencere oluştur
    login_window.title("Login")
    login_window.geometry("800x600")

    # Username label ve giriş alanı
    tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    # Password label ve giriş alanı
    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(login_window, show="*")  # Şifre girişinde karakterleri gizle
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Hatalı giriş mesajı göstermek için boş bir Label
    message_label = tk.Label(login_window, text="", fg="red", font=("Helvetica", 10))
    message_label.grid(row=3, column=0, columnspan=2)

    # Login işlemini gerçekleştiren iç fonksiyon
    def login():
        username = username_entry.get()
        password = password_entry.get()

        user = check_login(username, password)  # Veritabanında kullanıcıyı kontrol et

        if user:
            # Giriş başarılıysa session bilgilerini güncelle
            session.current_user_id = user[0]
            session.current_username = user[1]

            # Main menu ekranını aç
            from main_menu import open_main_menu
            open_main_menu(login_window)
        else:
            # Giriş başarısızsa hata mesajı göster
            message_label.config(text="Invalid username or password.")

    # Login butonu
    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.grid(row=2, column=0, pady=10)

    # Register butonu (kayıt ekranına yönlendirir)
    register_button = tk.Button(login_window, text="Register", command=lambda: open_register_window(login_window))
    register_button.grid(row=2, column=1, pady=10)

# Register (Kayıt) penceresini açan fonksiyon
def open_register_window(previous_window=None):
    if previous_window:
        previous_window.destroy()  # Önceki pencereyi kapat

    register_window = tk.Toplevel()  # Yeni bir pencere oluştur
    register_window.title("Register")
    register_window.geometry("350x400")

    # Kayıt için gerekli alanlar
    fields = ["Username", "Email", "Password", "Age", "Gender", "Location"]
    entries = {}

    # Alanları ve giriş kutularını oluştur
    for idx, field in enumerate(fields):
        tk.Label(register_window, text=field + ":").grid(row=idx, column=0, padx=10, pady=10, sticky='e')
        entry = tk.Entry(register_window)
        entry.grid(row=idx, column=1, padx=10, pady=10)
        entries[field] = entry

    # Register işlemini gerçekleştiren iç fonksiyon
    def register():
        username = entries["Username"].get()
        email = entries["Email"].get()
        password = entries["Password"].get()
        age = entries["Age"].get()
        gender = entries["Gender"].get()
        location = entries["Location"].get()

        # Zorunlu alanlar kontrolü
        if not (username and email and password):
            messagebox.showerror("Error", "Username, Email and Password are required.")
            return

        # Age girişini integer'a çevirme (hata olursa None yapıyoruz)
        try:
            age = int(age)
        except ValueError:
            age = None

        # Kullanıcıyı veritabanına ekle
        add_user(username, email, password, age, gender, location)
        messagebox.showinfo("Success", "Registration successful!")

        # 🔥 Başarılı kayıt sonrası login ekranına geri dön
        open_login_window(register_window)

    # Register butonu
    register_button = tk.Button(register_window, text="Register", command=register)
    register_button.grid(row=len(fields), column=0, pady=10)

    # Geri dön butonu (login ekranına yönlendirir)
    back_button = tk.Button(register_window, text="Back", command=lambda: open_login_window(register_window))
    back_button.grid(row=len(fields), column=1, pady=10)

# Eğer bu dosya doğrudan çalıştırılırsa login ekranı göster
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle (sadece login/register pencereleri kullanılacak)
    open_login_window()
    root.mainloop()
