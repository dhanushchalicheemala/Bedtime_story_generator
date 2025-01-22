import streamlit as st
from story_generator import generate_story_and_image

# 🎨 Set Streamlit Page Configuration
st.set_page_config(page_title="Cozy Story Time 🛏️📖", layout="centered")

# 📖 Web App Title
st.title("🌙 Cozy Story Time 🛏️📖")

# 📝 Description
st.write("Enter a simple story idea, and this will generate a **gentle Bedtime Story** with a **beautiful illustration and voice narration**.")

# 📌 Set a Usage Limit (Max 2 Stories per Session)
if "story_count" not in st.session_state:
    st.session_state.story_count = 0

MAX_STORIES = 2

# 📌 User Inputs
story_topic = st.text_input("✨ Enter a Bedtime Story Topic:", "A little bunny who can't sleep")
story_length = st.selectbox("🕒 Choose story length:", ["Short", "Medium"], help="Short: 2-3 minutes | Medium: 5-7 minutes")

# 🎬 Generate Story Button
if st.button("Generate Story, Image & Narration"):
    if st.session_state.story_count < MAX_STORIES:
        if story_topic.strip():
            st.info("🪄 Creating your Bedtime Story... Please wait ⏳")

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
            st.subheader("📖 Your AI-Generated Bedtime Story")
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

# 🎨 Footer
st.markdown("---")
st.markdown("✨ Created with ❤️ using OpenAI & Streamlit ✨")
