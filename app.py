import streamlit as st
from story_generator import generate_story_text, generate_story_image, generate_story_audio, generate_story_pdf

# Set Streamlit Page Configuration
st.set_page_config(page_title="Cozy Story Time 🛏️📖", layout="centered")

# App Title
st.title("🌙 Cozy Story Time 🛏️📖")

# Description
st.write("Enter a simple story idea, and this will generate a **gentle Bedtime Story** with a **beautiful illustration and voice narration**.")

# Token-based System
if "story_tokens" not in st.session_state:
    st.session_state.story_tokens = 2  # Max 2 stories per session

# User Inputs
story_topic = st.text_input("✨ Enter a Bedtime Story Topic:", "A little bunny who can't sleep")
story_length = st.selectbox("🕒 Choose story length:", ["Short", "Medium"])

# Show Token Indicator Next to Button
col1, col2 = st.columns([4, 1])
with col1:
    generate_button = st.button("Generate Story")
with col2:
    st.markdown(f"🪙 **{2 - st.session_state.story_tokens}/2 Stories Used**", unsafe_allow_html=True)

# Generate Story
if generate_button:
    if st.session_state.story_tokens > 0:
        if story_topic.strip():
            with st.spinner("🪄 Creating your Bedtime Story... Please wait ⏳"):
                story = generate_story_text(story_topic, story_length)
                image = generate_story_image(story_topic)
                audio = generate_story_audio(story)
                pdf = generate_story_pdf(story, image)

            # Display Story Content
            st.subheader("🎨 Illustration for Your Story")
            st.image(image, caption="A cozy bedtime scene", use_column_width=True)

            st.subheader("🔊 Listen to the Story")
            with open(audio, "rb") as audio_file:
                st.audio(audio_file, format="audio/mp3")

            st.subheader("📖 Your Generated Bedtime Story")
            st.write(story)

            st.subheader("📄 Download Story")
            with open(pdf, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download as PDF",
                    data=pdf_file,
                    file_name=f"{story_topic}.pdf",
                    mime="application/pdf"
                )

            # Deduct Token & Refresh UI
            st.session_state.story_tokens -= 1
            st.experimental_rerun()

        else:
            st.warning("⚠️ Please enter a valid story topic.")
    else:
        st.error("🚫 You have reached the **maximum limit of 2 stories per session**.")