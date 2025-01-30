import streamlit as st
from story_generator import generate_story_and_image
import time

# 🎨 Set Streamlit Page Configuration
st.set_page_config(page_title="Cozy Story Time 🛏️📖", layout="centered")

# 📌 Token System Implementation
TOKEN_RESET_TIME = 8 * 60 * 60  # 8 hours in seconds
MAX_TOKENS = 2  # Allowed story generations

# Initialize session state for tokens and generated content
if "tokens" not in st.session_state:
    st.session_state.tokens = MAX_TOKENS
    st.session_state.token_timestamp = time.time()
    st.session_state.generated_story = None
    st.session_state.generated_image = None
    st.session_state.generated_audio = None
    st.session_state.generated_pdf = None
    st.session_state.loading = False  # Track loading state

# Function to reset tokens after the set time period
def reset_tokens():
    elapsed_time = time.time() - st.session_state.token_timestamp
    if elapsed_time > TOKEN_RESET_TIME:
        st.session_state.tokens = MAX_TOKENS
        st.session_state.token_timestamp = time.time()

# Reset tokens if needed
reset_tokens()

# 📖 Web App Title
st.title("🌙 Cozy Story Time 🛏️📖")

# 📝 Description
st.write("Enter a simple story idea, and this will generate a **gentle Bedtime Story** with a **beautiful illustration and voice narration**.")

# 📌 User Inputs
story_topic = st.text_input("✨ Enter a Bedtime Story Topic:", "A little bunny who can't sleep")
story_length = st.selectbox("🕒 Choose story length:", ["Short", "Medium"], help="Short: 2-3 minutes | Medium: 5-7 minutes")

# 🎬 Generate Story Button with Token Counter
col1, col2 = st.columns([3, 1])
with col1:
    generate_button = st.button("🎬 Generate Story", key="generate_btn")
with col2:
    st.markdown(
        f"""
        <div style="text-align:center; padding:6px; font-size:16px; font-weight:bold; color:#F4A261; border:2px solid #F4A261; border-radius:10px;">
            🪙 {MAX_TOKENS - st.session_state.tokens}/{MAX_TOKENS} Stories Used
        </div>
        """,
        unsafe_allow_html=True
    )

# 🎬 Generate Story Action
if generate_button:
    if st.session_state.tokens > 0:
        if story_topic.strip():
            st.session_state.loading = True  # Start loading state
            st.experimental_rerun()  # Force UI update

            # Display loading message
            with st.spinner("🪄 Creating your Bedtime Story... Please wait ⏳"):
                result = generate_story_and_image(story_topic, story_length)

            # Store generated content
            st.session_state.generated_story = result["story"]
            st.session_state.generated_image = result["image"]
            st.session_state.generated_audio = result["audio"]
            st.session_state.generated_pdf = result["pdf"]

            # Deduct a Token
            st.session_state.tokens -= 1
            st.session_state.loading = False  # Stop loading state
            st.experimental_rerun()  # Refresh UI
        else:
            st.warning("⚠️ Please enter a valid story topic.")
    else:
        st.error("🚫 You have reached the **maximum limit of 2 stories**. Please wait **8 hours** for token refresh.")

# 🎨 Display Story, Image, Audio, and PDF if available
if not st.session_state.loading and st.session_state.generated_story:
    st.subheader("🎨 Illustration for Your Story")
    st.image(st.session_state.generated_image, caption="A cozy bedtime scene", use_container_width=True)

    st.subheader("🔊 Listen to the Story")
    with open(st.session_state.generated_audio, "rb") as audio_file:
        st.audio(audio_file, format="audio/mp3")

    st.subheader("📖 Your Generated Bedtime Story")
    st.write(st.session_state.generated_story)

    st.subheader("📄 Download Story")
    with open(st.session_state.generated_pdf, "rb") as pdf_file:
        st.download_button(
            label="📥 Download as PDF",
            data=pdf_file,
            file_name=f"{story_topic}.pdf",
            mime="application/pdf"
        )

# 🎨 Footer
st.markdown("---")
st.markdown("✨ Created with ❤️ using OpenAI & Streamlit ✨")