import streamlit as st
import json
import os

LIBRARY_FILE = "library.json"

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Initialize library
if "library" not in st.session_state:
    st.session_state.library = load_library()

st.title("📚 Personal Library Manager")

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Book", "Display Books", "Statistics"])

if menu == "Add Book":
    st.subheader("➕ Add a Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Read")

    if st.button("Add Book"):
        if title and author and genre:
            book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status}
            st.session_state.library.append(book)
            save_library(st.session_state.library)
            st.success(f'📖 Book "{title}" added successfully!')
        else:
            st.error("Please fill in all fields.")

elif menu == "Remove Book":
    st.subheader("🗑️ Remove a Book")
    titles = [book["title"] for book in st.session_state.library]
    title_to_remove = st.selectbox("Select a book to remove", titles) if titles else None

    if title_to_remove and st.button("Remove Book"):
        st.session_state.library = [book for book in st.session_state.library if book["title"] != title_to_remove]
        save_library(st.session_state.library)
        st.success(f'🚮 Book "{title_to_remove}" removed!')

elif menu == "Search Book":
    st.subheader("🔍 Search for a Book")
    query = st.text_input("Enter title or author")

    if query:
        results = [book for book in st.session_state.library if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]
        if results:
            for book in results:
                st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')
        else:
            st.warning("No books found.")

elif menu == "Display Books":
    st.subheader("📚 All Books in Library")
    if not st.session_state.library:
        st.info("No books available.")
    else:
        for book in st.session_state.library:
            st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')

elif menu == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"✅ **Books Read:** {read_books} ({read_percentage:.2f}%)")

# Run with: streamlit run app.py
