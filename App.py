import json
import os

# 📂 File to store books
LIBRARY_FILE = "library.json"

# 📚 Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# 💾 Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# 📖 Add a new book
def add_book(library):
    title = input("📕 Enter book title: ").strip()
    author = input("✍️ Enter author name: ").strip()
    try:
        year = int(input("📅 Enter publication year: "))
    except ValueError:
        print("❌ Invalid year! Please enter a number.")
        return
    genre = input("📚 Enter genre: ").strip()
    read_status = input("✅ Have you read this book? (yes/no): ").strip().lower() == "yes"

    book = {"title": title, "author": author, "year": year, "genre": genre, "read": read_status}
    library.append(book)
    save_library(library)
    print(f'✅ Book "{title}" added successfully!\n')

# 🚮 Remove a book
def remove_book(library):
    title_to_remove = input("📕 Enter the title of the book to remove: ").strip()
    updated_library = [book for book in library if book["title"].lower() != title_to_remove.lower()]

    if len(updated_library) == len(library):
        print("🚫 Book not found!")
    else:
        save_library(updated_library)
        print(f'🗑️ Book "{title_to_remove}" removed successfully!\n')

# 🔎 Search for a book
def search_book(library):
    query = input("🔍 Enter title or author to search: ").strip().lower()
    results = [book for book in library if query in book["title"].lower() or query in book["author"].lower()]

    if results:
        print("\n📖 Matching Books:")
        for book in results:
            print(f'📚 "{book["title"]}" - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')
    else:
        print("🚫 No matching books found!")

# 📚 Display all books
def display_books(library):
    if not library:
        print("📌 No books available!")
    else:
        print("\n📖 Your Library Collection:")
        for book in library:
            print(f'📚 "{book["title"]}" - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')

# 📊 Show library statistics
def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    unread_books = total_books - read_books
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0

    print("\n📊 Library Statistics:")
    print(f"📚 Total Books: {total_books}")
    print(f"✅ Books Read: {read_books} ({read_percentage:.2f}%)")
    print(f"📖 Books Unread: {unread_books}")

# 🎛️ Menu System
def main():
    library = load_library()

    while True:
        print("\n📚 PERSONAL LIBRARY MANAGER")
        print("1️⃣ Add a Book")
        print("2️⃣ Remove a Book")
        print("3️⃣ Search for a Book")
        print("4️⃣ Display All Books")
        print("5️⃣ Show Statistics")
        print("6️⃣ Exit")
        choice = input("📌 Select an option (1-6): ").strip()

        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            search_book(library)
        elif choice == "4":
            display_books(library)
        elif choice == "5":
            display_statistics(library)
        elif choice == "6":
            print("👋 Exiting... Have a great day! 📚")
            break
        else:
            print("⚠️ Invalid option! Please choose a number between 1-6.")

# 🚀 Run the program
if __name__ == "__main__":
    main()
