import streamlit as st
import json
import os
import pandas as pd
import time
from streamlit_lottie import st_lottie
import requests

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

# Add Typing Effect for Welcome Message
st.markdown("<h1 style='text-align: center;'>📚 Personal Library Manager</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'><span class='typing'>Manage Your Books Easily!</span></h3>", unsafe_allow_html=True)

# CSS for Typing Effect
st.markdown(
    """
    <style>
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    .typing {
        display: inline-block;
        border-right: 3px solid;
        white-space: nowrap;
        overflow: hidden;
        animation: typing 3s steps(30, end), blink-caret 0.5s step-end infinite;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to Load Lottie Animations
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Load Animations
lottie_add = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_dun4sc2l.json")
lottie_books = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_0nzuchju.json")

# Snowfall Effect
st.markdown(
    """
    <script>
    function startSnow() {
        let snowflakes = document.createElement("div");
        snowflakes.innerHTML = "❄️❄️❄️❄️❄️";
        snowflakes.style.position = "fixed";
        snowflakes.style.top = "0";
        snowflakes.style.width = "100%";
        snowflakes.style.textAlign = "center";
        snowflakes.style.fontSize = "50px";
        document.body.appendChild(snowflakes);
        setTimeout(() => document.body.removeChild(snowflakes), 5000);
    }
    setInterval(startSnow, 10000);
    </script>
    """,
    unsafe_allow_html=True
)

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Book", "Display Books", "Statistics", "Import/Export"])

# ✅ **Add a Book with Celebration & Animation**
if menu == "Add Book":
    st.subheader("➕ Add a New Book")
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
            
            # 🎉 Celebration Effects
            st.balloons()
            st.success(f'📖 Book "{title}" added successfully!')
            time.sleep(2)
            st.snow()
        else:
            st.error("Please fill in all fields.")

    # Add Lottie Animation
    if lottie_add:
        st_lottie(lottie_add, height=200, key="add_animation")

# ✅ **Remove a Book**
elif menu == "Remove Book":
    st.subheader("🗑️ Remove a Book")
    titles = [book["title"] for book in st.session_state.library]
    title_to_remove = st.selectbox("Select a book to remove", titles) if titles else None

    if title_to_remove and st.button("Remove Book"):
        st.session_state.library = [book for book in st.session_state.library if book["title"] != title_to_remove]
        save_library(st.session_state.library)
        st.success(f'🚮 Book "{title_to_remove}" removed!')

# ✅ **Display Books with Sorting & Filtering**
elif menu == "Display Books":
    st.subheader("📚 All Books in Library")
    
    if not st.session_state.library:
        st.info("No books available.")
    else:
        filter_genre = st.selectbox("Filter by Genre", ["All"] + list(set(book["genre"] for book in st.session_state.library)))
        sort_by = st.radio("Sort By", ["Title", "Author", "Year"])

        filtered_books = st.session_state.library
        if filter_genre != "All":
            filtered_books = [book for book in filtered_books if book["genre"] == filter_genre]

        if sort_by == "Title":
            filtered_books.sort(key=lambda x: x["title"])
        elif sort_by == "Author":
            filtered_books.sort(key=lambda x: x["author"])
        elif sort_by == "Year":
            filtered_books.sort(key=lambda x: x["year"], reverse=True)

        for book in filtered_books:
            st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')

    # Lottie Animation
    if lottie_books:
        st_lottie(lottie_books, height=200, key="books_animation")

# ✅ **Library Statistics**
elif menu == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read"])
    unread_books = total_books - read_books
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"✅ **Books Read:** {read_books} ({read_percentage:.2f}%)")
    st.write(f"📖 **Books Unread:** {unread_books}")

    # Confetti for 100% read books
    if read_percentage == 100:
        st.success("🎉 Congratulations! You've read all your books!")
        st.balloons()
