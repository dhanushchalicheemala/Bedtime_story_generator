import streamlit as st
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from story_generator import generate_story_and_image

# 🎨 Set Streamlit Page Configuration
st.set_page_config(page_title="Cozy Story Time 🛏️📖", layout="centered")

# 📖 Web App Title
st.title("🌙 Cozy Story Time 🛏️📖")

# 📝 Description
st.write("Enter a simple story idea, and this will generate a **gentle Bedtime Story** with a **beautiful illustration and voice narration**.")

# 📌 Token System Implementation
TOKEN_RESET_TIME = 8 * 60 * 60  # 8 hours in seconds
MAX_TOKENS = 4  # Number of allowed story generations

# Initialize session state for tokens
if "tokens" not in st.session_state:
    st.session_state.tokens = MAX_TOKENS
    st.session_state.token_timestamp = time.time()
    st.session_state.story_cache = {}  # Cache to store generated stories

# Function to reset tokens after the set time period
def reset_tokens():
    elapsed_time = time.time() - st.session_state.token_timestamp
    if elapsed_time > TOKEN_RESET_TIME:
        st.session_state.tokens = MAX_TOKENS
        st.session_state.token_timestamp = time.time()

# Reset tokens if the time has passed
reset_tokens()

# 📌 User Inputs
story_topic = st.text_input("✨ Enter a Bedtime Story Topic:", "A little bunny who can't sleep")
story_length = st.selectbox("🕒 Choose story length:", ["Short", "Medium"], help="Short: 2-3 minutes | Medium: 5-7 minutes")

# 📊 Show Token Usage
st.markdown(f"🪙 **{MAX_TOKENS - st.session_state.tokens}/{MAX_TOKENS} Stories Used**", unsafe_allow_html=True)

# 🎬 Generate Story Button
if st.button("Generate Story"):
    if st.session_state.tokens > 0:
        if story_topic.strip():
            st.info("🪄 Creating your Bedtime Story... Please wait ⏳")

            # Check cache to avoid redundant processing
            if story_topic in st.session_state.story_cache:
                result = st.session_state.story_cache[story_topic]
            else:
                # Use ThreadPoolExecutor to run the story generation asynchronously
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(generate_story_and_image, story_topic, story_length)
                    result = future.result()
                    st.session_state.story_cache[story_topic] = result  # Store in cache

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

            # 🔢 Deduct a Token
            st.session_state.tokens -= 1

        else:
            st.warning("⚠️ Please enter a valid story topic.")
    else:
        st.error("🚫 You have reached the **maximum limit of 4 stories**. Please wait **8 hours** for token refresh.")

# 🎨 Footer
st.markdown("---")
st.markdown("✨ Created with ❤️ using OpenAI & Streamlit ✨")
