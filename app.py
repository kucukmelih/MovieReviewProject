import tkinter as tk
from login_window import open_login_window

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  
    open_login_window()
    root.mainloop()