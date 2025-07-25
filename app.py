import streamlit as st
import datetime
import os

# Constants
USERNAME = "admin"
PASSWORD = "1234"
ENTRY_FILE = "diary_entries.txt"

# ---------------------
# Login Function
# ---------------------
def login(username, password):
    return username == USERNAME and password == PASSWORD

# ---------------------
# Diary Entry Functions
# ---------------------
def add_entry(entry_text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ENTRY_FILE, "a") as f:
        f.write(f"[{timestamp}]\n{entry_text}\n{'-'*40}\n")

def view_entries():
    if not os.path.exists(ENTRY_FILE) or os.path.getsize(ENTRY_FILE) == 0:
        return "🚫 No entries found."
    with open(ENTRY_FILE, "r") as f:
        return f.read()

def delete_entries():
    open(ENTRY_FILE, "w").close()

# ---------------------
# Streamlit App
# ---------------------
st.title("📘 Personal Diary App")

# Login form
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials!")
else:
    st.success(f"Welcome, {USERNAME}!")

    # Menu
    menu = st.sidebar.selectbox("Menu", ["Add Entry", "View Entries", "Delete All Entries", "Logout"])

    if menu == "Add Entry":
        st.subheader("📝 Write New Entry")
        entry_text = st.text_area("Write here...")
        if st.button("Save Entry"):
            if entry_text.strip() != "":
                add_entry(entry_text)
                st.success("✅ Entry saved!")
            else:
                st.warning("Entry is empty!")

    elif menu == "View Entries":
        st.subheader("📖 Your Entries")
        st.text(view_entries())

    elif menu == "Delete All Entries":
        if st.button("🗑️ Delete All"):
            delete_entries()
            st.warning("All entries deleted.")

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.experimental_rerun()
