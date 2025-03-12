import streamlit as st
import json
import pandas as pd
import sys  # To exit the app

# Initialize session state for the library
if "library" not in st.session_state:
    st.session_state.library = []

# Function to save library data
def save_library():
    with open("library.json", "w") as f:
        json.dump(st.session_state.library, f, indent=4)

# Sidebar Menu
menu = st.sidebar.selectbox("📌 Menu", [
    "🏠 Home", "📖 Add Book", "🗑️ Remove Book", "🔍 Search Book",
    "📚 Display Books", "📊 Statistics", "📥 Import/Export", "🚪 Exit"
])

# ✅ **Home Page**
if menu == "🏠 Home":
    st.title("📖 Library Manager App")
    st.subheader("📌 Organize, Track, and Manage Your Books with Ease!")

    # About the App
    st.markdown("""
    <div style="background-color: #f0f0f0; border-radius: 10px; padding: 20px; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h4 style="color: #2c3e50;">📌 About the App</h4>
        <p style="color: #34495e; font-size: 16px;">
            The <b>Library Manager App</b> helps you manage your book collection efficiently.
            You can <b>add, track, and organize books</b>, see statistics, and <b>import/export</b> your library.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ✅ **Add a New Book**
elif menu == "📖 Add Book":
    st.subheader("📖 Add a New Book")
    
    title = st.text_input("📌 Book Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Year", min_value=0, step=1)
    genre = st.text_input("🎭 Genre")
    read = st.checkbox("✔️ Mark as Read")

    if st.button("➕ Add Book"):
        new_book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read}
        st.session_state.library.append(new_book)
        save_library()
        st.success(f"✅ '{title}' added successfully!")

# ✅ **Remove a Book**
elif menu == "🗑️ Remove Book":
    st.subheader("🗑️ Remove a Book")
    
    if not st.session_state.library:
        st.info("No books available to remove!")
    else:
        book_titles = [book["title"] for book in st.session_state.library]
        book_to_remove = st.selectbox("📌 Select Book to Remove", book_titles)

        if st.button("🗑️ Remove"):
            st.session_state.library = [book for book in st.session_state.library if book["title"] != book_to_remove]
            save_library()
            st.success(f"❌ '{book_to_remove}' removed successfully!")

# ✅ **Search for a Book**
elif menu == "🔍 Search Book":
    st.subheader("🔍 Search for a Book")
    
    search_query = st.text_input("🔎 Enter Book Title or Author")
    
    if search_query:
        results = [book for book in st.session_state.library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        
        if results:
            for book in results:
                st.markdown(f"""
                <div style="background-color: #f0f0f0; border-radius: 10px; padding: 20px; 
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
                    <h4 style="color: #2c3e50;">{book["title"]}</h4>
                    <p style="color: #34495e; font-size: 16px;">{book["author"]}</p>
                    <p style="color: #7f8c8d;">{book["year"]} | {book["genre"]}</p>
                    <p style="color: #16a085;">{"✔️ Read" if book["read"] else "📖 Unread"}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matching books found!")

# ✅ **Display Books**
elif menu == "📚 Display Books":
    st.subheader("📚 Your Library Collection")
    
    if not st.session_state.library:
        st.info("No books found!")
    else:
        for book in st.session_state.library:
            st.markdown(f"""
            <div style="background-color: #f0f0f0; border-radius: 10px; padding: 20px; 
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
                <h4 style="color: #2c3e50;">{book["title"]}</h4>
                <p style="color: #34495e; font-size: 16px;">{book["author"]}</p>
                <p style="color: #7f8c8d;">{book["year"]} | {book["genre"]}</p>
                <p style="color: #16a085;">{"✔️ Read" if book["read"] else "📖 Unread"}</p>
            </div>
            """, unsafe_allow_html=True)

# ✅ **Statistics**
elif menu == "📊 Statistics":
    st.subheader("📊 Library Statistics")

    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read"])
    unread_books = total_books - read_books

    genres = [book["genre"] for book in st.session_state.library]
    most_common_genre = pd.Series(genres).mode()[0] if genres else "N/A"

    authors = [book["author"] for book in st.session_state.library if book["read"]]
    most_read_author = pd.Series(authors).mode()[0] if authors else "N/A"

    st.markdown(f"📚 **Total Books:** {total_books}")
    st.markdown(f"✔️ **Books Read:** {read_books} ({(read_books/total_books*100) if total_books > 0 else 0:.2f}%)")
    st.markdown(f"📖 **Books Unread:** {unread_books}")
    st.markdown(f"🎭 **Most Common Genre:** {most_common_genre}")
    st.markdown(f"🌟 **Most Read Author:** {most_read_author}")

# ✅ **Import/Export**
elif menu == "📥 Import/Export":
    st.subheader("📥 Import / 📤 Export Library Data")

    if st.button("📤 Export as JSON"):
        with open("library_export.json", "w") as f:
            json.dump(st.session_state.library, f, indent=4)
        st.success("📂 Exported as JSON!")

    uploaded_file = st.file_uploader("📥 Import JSON File", type=["json"])
    if uploaded_file:
        st.session_state.library.extend(json.load(uploaded_file))
        save_library()
        st.success("✅ Library imported successfully!")

# ✅ **Exit**
elif menu == "🚪 Exit":
    st.markdown("📌 **You have exited the app. Thank you for using the Library Manager!**")
    st.stop()
