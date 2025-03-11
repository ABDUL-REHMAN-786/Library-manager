import streamlit as st
import json
import os
import pandas as pd
import time
from streamlit_lottie import st_lottie
import requests

# File to store books
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

# Function to Load Lottie Animations
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Load Lottie Animations
lottie_add = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_dun4sc2l.json")
lottie_books = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_0nzuchju.json")

# Typing Effect for Welcome Message
st.markdown("<h1 style='text-align: center;'>📚 Personal Library Manager</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'><span class='typing'>Manage Your Books Easily!</span></h3>", unsafe_allow_html=True)

# CSS for Typing Effect & Snowfall
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

# Sidebar Menu
menu = st.sidebar.radio("📌 Menu", ["➕ Add Book", "❌ Remove Book", "🔍 Search Book", "📚 Display Books", "📊 Statistics"])

# ✅ **Add a Book with Celebration & Animation**
if menu == "➕ Add Book":
    st.subheader("📖 Add a New Book")
    title = st.text_input("📕 Book Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Publication Year", min_value=0, step=1)
    genre = st.text_input("📚 Genre")
    read_status = st.checkbox("✅ Read")

    if st.button("📌 Add Book"):
        if title and author and genre:
            book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status}
            st.session_state.library.append(book)
            save_library(st.session_state.library)

            st.balloons()  # 🎈 Celebration Effect
            st.success(f'📖 Book "{title}" added successfully!')
            time.sleep(2)
            st.snow()  # ❄️ Snow Effect
        else:
            st.error("⚠️ Please fill in all fields.")

    if lottie_add:
        st_lottie(lottie_add, height=200, key="add_animation")

# ✅ **Remove a Book**
elif menu == "❌ Remove Book":
    st.subheader("🚮 Remove a Book")
    titles = [book["title"] for book in st.session_state.library]
    title_to_remove = st.selectbox("📕 Select a book to remove", titles) if titles else None

    if title_to_remove and st.button("🗑️ Remove Book"):
        st.session_state.library = [book for book in st.session_state.library if book["title"] != title_to_remove]
        save_library(st.session_state.library)
        st.success(f'📕 Book "{title_to_remove}" removed successfully!')

# ✅ **Search for a Book**
elif menu == "🔍 Search Book":
    st.subheader("🔎 Search for a Book")
    search_query = st.text_input("📌 Enter title or author name")

    if search_query:
        results = [book for book in st.session_state.library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        if results:
            st.write("📖 **Matching Books:**")
            for book in results:
                st.write(f'📚 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')
        else:
            st.warning("🚫 No matching books found.")

# ✅ **Display Books**
elif menu == "📚 Display Books":
    st.subheader("📚 Your Library Collection")

    if not st.session_state.library:
        st.info("📌 No books available.")
    else:
        df = pd.DataFrame(st.session_state.library)
        st.dataframe(df)

    if lottie_books:
        st_lottie(lottie_books, height=200, key="books_animation")

# ✅ **Library Statistics**
elif menu == "📊 Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read"])
    unread_books = total_books - read_books
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0

    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"✅ **Books Read:** {read_books} ({read_percentage:.2f}%)")
    st.write(f"📖 **Books Unread:** {unread_books}")

    if read_percentage == 100:
        st.success("🎉 Congratulations! You've read all your books!")
        st.balloons()
