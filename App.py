import streamlit as st
import json
import os
import pandas as pd
import requests
import time

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
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except:
        return None
    return None

# Load Lottie Animations (Using JSON Directly)
lottie_add = load_lottie_url("https://lottie.host/85c5de04-0f66-442e-970c-0291b4967d1e/9kGmNp6QIA.json")
lottie_books = load_lottie_url("https://lottie.host/997df92b-39b5-4d42-97ba-fc83d232a73b/dmWvTTRSAy.json")

# 🎉 Welcome Message with Animations
st.markdown("<h1 style='text-align: center;'>📚 Personal Library Manager</h1>", unsafe_allow_html=True)

st.sidebar.title("📌 Menu")
menu = st.sidebar.radio("", ["➕ Add Book", "❌ Remove Book", "🔍 Search Book", "📚 Display Books", "📊 Statistics"])

# ✅ **Add a Book**
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
            st.success(f'📖 Book "{title}" added successfully!')
            st.balloons()  # 🎈 Celebration Effect
            time.sleep(1)
            st.snow()  # ❄️ Snow Effect
        else:
            st.error("⚠️ Please fill in all fields.")

    if lottie_add:
        st.write("📌 Here's a cool animation for adding books:")
        st.json(lottie_add)

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
        st.write("📚 Enjoy a cool animation:")
        st.json(lottie_books)

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
