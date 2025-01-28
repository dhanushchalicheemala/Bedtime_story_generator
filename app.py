import streamlit as st
import csv
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import sqlite3
import json

from story_generator import generate_story_and_image

# 🎨 Set Streamlit Page Configuration
st.set_page_config(page_title="Cozy Story Time 🛏️📖", layout="centered")

# 📖 Web App Title
st.title("🌙 Cozy Story Time 🛏️📖")

# 📝 Description
st.write("Enter a simple story idea, and this will generate a **gentle bedtime story** with a **beautiful illustration and voice narration**.")

# 📌 Set a Usage Limit (Max 2 Stories per Session)
if "story_count" not in st.session_state:
    st.session_state.story_count = 0

MAX_STORIES = 2

# 📌 User Inputs
story_topic = st.text_input("✨ Enter a bedtime story topic:", "A little bunny who can't sleep")
story_length = st.selectbox("🕒 Choose story length:", ["Short", "Medium"], help="Short: 2-3 minutes | Medium: 5-7 minutes")

# 🎬 Generate Story Button
if st.button("Generate Story"):
    if st.session_state.story_count < MAX_STORIES:
        if story_topic.strip():
            st.info("🪄 Creating your bedtime story... Please wait ⏳")

            # Generate story, image, audio, and PDF
            result = generate_story_and_image(story_topic, story_length)

            # 📸 Display Image First
            st.subheader("🎨 Illustration for Your Story")
            st.image(result["image"], caption="A cozy bedtime scene", use_container_width=True)

            # 🔊 Play Voice Narration
            st.subheader("🔊 Listen to the Story")
            with open(result["audio"], "rb") as audio_file:
                st.audio(audio_file, format="audio/mp3")

            # 📖 Display Story
            st.subheader("📖 Your Generated Bedtime Story")
            st.write(result["story"])

            # 📄 Download Story as PDF
            st.subheader("📄 Download Story")
            with open(result["pdf"], "rb") as pdf_file:
                st.download_button(
                    label="📥 Download as PDF",
                    data=pdf_file,
                    file_name=f"{story_topic}.pdf",
                    mime="application/pdf"
                )

            # 🔢 Increment Story Count
            st.session_state.story_count += 1

        else:
            st.warning("⚠️ Please enter a valid story topic.")
    else:
        st.error("🚫 You have reached the **maximum limit of 2 stories per session**.")

# 📌 Parent Feedback Section
st.markdown("---")
st.subheader("📢 Parent Feedback & Suggestions")

# Google Sheets API Setup
# Load credentials from Streamlit secrets
service_account_info = st.secrets["google_sheets"]
creds = Credentials.from_service_account_info(service_account_info)

# Authenticate with Google Sheets
client = gspread.authorize(creds)

# Open Google Sheet
SHEET_ID = "1kEqFqyHpUKRl4K9WQMku3wgYBkiNE-8d66QhFas0xcU"
SHEET_NAME = "Feedback"
spreadsheet = client.open_by_key(SHEET_ID)
worksheet = spreadsheet.worksheet(SHEET_NAME)

# Database Setup for Analytics
conn = sqlite3.connect("feedback.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        rating INTEGER,
        feedback TEXT
    )
""")
conn.commit()

# Collect user feedback
with st.form("feedback_form"):
    parent_name = st.text_input("👨‍👩‍👧 Your Name (Optional)")
    rating = st.slider("⭐ How would you rate this story?", 1, 5, 5)
    feedback_text = st.text_area("💬 What did you like or what can we improve?")

    submit_feedback = st.form_submit_button("Submit Feedback")

    if submit_feedback:
        if feedback_text.strip():
            # Save feedback to Google Sheets
            worksheet.append_row([parent_name, rating, feedback_text])

            # Save feedback to SQLite database
            c.execute("INSERT INTO feedback (name, rating, feedback) VALUES (?, ?, ?)",
                      (parent_name, rating, feedback_text))
            conn.commit()

            st.success("✅ Thank you for your feedback! 😊")
        else:
            st.warning("⚠️ Please enter feedback before submitting.")

# 📌 Display Recent Feedback
st.subheader("📝 Recent Parent Reviews")

# Load feedback from Google Sheets
feedback_data = worksheet.get_all_records()
if feedback_data:
    df = pd.DataFrame(feedback_data)
    st.dataframe(df.tail(5))  # Show last 5 reviews
else:
    st.info("No feedback submitted yet. Be the first to leave a review! 😊")

# 📊 Parent Feedback Dashboard
st.subheader("📊 Parent Feedback Dashboard")

# Load feedback from SQLite database
df_feedback = pd.read_sql("SELECT * FROM feedback", conn)

if not df_feedback.empty:
    # Display rating distribution
    st.bar_chart(df_feedback["rating"].value_counts())

    # Display latest feedback
    st.write("Recent Feedback:")
    st.table(df_feedback.tail(5))
else:
    st.info("No feedback data available yet.")

# 🎨 Footer
st.markdown("---")
st.markdown("✨ Created with ❤️ using OpenAI & Streamlit ✨")