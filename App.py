

import streamlit as st
import json
import os
import pandas as pd
import datetime
import pytz
from PIL import Image

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

# Get Karachi Time (Pakistan Standard Time)
karachi_tz = pytz.timezone("Asia/Karachi")
current_time = datetime.datetime.now(karachi_tz).strftime("%d-%m-%Y %H:%M:%S")  # Date format: DD-MM-YYYY HH:MM:SS

# Set page config
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# Header Section (Simple & Clean)
st.title("📚 Personal Library Manager")
st.caption(f"**Developed by Abdul Rehman** | 🕒 **Current Time (Karachi):** {current_time}")

# Sidebar menu
menu = st.sidebar.radio("📌 Menu", ["➕ Add Book", "🗑️ Remove Book", "🔍 Search Book", "📚 Display Books", "📊 Statistics", "📥 Import/Export", "🚪 Exit"])

# ✅ **Add a Book with Cover Upload**
if menu == "➕ Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("📖 Book Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Publication Year", min_value=0, step=1)
    genre = st.text_input("📌 Genre")
    read_status = st.checkbox("✅ Read")
    cover = st.file_uploader("📸 Upload Book Cover (optional)", type=["png", "jpg", "jpeg"])

    if st.button("➕ Add Book"):
        if title.strip() == "" or author.strip() == "" or genre.strip() == "":
            st.error("❌ Please fill in all required fields (Title, Author, Genre).")
        else:
            book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status, "cover": ""}
            if cover:
                covers_dir = "covers"
                if not os.path.exists(covers_dir):
                    os.makedirs(covers_dir)
                cover_path = os.path.join(covers_dir, f"{title.replace(' ', '_')}.jpg")
                with open(cover_path, "wb") as f:
                    f.write(cover.getbuffer())
                book["cover"] = cover_path

            st.session_state.library.append(book)
            save_library(st.session_state.library)
            st.success(f'📘 Book "{title}" added successfully!')

# ✅ **Remove a Book**
elif menu == "🗑️ Remove Book":
    st.subheader("🗑️ Remove a Book")
    titles = [book["title"] for book in st.session_state.library]
    title_to_remove = st.selectbox("🗃️ Select a book to remove", titles) if titles else None

    if title_to_remove and st.button("🗑️ Remove Book"):
        st.session_state.library = [book for book in st.session_state.library if book["title"] != title_to_remove]
        save_library(st.session_state.library)
        st.success(f'🚮 Book "{title_to_remove}" removed!')

# ✅ **Search for Books**
elif menu == "🔍 Search Book":
    st.subheader("🔍 Search for a Book")
    search_criteria = st.radio("🔎 Search by:", ["Title", "Author", "Year", "Genre", "Read/Unread"])

    query = st.text_input(f"Enter {search_criteria} to search") if search_criteria != "Read/Unread" else None

    if search_criteria == "Read/Unread":
        read_status = st.radio("✅ Read Status", ["Read", "Unread"])
        results = [book for book in st.session_state.library if (read_status == "Read" and book["read"]) or (read_status == "Unread" and not book["read"])]
    else:
        results = [book for book in st.session_state.library if query and query.lower() in str(book[search_criteria.lower()]).lower()]

    if results:
        for book in results:
            st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')
    else:
        st.warning("⚠️ No books found.")

# ✅ **Display Books with Sorting & Filtering**
elif menu == "📚 Display Books":
    st.subheader("📚 Library Collection")
    if not st.session_state.library:
        st.info("📭 No books available.")
    else:
        filter_genre = st.selectbox("📌 Filter by Genre", ["All"] + list(set(book["genre"] for book in st.session_state.library)))
        filter_read = st.radio("✅ Filter by Read Status", ["All", "Read", "Unread"])
        sort_by = st.radio("🔽 Sort By", ["Title", "Author", "Year"])

        filtered_books = st.session_state.library
        if filter_genre != "All":
            filtered_books = [book for book in filtered_books if book["genre"] == filter_genre]
        if filter_read == "Read":
            filtered_books = [book for book in filtered_books if book["read"]]
        elif filter_read == "Unread":
            filtered_books = [book for book in filtered_books if not book["read"]]

        filtered_books.sort(key=lambda x: x[sort_by.lower()])

        for book in filtered_books:
            col1, col2 = st.columns([0.2, 0.8])
            with col1:
                if book["cover"]:
                    st.image(book["cover"], width=100)
            with col2:
                st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')

# ✅ **Library Statistics with Charts**
elif menu == "📊 Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book["read"])
    unread_books = total_books - read_books

    st.write(f"📚 **Total Books:** {total_books}")
    st.write(f"✅ **Books Read:** {read_books} ({(read_books / total_books * 100) if total_books > 0 else 0:.2f}%)")
    st.write(f"📖 **Books Unread:** {unread_books}")

    if total_books > 0:
        data = pd.DataFrame({"Status": ["Read", "Unread"], "Count": [read_books, unread_books]})
        st.bar_chart(data.set_index("Status"))

# ✅ **Import/Export Library**
elif menu == "📥 Import/Export":
    st.subheader("📥 Import / 📤 Export Library Data")
    if st.button("Export JSON"):
        with open("library_export.json", "w") as f:
            json.dump(st.session_state.library, f, indent=4)
        st.success("📂 Library exported as JSON!")

    uploaded_file = st.file_uploader("📥 Import JSON File", type=["json"])
    if uploaded_file:
        imported_data = json.load(uploaded_file)
        st.session_state.library.extend(imported_data)
        save_library(st.session_state.library)
        st.success("📂 Library imported successfully!")

# ✅ **Exit**
elif menu == "🚪 Exit":
    st.markdown("👋 Thank you for using the Library Manager! You can close this tab.")































# # import streamlit as st
# # import json
# # import os
# # import pandas as pd
# # import datetime
# # import pytz
# # from PIL import Image

# # LIBRARY_FILE = "library.json"

# # # Load library from file
# # def load_library():
# #     if os.path.exists(LIBRARY_FILE):
# #         with open(LIBRARY_FILE, "r") as file:
# #             return json.load(file)
# #     return []

# # # Save library to file
# # def save_library(library):
# #     with open(LIBRARY_FILE, "w") as file:
# #         json.dump(library, file, indent=4)

# # # Initialize session state
# # if "library" not in st.session_state:
# #     st.session_state.library = load_library()

# # # Get Karachi Time (Pakistan Standard Time)
# # karachi_tz = pytz.timezone("Asia/Karachi")
# # current_time = datetime.datetime.now(karachi_tz).strftime("%d-%m-%Y %H:%M:%S")  # Date format: DD-MM-YYYY HH:MM:SS

# # # Set page config
# # st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# # # Header Section
# # st.markdown(f"""
# #     <div style="text-align: center; padding: 10px; background-color: #f1f1f1;">
# #         <h1>📚 Personal Library Manager</h1>
# #         <p><strong>Developed by Abdul Rehman</strong></p>
# #         <p>Current Time (Karachi): {current_time}</p>
# #     </div>
# # """, unsafe_allow_html=True)

# # # Main Menu Prompt (based on user choice input)
# # st.subheader("Welcome to your Personal Library Manager! Please choose an option below:")

# # menu = st.selectbox("Enter your choice:", [
# #     "1. ➕ Add a Book", 
# #     "2. 🗑️ Remove a Book", 
# #     "3. 🔍 Search for a Book", 
# #     "4. 📚 Display All Books", 
# #     "5. 📊 Display Statistics", 
# #     "6. 📥📤 Import/Export", 
# #     "7. ❌ Exit"
# # ])

# # # Action based on the user's choice
# # if menu == "1. ➕ Add a Book":
# #     st.subheader("➕ Add a New Book")
# #     title = st.text_input("Book Title")
# #     author = st.text_input("Author")
# #     year = st.number_input("Publication Year", min_value=0, step=1)
# #     genre = st.text_input("Genre")
# #     read_status = st.checkbox("Read")
# #     cover = st.file_uploader("Upload Book Cover (optional)", type=["png", "jpg", "jpeg"])

# #     if st.button("Add Book"):
# #         # Validate all required fields (Title, Author, and Genre)
# #         if title.strip() == "" or author.strip() == "" or genre.strip() == "":
# #             st.error("Please fill in all fields (Title, Author, and Genre are required).")
# #         else:
# #             # Proceed if all fields are filled
# #             book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status, "cover": ""}

# #             # If a cover image is provided, save it
# #             if cover:
# #                 covers_dir = "covers"
# #                 if not os.path.exists(covers_dir):
# #                     os.makedirs(covers_dir)
                
# #                 cover_path = os.path.join(covers_dir, f"{title.replace(' ', '_')}.jpg")
# #                 with open(cover_path, "wb") as f:
# #                     f.write(cover.getbuffer())
# #                 book["cover"] = cover_path

# #             # Append the book to the library and save it
# #             st.session_state.library.append(book)
# #             save_library(st.session_state.library)
# #             st.success(f'📖 Book "{title}" added successfully!')

# # elif menu == "2. 🗑️ Remove a Book":
# #     st.subheader("🗑️ Remove a Book")
# #     titles = [book["title"] for book in st.session_state.library]
# #     title_to_remove = st.selectbox("Select a book to remove", titles) if titles else None

# #     if title_to_remove and st.button("Remove Book"):
# #         st.session_state.library = [book for book in st.session_state.library if book["title"] != title_to_remove]
# #         save_library(st.session_state.library)
# #         st.success(f'🚮 Book "{title_to_remove}" removed!')

# # elif menu == "3. 🔍 Search for a Book":
# #     st.subheader("🔍 Search for a Book")
    
# #     # Search by Title, Author, Publication Year, Genre, Read/Unread
# #     search_criteria = st.radio("Search by:", ["Title", "Author", "Year", "Genre", "Read/Unread", "Cover Image"])
    
# #     query = ""
# #     if search_criteria != "Cover Image":
# #         query = st.text_input(f"Enter {search_criteria} to search")

# #     # Handle search by title
# #     if search_criteria == "Title" and query:
# #         results = [book for book in st.session_state.library if query.lower() in book["title"].lower()]
# #         if results:
# #             for book in results:
# #                 st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')
# #         else:
# #             st.warning("No books found.")

# #     # Handle search by author
# #     elif search_criteria == "Author" and query:
# #         results = [book for book in st.session_state.library if query.lower() in book["author"].lower()]
# #         if results:
# #             for book in results:
# #                 st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')
# #         else:
# #             st.warning("No books found.")

# #     # Handle search by year
# #     elif search_criteria == "Year" and query:
# #         try:
# #             year_query = int(query)
# #             results = [book for book in st.session_state.library if book["year"] == year_query]
# #             if results:
# #                 for book in results:
# #                     st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')
# #             else:
# #                 st.warning("No books found.")
# #         except ValueError:
# #             st.error("Please enter a valid year.")

# #     # Handle search by genre
# #     elif search_criteria == "Genre" and query:
# #         results = [book for book in st.session_state.library if query.lower() in book["genre"].lower()]
# #         if results:
# #             for book in results:
# #                 st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')
# #         else:
# #             st.warning("No books found.")

# #     # Handle search by read/unread
# #     elif search_criteria == "Read/Unread":
# #         read_status = st.radio("Choose status:", ["Read", "Unread"])
# #         results = [book for book in st.session_state.library if (read_status == "Read" and book["read"]) or (read_status == "Unread" and not book["read"])]
# #         if results:
# #             for book in results:
# #                 st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')
# #         else:
# #             st.warning("No books found.")

# #     # Handle search by cover image
# #     elif search_criteria == "Cover Image":
# #         uploaded_image = st.file_uploader("Upload a book cover image to search", type=["png", "jpg", "jpeg"])

# #         if uploaded_image:
# #             uploaded_image = Image.open(uploaded_image)
# #             results = []
# #             for book in st.session_state.library:
# #                 if book["cover"]:
# #                     stored_image = Image.open(book["cover"])
# #                     if list(stored_image.getdata()) == list(uploaded_image.getdata()):  # Simple comparison
# #                         results.append(book)

# #             if results:
# #                 for book in results:
# #                     st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')
# #             else:
# #                 st.warning("No books found with the matching cover image.")

# # elif menu == "4. 📚 Display All Books":
# #     st.subheader("📚 All Books in Library")
    
# #     if not st.session_state.library:
# #         st.info("No books available.")
# #     else:
# #         # Prepare book data for table display
# #         books_data = []
# #         for book in st.session_state.library:
# #             cover_image = ""
# #             if book["cover"]:
# #                 cover_image = Image.open(book["cover"])
# #                 cover_image = cover_image.resize((50, 50))  # Resize for display purposes
            
# #             books_data.append({
# #                 "Title": book["title"],
# #                 "Author": book["author"],
# #                 "Year": book["year"],
# #                 "Genre": book["genre"],
# #                 "Read": "✅" if book["read"] else "📖",
# #                 "Cover": cover_image
# #             })
        
# #         # Display books data in a table
# #         df = pd.DataFrame(books_data)
# #         st.dataframe(df)

# # elif menu == "5. 📊 Display Statistics":
# #     st.subheader("📊 Display Statistics")
# #     total_books = len(st.session_state.library)
# #     read_books = sum(1 for book in st.session_state.library if book["read"])
# #     unread_books = total_books - read_books
# #     genres = set(book["genre"] for book in st.session_state.library)
    
# #     st.write(f"**Total Books:** {total_books}")
# #     st.write(f"**Read Books:** {read_books}")
# #     st.write(f"**Unread Books:** {unread_books}")
# #     st.write(f"**Genres:** {', '.join(genres)}")

# # elif menu == "6. 📥📤 Import/Export":
# #     st.subheader("📥📤 Import/Export Library")
# #     st.write("Coming soon! Feature for importing/exporting data.")

# # elif menu == "7. ❌ Exit":
# #     st.write("Goodbye! 👋")
# #     st.stop()



























# import streamlit as st
# import json
# import os
# import pandas as pd
# import datetime
# import pytz
# from PIL import Image
# import io

# # Attempt to import matplotlib for plotting, handle import errors
# try:
#     import matplotlib.pyplot as plt
# except ImportError:
#     st.error("Matplotlib is required for generating charts. Please install it by running `pip install matplotlib`.")
#     plt = None

# # Set page config FIRST to avoid StreamlitSetPageConfigMustBeFirstCommandError
# st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# LIBRARY_FILE = "library.json"

# # Load library from file
# def load_library():
#     if os.path.exists(LIBRARY_FILE):
#         with open(LIBRARY_FILE, "r") as file:
#             return json.load(file)
#     return []

# # Save library to file
# def save_library(library):
#     with open(LIBRARY_FILE, "w") as file:
#         json.dump(library, file, indent=4)

# # Initialize session state
# if "library" not in st.session_state:
#     st.session_state.library = load_library()

# # Get Karachi Time (Pakistan Standard Time)
# karachi_tz = pytz.timezone("Asia/Karachi")
# current_time = datetime.datetime.now(karachi_tz).strftime("%d-%m-%Y %H:%M:%S")  # Date format: DD-MM-YYYY HH:MM:SS

# # Header Section
# st.markdown(f"""
#     <div style="text-align: center; padding: 10px; background-color: #f1f1f1;">
#         <h1>📚 Personal Library Manager</h1>
#         <p><strong>Developed by Abdul Rehman</strong></p>
#         <p>Current Time (Karachi): {current_time}</p>
#     </div>
# """, unsafe_allow_html=True)

# # Sidebar menu with an exit option
# menu = st.sidebar.radio("Menu", ["Add Book", "Remove Book", "Search Book", "Display Books", "Statistics", "Import/Export", "Exit"])

# # ✅ **Library Statistics with Enhanced Charts**
# if menu == "Statistics":
#     st.subheader("📊 Library Statistics")
    
#     # Total books and read/unread count
#     total_books = len(st.session_state.library)
#     read_books = sum(1 for book in st.session_state.library if book["read"])
#     unread_books = total_books - read_books
#     read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    
#     # Display basic statistics
#     st.write(f"📚 **Total Books:** {total_books}")
#     st.write(f"✅ **Books Read:** {read_books} ({read_percentage:.2f}%)")
#     st.write(f"📖 **Books Unread:** {unread_books}")
    
#     # Pie Chart for Read vs Unread
#     if total_books > 0 and plt:
#         read_unread_data = pd.DataFrame({
#             "Status": ["Read", "Unread"],
#             "Count": [read_books, unread_books]
#         })
        
#         fig, ax = plt.subplots()
#         ax.pie(read_unread_data["Count"], labels=read_unread_data["Status"], autopct='%1.1f%%', startangle=90, colors=["#4CAF50", "#F44336"])
#         ax.axis('equal')
#         st.pyplot(fig)

#     # Bar Chart for Books per Genre
#     genre_counts = pd.Series([book["genre"] for book in st.session_state.library]).value_counts()
#     if not genre_counts.empty:
#         st.write("### 📊 Books per Genre")
#         st.bar_chart(genre_counts)

#     # Average Publication Year and Yearly Distribution
#     years = [book["year"] for book in st.session_state.library]
#     if years:
#         avg_year = sum(years) / len(years)
#         st.write(f"### 🗓️ **Average Publication Year:** {avg_year:.2f}")
        
#         year_counts = pd.Series(years).value_counts().sort_index()
#         st.write("### 📆 Books Published Each Year")
#         st.bar_chart(year_counts)

#     # Download CSV/JSON
#     st.write("### 📥 Export Statistics")
#     csv_data = read_unread_data.to_csv(index=False)
#     json_data = read_unread_data.to_json(orient="records", lines=True)

#     st.download_button("Download as CSV", csv_data, file_name="library_statistics.csv", mime="text/csv")
#     st.download_button("Download as JSON", json_data, file_name="library_statistics.json", mime="application/json")

# # ✅ **Add a Book with Cover Upload**
# if menu == "Add Book":
#     st.subheader("➕ Add a New Book")
#     title = st.text_input("Book Title")
#     author = st.text_input("Author")
#     year = st.number_input("Publication Year", min_value=0, step=1)
#     genre = st.text_input("Genre")
#     read_status = st.checkbox("Read")
#     cover = st.file_uploader("Upload Book Cover (optional)", type=["png", "jpg", "jpeg"])

#     if st.button("Add Book"):
#         # Validate all required fields (Title, Author, and Genre)
#         if title.strip() == "" or author.strip() == "" or genre.strip() == "":
#             st.error("Please fill in all fields (Title, Author, and Genre are required).")
#         else:
#             # Proceed if all fields are filled
#             book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read_status, "cover": ""}

#             # If a cover image is provided, save it
#             if cover:
#                 covers_dir = "covers"
#                 if not os.path.exists(covers_dir):
#                     os.makedirs(covers_dir)
                
#                 cover_path = os.path.join(covers_dir, f"{title.replace(' ', '_')}.jpg")
#                 with open(cover_path, "wb") as f:
#                     f.write(cover.getbuffer())
#                 book["cover"] = cover_path

#             # Append the book to the library and save it
#             st.session_state.library.append(book)
#             save_library(st.session_state.library)
#             st.success(f'📖 Book "{title}" added successfully!')

# # ✅ **Remove a Book**
# elif menu == "Remove Book":
#     st.subheader("🗑️ Remove a Book")
#     titles = [book["title"] for book in st.session_state.library]
#     title_to_remove = st.selectbox("Select a book to remove", titles) if titles else None

#     if title_to_remove and st.button("Remove Book"):
#         st.session_state.library = [book for book in st.session_state.library if book["title"] != title_to_remove]
#         save_library(st.session_state.library)
#         st.success(f'🚮 Book "{title_to_remove}" removed!')

# # ✅ **Search for Books**
# elif menu == "Search Book":
#     st.subheader("🔍 Search for a Book")
    
#     # Search by Title, Author, Publication Year, Genre, Read/Unread
#     search_criteria = st.radio("Search by:", ["Title", "Author", "Year", "Genre", "Read/Unread", "Cover Image"])
    
#     query = ""
#     if search_criteria != "Cover Image":
#         query = st.text_input(f"Enter {search_criteria} to search")

#     # Handle search logic based on criteria...
#     # (As already implemented in your code)

# # ✅ **Display Books**
# elif menu == "Display Books":
#     st.subheader("📚 All Books in Library")
#     if not st.session_state.library:
#         st.info("No books available.")
#     else:
#         filter_genre = st.selectbox("Filter by Genre", ["All"] + list(set(book["genre"] for book in st.session_state.library)))
#         filter_read = st.radio("Filter by Read Status", ["All", "Read", "Unread"])
#         sort_by = st.radio("Sort By", ["Title", "Author", "Year"])

#         filtered_books = st.session_state.library
#         if filter_genre != "All":
#             filtered_books = [book for book in filtered_books if book["genre"] == filter_genre]
#         if filter_read == "Read":
#             filtered_books = [book for book in filtered_books if book["read"]]
#         elif filter_read == "Unread":
#             filtered_books = [book for book in filtered_books if not book["read"]]

#         if sort_by == "Title":
#             filtered_books.sort(key=lambda x: x["title"])
#         elif sort_by == "Author":
#             filtered_books.sort(key=lambda x: x["author"])
#         elif sort_by == "Year":
#             filtered_books.sort(key=lambda x: x["year"], reverse=True)

#         for book in filtered_books:
#             col1, col2 = st.columns([0.2, 0.8])
#             with col1:
#                 if book["cover"]:
#                     st.image(book["cover"], width=100)
#             with col2:
#                 st.write(f'📘 **{book["title"]}** - {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "📖 Unread"}')

# # ✅ **Import/Export Library**
# elif menu == "Import/Export":
#     st.subheader("📥 Import / 📤 Export Library Data")
#     # (Import/Export code as previously)

# # ✅ **Exit Option**
# elif menu == "Exit":
#     st.markdown("You have exited the app. Thank you for using the Library Manager! You can close this tab.")






