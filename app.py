import streamlit as st
from story_generator import generate_story_and_image

# 🎨 Set Streamlit Page Configuration
st.set_page_config(page_title="Cozy Story Time 🛏️📖", layout="centered")

# 📖 Web App Title
st.title("🌙 Cozy Story Time 🛏️📖")

# 📝 Description
st.write("Enter a simple story idea, and AI will generate a **gentle bedtime story** with a **beautiful illustration**.")

# 📌 User Inputs
story_topic = st.text_input("✨ Enter a bedtime story topic:", "A little bunny who can't sleep")
story_length = st.selectbox("🕒 Choose story length:", ["short", "medium"], help="Short: 2-3 minutes | Medium: 5-7 minutes")

# 🎬 Generate Story Button
if st.button("Generate Story & Image"):
    if story_topic.strip():
        st.info("🪄 Creating your bedtime story... Please wait ⏳")

        # Generate story and image
        result = generate_story_and_image(story_topic, story_length)

        # 📖 Display Story
        st.subheader("📖 Your AI-Generated Bedtime Story")
        st.write(result["story"])

        # 📸 Display Image
        st.subheader("🎨 Illustration for Your Story")
        st.image(result["image"], caption="A cozy bedtime scene", use_column_width=True)

    else:
        st.warning("⚠️ Please enter a valid story topic.")

# 🎨 Footer
st.markdown("---")
st.markdown("✨ Created with ❤️ using OpenAI & Streamlit ✨")
