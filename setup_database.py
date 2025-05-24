# Import necessary functions from the previously created database.py module
from database import create_tables, load_movies_from_csv, generate_dummy_data

# Main function to execute primary operations
def main():
    # Create database tables
    print("🔵 Setting up the database and creating tables...")
    create_tables()
    print("✅ Tables created successfully.")

    # Load movies from the movies.csv file
    try:
        print("🔵 Loading movie data from movies.csv...")
        load_movies_from_csv('movies.csv')
        print("✅ Movie data loaded successfully.")
    except FileNotFoundError:
        print("⚠️ Warning: movies.csv not found. No movie data loaded.")

    # Generate dummy users and reviews
    print("🔵 Generating dummy users and reviews...")
    generate_dummy_data()
    print("✅ Dummy users and 2000 reviews created successfully.")

# If this script is run directly, call the main() function
if __name__ == "__main__":
    main()
