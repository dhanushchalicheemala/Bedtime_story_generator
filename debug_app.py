import streamlit as st
import sys

# Enable verbose output
st.set_option('server.enableCORS', False)
st.set_option('server.enableWebsocketCompression', False)

# Print environment info
st.write(f"Python version: {sys.version}")
st.write(f"Streamlit version: {st.__version__}")

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Debug DreamTales",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Page header
st.markdown("<h1 style='text-align: center;'>✨ DreamTales Debug ✨</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Troubleshooting Page</h3>", unsafe_allow_html=True)

# Create a simple form
st.markdown("### Basic Form Test")
child_name = st.text_input("Child's Name", placeholder="Enter your child's name")
selected_topic = st.selectbox("Choose a story topic:", ["Space Adventure", "Underwater Journey"])
story_length = st.select_slider("Story Length", options=["Short", "Medium"], value="Short")

# Test button
if st.button("Test Button"):
    st.success("Button clicked successfully!")
    
# Show session state
st.markdown("### Session State")
st.write(st.session_state)

# Footer
st.markdown("<div style='text-align: center; margin-top: 30px;'>Debug Page</div>", unsafe_allow_html=True)
