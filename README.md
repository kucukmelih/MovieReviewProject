# Movie Review Project 🎬

A simple movie review application built with Python and Tkinter.  
Users can register, login, view movies, and leave reviews.

---

## 📦 Features

- User registration and login
- View movie list
- View detailed movie information
- Add and view movie reviews
- Average movie rating calculation

---

## 🛠️ Technologies

- Python 3
- Tkinter (GUI)
- SQLite3 (Database)

---

## 🚀 Setup and Installation

Follow these steps to set up and run the project:

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/MovieReviewProject.git
cd MovieReviewProject
    Prepare the database:

    Run the setup script to create the database and tables:

python setup_database.py

    This will:

        Create the movies.db SQLite database file.

        Load sample movies from movies.csv.

    Start the application:

    Launch the login window:

python login_window.py

    Enjoy!

📂 File Structure

database.py          # Database operations (Users, Movies, Reviews)
login_window.py      # Login and Registration GUI
main_menu.py         # Main menu after login (view movies, add reviews)
session.py           # Session management (store current user info)
setup_database.py    # Initial database setup (create tables, load CSV)
movies.csv           # Sample movie data
README.md            # Project information

📌 Important Notes

    Before running the application, make sure movies.csv is available in the project folder.

    If you want to add your own movies, simply edit or replace movies.csv before running setup_database.py.

    Passwords are stored in plain text for simplicity. In a real-world application, always hash passwords!

✨ Future Improvements

    Add password hashing

    Allow users to edit or delete their reviews

    Better GUI design with Tkinter themes

    Search/filter movies
