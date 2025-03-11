import streamlit as st
import json
import time
from streamlit_lottie import st_lottie

# Load Animation
def load_lottie(url):
    return f'<lottie-player src="{url}" background="transparent" speed="1" loop autoplay></lottie-player>'

# Celebrations
def celebrate():
    st.balloons()
    time.sleep(1)
    st.snow()

# Load Library from File
def load_library():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save Library to File
def save_library():
    with open("library.json", "w") as file:
        json.dump(library, file, indent=4)

# Initialize Library
library = load_library()

# Function to Add a Book
def add_book():
    global library
    st.subheader("📚 Add a New Book")
    title = st.text_input("📖 Enter Book Title")
    author = st.text_input("✍️ Enter Author Name")
    year = st.number_input("📅 Enter Publication Year", min_value=0, format="%d")
    genre = st.text_input("🎭 Enter Genre")
    read_status = st.radio("✅ Have You Read This Book?", ["Yes", "No"])

    if st.button("➕ Add Book"):
        if title and author and year and genre:
            library.append({
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": True if read_status == "Yes" else False
            })
            save_library()
            st.success(f"📘 '{title}' added successfully!")
            celebrate()
        else:
            st.error("⚠️ Please fill in all fields.")

# Function to Remove a Book
def remove_book():
    global library
    st.subheader("🗑️ Remove a Book")
    book_titles = [book["title"] for book in library]
    
    if book_titles:
        book_to_remove = st.selectbox("📕 Select a book to remove", book_titles)
        if st.button("🗑️ Remove Book"):
            library = [book for book in library if book["title"] != book_to_remove]
            save_library()
            st.success(f"🗑️ '{book_to_remove}' removed!")
            celebrate()
    else:
        st.warning("📌 No books available to remove.")

# Function to Search for Books
def search_books():
    st.subheader("🔍 Search for a Book")
    search_query = st.text_input("🔎 Enter Book Title or Author")

    if st.button("🔍 Search"):
        results = [book for book in library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        
        if results:
            st.success(f"✅ {len(results)} books found!")
            for book in results:
                st.write(f"📘 **{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("⚠️ No matching books found.")

# Function to Display All Books
def display_books():
    st.subheader("📚 Your Library")
    if library:
        for book in library:
            st.write(f"📖 **{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.warning("📌 No books in the library yet.")

# Function to Display Statistics
def display_stats():
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"✅ **Books Read:** {read_books}")
    st.write(f"📊 **Read Percentage:** {read_percentage:.2f}%")

# Function to Handle File Upload/Download
def file_management():
    global library
    st.subheader("📂 Backup & Restore Library")

    # 📥 Download File
    st.download_button("⬇️ Download Library", data=json.dumps(library, indent=4), file_name="library.json")

    # 📤 Upload File
    uploaded_file = st.file_uploader("📤 Upload Library JSON File", type=["json"])
    if uploaded_file is not None:
        data = json.load(uploaded_file)
        library = data
        save_library()
        st.success("✅ Library uploaded successfully!")

# Streamlit UI
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# Sidebar Menu
st.sidebar.title("📖 Library Manager")
menu = st.sidebar.radio("🔹 Select an Option", ["🏠 Home", "➕ Add Book", "🗑️ Remove Book", "🔍 Search Book", "📚 Display Books", "📊 Statistics", "📂 File Management", "❌ Exit"])

# Display Animation
st.markdown(load_lottie("https://assets4.lottiefiles.com/packages/lf20_hwcqq7xu.json"), unsafe_allow_html=True)

# Render Selected Option
if menu == "🏠 Home":
    st.title("📚 Welcome to Your Library Manager!")
    st.write("Manage your personal book collection with ease! 📖")
    st.image("https://www.publicbooks.org/wp-content/uploads/2021/09/Personal_Library-02.jpg", use_column_width=True)

elif menu == "➕ Add Book":
    add_book()

elif menu == "🗑️ Remove Book":
    remove_book()

elif menu == "🔍 Search Book":
    search_books()

elif menu == "📚 Display Books":
    display_books()

elif menu == "📊 Statistics":
    display_stats()

elif menu == "📂 File Management":
    file_management()

elif menu == "❌ Exit":
    st.warning("👋 Exiting... Library saved!")
    save_library()
    st.stop()
