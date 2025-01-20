import streamlit as st
from story_generator import generate_story

# Web App Title
st.title("📖 AI Story Generator")

# Description
st.write("Enter a simple idea for a story, and AI will generate a creative 100-word short story for you.")

# User Input: Single Story Idea
story_idea = st.text_area("Enter a brief story idea", "A scientist discovers a portal to another dimension.")

# Generate Story Button
if st.button("Generate Story"):
    if story_idea.strip():  # Ensure the input is not empty
        story = generate_story(story_idea, word_limit=100)
        st.subheader("Generated Story")
        st.write(story)
    else:
        st.warning("Please enter a story idea before generating.")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using OpenAI & Streamlit")