import streamlit as st
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

# 🎉 Streamlit UI Setup
st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="wide")

st.title("📚 Personal Library Manager")
st.sidebar.title("📖 Menu")

# Load books from file
library = load_library()

# 🎈 Celebration effect
def celebrate():
    st.balloons()
    st.success("🎉 Action successful!")

# 🎭 Add a new book
def add_book():
    with st.form("add_book_form"):
        title = st.text_input("📕 Book Title")
        author = st.text_input("✍️ Author")
        year = st.number_input("📅 Publication Year", min_value=1000, max_value=3000, step=1)
        genre = st.text_input("📚 Genre")
        read_status = st.checkbox("✅ Mark as Read")
        submit = st.form_submit_button("➕ Add Book")

        if submit:
            if title and author:
                library.append({"title": title, "author": author, "year": year, "genre": genre, "read": read_status})
                save_library(library)
                st.success(f"📖 '{title}' added successfully!")
                celebrate()
            else:
                st.error("❌ Please enter both title and author.")

# ❌ Remove a book
def remove_book():
    book_titles = [book["title"] for book in library]
    if book_titles:
        book_to_remove = st.selectbox("📕 Select a book to remove", book_titles)
        if st.button("🗑️ Remove Book"):
            global library
            library = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.success(f"🗑️ '{book_to_remove}' removed!")
            celebrate()
    else:
        st.warning("📌 No books available to remove.")

# 🔎 Search for a book
def search_book():
    search_term = st.text_input("🔍 Search by Title or Author").lower()
    if st.button("🔎 Search"):
        results = [book for book in library if search_term in book["title"].lower() or search_term in book["author"].lower()]
        if results:
            for book in results:
                st.write(f'📖 **{book["title"]}** by {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')
        else:
            st.warning("🚫 No matching books found.")

# 📚 Display all books
def display_books():
    if not library:
        st.warning("📌 No books available!")
    else:
        for book in library:
            st.write(f'📖 **{book["title"]}** by {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')

# 📊 Show library statistics
def display_statistics():
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    unread_books = total_books - read_books
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0

    st.subheader("📊 Library Statistics")
    st.metric("📚 Total Books", total_books)
    st.metric("✅ Books Read", read_books)
    st.metric("📖 Books Unread", unread_books)

    # 📊 Chart Visualization
    if total_books > 0:
        st.bar_chart({"Read": read_books, "Unread": unread_books})

# 📂 File Upload & Download Feature
def file_management():
    st.subheader("📂 Backup & Restore Library")

    # 📥 Download File
    st.download_button("⬇️ Download Library", data=json.dumps(library, indent=4), file_name="library.json")

    # 📤 Upload File
    uploaded_file = st.file_uploader("📤 Upload Library JSON File", type=["json"])
    if uploaded_file is not None:
        data = json.load(uploaded_file)
        global library
        library = data
        save_library(library)
        st.success("✅ Library uploaded successfully!")

# 🎛️ Menu System
menu = st.sidebar.radio("📌 Choose an option", ["➕ Add Book", "🗑️ Remove Book", "🔎 Search Book", "📚 Display All Books", "📊 Show Statistics", "📂 Backup & Restore"])

if menu == "➕ Add Book":
    add_book()
elif menu == "🗑️ Remove Book":
    remove_book()
elif menu == "🔎 Search Book":
    search_book()
elif menu == "📚 Display All Books":
    display_books()
elif menu == "📊 Show Statistics":
    display_statistics()
elif menu == "📂 Backup & Restore":
    file_management()

# 🎉 Footer Message
st.sidebar.markdown("---")
st.sidebar.markdown("📖 *Developed by Abdul Rehman*")
