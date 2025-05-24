
# 🎬 Movie Review Project

A simple movie review application built with Python and Tkinter.  
Users can register, login, view movies, leave reviews, and get movie recommendations.

---

## 📦 Features

- User registration and login
- View movie list
- View detailed movie information
- Add and view movie reviews
- Calculate and display average movie ratings
- Personalized movie recommendations based on user reviews

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
```

2. **Prepare the database:**

Run the setup script to create the database and load sample data:

```bash
python setup_database.py
```

This will:

- Create the `movies.db` SQLite database file.
- Load sample movies from `movies.csv`.

3. **Start the application:**

Launch the login window:

```bash
python app.py
```

Enjoy!

---

## 📂 File Structure

- `app.py` – The main entry point of the program, starts the application.
- `colors.py` – sColors for UI Design.
- `database.py` – Handles database connections and basic queries (Users, Movies, Reviews).
- `login_window.py` – GUI for user login and registration.
- `main_menu.py` – Main menu GUI after login (movie list, add reviews, access recommendations).
- `model.py` – Machine learning model and similarity calculations for the recommendation system.
- `movie_details.py` – Window and functions to display detailed movie information.
- `recommendations.py` – GUI and logic for the recommendation system.
- `session.py` – Session management storing current user information.
- `setup_database.py` – Creates the database and loads data from the `movies.csv` file.
- `movies.csv` – CSV file containing movie data.
- `movies.db` – SQLite database file (created by `setup_database.py`).
- `README.md` – Project documentation and usage instructions.

---

## 📌 Important Notes

- Before running the application, make sure `movies.csv` is available in the project folder.
- If you want to add your own movies, simply edit or replace `movies.csv` before running `setup_database.py`.
- Passwords are currently stored in plain text for simplicity.  
  ➔ **In a real-world application, always hash passwords!**
- The recommendation system uses user reviews to suggest movies similar to those the user liked.

---

## ✨ Future Improvements

- Implement password hashing for better security
- Allow users to edit or delete their reviews
- Improve GUI design with Tkinter themes
- Add search and filter functionality for movies
- Enhance recommendation algorithm with more advanced techniques

---
