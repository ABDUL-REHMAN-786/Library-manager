import streamlit as st
import json
import os
import pandas as pd

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

# Initialize session state
if "library" not in st.session_state:
    st.session_state.library = load_library()

st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

st.title("📚 Personal Library Manager")

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Book", "Display Books", "Statistics", "Import/Export"])

# ✅ **Add a Book with Cover Upload**
if menu == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Read")
    cover = st.file_uploader("Upload Book Cover (optional)", type=["png", "jpg", "jpeg"])

    if st.button("Add Book"):
        if title and author and genre:
            book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status, "cover": ""}
            if cover:
                cover_path = f"covers/{title.replace(' ', '_')}.jpg"
                with open(cover_path, "wb") as f:
                    f.write(cover.getbuffer())
                book["cover"] = cover_path

            st.session_state.library.append(book)
            save_library(st.session_state.library)
            st.success(f'📖 Book "{title}" added successfully!')
        else:
            st.error("Please fill in all fields.")

# ✅ **Remove a Book**
elif menu == "Remove Book":
    st.subheader("🗑️ Remove a Book")
    titles = [book["title"] for book in st.session_state.library]
    title_to_remove = st.selectbox("Select a book to remove", titles) if titles else None

    if title_to_remove and st.button("Remove Book"):
        st.session_state.library = [book for book in st.session_state.library if book["title"] != title_to_remove]
        save_library(st.session_state.library)
        st.success(f'🚮 Book "{title_to_remove}" removed!')

# ✅ **Search for Books**
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

# ✅ **Display Books with Sorting & Filtering**
elif menu == "Display Books":
    st.subheader("📚 All Books in Library")
    if not st.session_state.library:
        st.info("No books available.")
    else:
        filter_genre = st.selectbox("Filter by Genre", ["All"] + list(set(book["genre"] for book in st.session_state.library)))
        filter_read = st.radio("Filter by Read Status", ["All", "Read", "Unread"])
        sort_by = st.radio("Sort By", ["Title", "Author", "Year"])

        filtered_books = st.session_state.library
        if filter_genre != "All":
            filtered_books = [book for book in filtered_books if book["genre"] == filter_genre]
        if filter_read == "Read":
            filtered_books = [book for book in filtered_books if book["read"]]
        elif filter_read == "Unread":
            filtered_books = [book for book in filtered_books if not book["read"]]

        if sort_by == "Title":
            filtered_books.sort(key=lambda x: x["title"])
        elif sort_by == "Author":
            filtered_books.sort(key=lambda x: x["author"])
        elif sort_by == "Year":
            filtered_books.sort(key=lambda x: x["year"], reverse=True)

        for book in filtered_books:
            col1, col2 = st.columns([0.2, 0.8])
            with col1:
                if book["cover"]:
                    st.image(book["cover"], width=100)
            with col2:
                st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')

# ✅ **Library Statistics with Charts**
elif menu == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read"])
    unread_books = total_books - read_books
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"✅ **Books Read:** {read_books} ({read_percentage:.2f}%)")
    st.write(f"📖 **Books Unread:** {unread_books}")

    # Pie Chart for Read Status
    if total_books > 0:
        data = pd.DataFrame({"Status": ["Read", "Unread"], "Count": [read_books, unread_books]})
        st.bar_chart(data.set_index("Status"))

# ✅ **Import & Export Library**
elif menu == "Import/Export":
    st.subheader("📥 Import / 📤 Export Library Data")

    # Export JSON
    if st.button("Export as JSON"):
        with open("library_export.json", "w") as f:
            json.dump(st.session_state.library, f, indent=4)
        st.success("Library exported as JSON!")

    # Export CSV
    if st.button("Export as CSV"):
        df = pd.DataFrame(st.session_state.library)
        df.to_csv("library_export.csv", index=False)
        st.success("Library exported as CSV!")

    # Import JSON
    uploaded_file = st.file_uploader("Import JSON File", type=["json"])
    if uploaded_file:
        imported_data = json.load(uploaded_file)
        st.session_state.library.extend(imported_data)
        save_library(st.session_state.library)
        st.success("Library imported successfully!")
