import streamlit as st
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import base64
from story_generator import generate_story_and_image

# Custom CSS for styling
def local_css():
    st.markdown("""
    <style>
        /* Base styles */
        .main {background-color: #2d2d39;}
        h1 {color: #e4c1f9; font-family: 'Trebuchet MS', sans-serif;}
        h2 {color: #a6e1fa; font-family: 'Trebuchet MS', sans-serif;}
        h3 {color: #a6e1fa; font-family: 'Trebuchet MS', sans-serif;}
        p {color: #edf2f4;}
        label {color: #edf2f4 !important;}
        .story-text {font-family: 'Trebuchet MS', sans-serif; font-size: 18px; line-height: 1.6; color: #ffffff; background-color: rgba(45, 45, 57, 0.8); padding: 15px; border-radius: 8px;}
        
        /* Button styles */
        .stButton>button {background-color: #e4c1f9; color: #2d2d39; font-weight: bold; border-radius: 20px; padding: 10px 25px;}
        .stButton>button:hover {background-color: #d4a6ff;}
        
        /* Container styles */
        .story-container {background-color: #edf2f4; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.3);}
        .story-header {background-color: #6c5b7b; color: white; padding: 15px; border-radius: 10px 10px 0 0; margin-bottom: 20px;}
        
        /* Footer styles */
        .footer {font-size: 12px; color: #a6e1fa; text-align: center; margin-top: 30px;}
        
        /* Input field styles */
        .stTextInput>div>div>input {border-radius: 20px; background-color: #3d3d4d; color: #ffffff;}
        .stSelectbox>div>div>div {border-radius: 20px; background-color: #3d3d4d; color: #ffffff;}
        
        /* Feature boxes */
        .feature-box {background-color: #3d3d4d; padding: 20px; border-radius: 10px; color: #edf2f4;}
        .feature-box h2, .feature-box h3 {color: #e4c1f9;}
        .feature-box ul li {color: #edf2f4;}
    </style>
    """, unsafe_allow_html=True)

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="DreamTales - Personalized Bedtime Stories",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
local_css()

# Token system configuration (hidden from user but still functional)
TOKEN_RESET_TIME = 8 * 60 * 60  # 8 hours in seconds
MAX_TOKENS = 4  # Number of allowed story generations

# Initialize session state variables
if "tokens" not in st.session_state:
    st.session_state.tokens = MAX_TOKENS
    st.session_state.token_timestamp = time.time()
    st.session_state.story_cache = {}  # Cache to store generated stories
    st.session_state.page = "home"  # Track which page we're on
    st.session_state.current_story = None  # Store the current story
    st.session_state.final_story_topic = None  # Store the combined topic and tone

# Function to reset tokens after the set time period
def reset_tokens():
    elapsed_time = time.time() - st.session_state.token_timestamp
    if elapsed_time > TOKEN_RESET_TIME:
        st.session_state.tokens = MAX_TOKENS
        st.session_state.token_timestamp = time.time()

# Reset tokens if the time has passed
reset_tokens()

# Function to generate story and redirect to story page
def generate_and_redirect():
    # Check if we have enough tokens
    if st.session_state.tokens <= 0:
        st.error("🚫 You have reached the maximum limit of stories. Please try again later.")
        return
    
    # Create a unique cache key that includes both the topic and child's name
    cache_key = f"{final_story_topic}_{child_name}"
    
    # Check cache to avoid redundant processing
    if cache_key in st.session_state.story_cache:
        result = st.session_state.story_cache[cache_key]
        # Add a flag to indicate this was from cache
        if "timings" in result:
            result["timings"]["from_cache"] = True
            # Print cached timing data to console for PPT
            print("="*60)
            print("📊 TIMING DATA FOR PPT (CACHED RESULT)")
            print("="*60)
            print(f"Story Topic: {final_story_topic}")
            print(f"Child Name: {child_name}")
            print(f"📝 Story Generation: {result['timings'].get('story_generation', 'N/A')}s")
            print(f"🎨 Image Generation: {result['timings'].get('image_generation', 'N/A')}s")
            print(f"🎵 Audio Generation: {result['timings'].get('audio_generation', 'N/A')}s")
            print(f"📄 PDF Generation: {result['timings'].get('pdf_generation', 'N/A')}s")
            print(f"🚀 Total Generation Time: {result['timings'].get('total_time', 'N/A')}s")
            print(f"Status: ⚡ CACHED (Instant delivery)")
            print("="*60)
    else:
        with st.spinner('Crafting your magical story... 🪄'):
            # Create the thread pool executor
            executor = ThreadPoolExecutor(max_workers=1)
            # Submit the task
            future = executor.submit(generate_story_and_image, final_story_topic, story_length.lower(), child_name)
            result = future.result()
            # Add a flag to indicate this was fresh generation
            if "timings" in result:
                result["timings"]["from_cache"] = False
                # Print fresh timing data to console for PPT
                print("="*60)
                print("📊 TIMING DATA FOR PPT (FRESH GENERATION)")
                print("="*60)
                print(f"Story Topic: {final_story_topic}")
                print(f"Child Name: {child_name}")
                print(f"📝 Story Generation: {result['timings'].get('story_generation', 'N/A')}s")
                print(f"🎨 Image Generation: {result['timings'].get('image_generation', 'N/A')}s")
                print(f"🎵 Audio Generation: {result['timings'].get('audio_generation', 'N/A')}s")
                print(f"📄 PDF Generation: {result['timings'].get('pdf_generation', 'N/A')}s")
                print(f"🚀 Total Generation Time: {result['timings'].get('total_time', 'N/A')}s")
                print(f"Status: ✨ FRESH GENERATION")
                print("="*60)
            # Cache the result
            st.session_state.story_cache[cache_key] = result  # Store in cache
        
        st.session_state.tokens -= 1  # Deduct a token only for fresh generation
    
    # Store the result and change page
    st.session_state.current_story = result
    st.session_state.final_story_topic = final_story_topic  # Store the topic for the story page
    st.session_state.page = "story"

# Render the appropriate page based on state
if st.session_state.page == "home":
    # Home page with story creation form
    st.markdown("<h1 style='text-align: center;'>✨ DreamTales ✨</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Personalized Bedtime Stories for Little Dreamers</h3>", unsafe_allow_html=True)
    
    # Create two columns for a better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""<div class='feature-box'>
            <h2>Create a Magical Story</h2>
            <p>Enter a few details below to generate a personalized bedtime story complete with beautiful illustrations and narration.</p>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("### Story Details")
        child_name = st.text_input("Child's Name", placeholder="Enter child's name (optional)")
        
        # Story Topic Selection
        st.markdown("### Story Topic")

        # All topic options in a single radio button group
        all_topics = [
            "Animals", "Dinosaurs", "Superheroes", "Sports",
            "Space", "Robots", "Ocean", "Music",
            "Magic", "Fairies", "Forest"
        ]
        
        # Default to first topic if none selected
        if "selected_topic" not in st.session_state:
            st.session_state.selected_topic = all_topics[0]
            
        selected_topic = st.radio(
            "Choose a topic:",
            all_topics,
            index=all_topics.index(st.session_state.selected_topic) if st.session_state.selected_topic in all_topics else 0,
            label_visibility="collapsed",
            horizontal=True
        )
            
        # Story Tone Selection
        st.markdown("### Story Tone")
        
        # All tone options in a single radio button group
        all_tones = ["Calm & Peaceful", "Silly & Funny", "Adventurous & Exciting"]
        
        # Default to first tone if none selected
        if "selected_tone" not in st.session_state:
            st.session_state.selected_tone = all_tones[0]
            
        selected_tone = st.radio(
            "Choose a tone:",
            all_tones,
            index=all_tones.index(st.session_state.selected_tone) if st.session_state.selected_tone in all_tones else 0,
            label_visibility="collapsed",
            horizontal=True
        )
        
        # Save the selections to session state for persistence
        st.session_state.selected_topic = selected_topic
        st.session_state.selected_tone = selected_tone
        
        # Create a story idea based on selection
        story_base = f"A {selected_tone.lower()} story about {selected_topic.lower()}"
        story_topic = st.text_input("Custom Story Details (Optional)", 
                                  placeholder="Add any specific details to your story", 
                                  help="You can leave this empty or add specific details")
        
        # Combine the topic and any custom details
        if story_topic:
            final_story_topic = f"{story_base} - {story_topic}"
        else:
            final_story_topic = story_base
        
        story_length = st.select_slider("Story Length", options=["Short", "Medium"], value="Short", help="Short: 2-3 minutes | Medium: 5-7 minutes")
        
        # Create story button
        if st.button("✨ Create My Story", use_container_width=True):
            generate_and_redirect()
    
    with col2:
        st.markdown("""<div class='feature-box' style='height: 100%;'>
            <h3>Why DreamTales?</h3>
            <ul>
                <li>Personalized stories featuring your child</li>
                <li>Beautiful illustrations</li>
                <li>Voice narration</li>
                <li>Downloadable PDFs</li>
                <li>Child-appropriate content</li>
            </ul>
        </div>""", unsafe_allow_html=True)
    
    # Footer
    st.markdown("<div class='footer'>Created for LLM project by Dhanush and Charan</div>", unsafe_allow_html=True)

elif st.session_state.page == "story":
    # Story display page
    result = st.session_state.current_story
    
    # Handle AI refusal
    if result["story"].startswith("Sorry, I cannot create a story on this topic."):
        st.error(result["story"])
        if st.button("← Back to Story Creator"):
            st.session_state.page = "home"
    else:
        # Story header with navigation
        st.markdown("""<div class='story-header'>
            <h2 style='margin: 0;'>Your Magical Bedtime Story</h2>
        </div>""", unsafe_allow_html=True)
        
        # Back button
        if st.button("← Back to Story Creator"):
            st.session_state.page = "home"
        
        # Story container
        st.markdown("<div class='story-container'>", unsafe_allow_html=True)
        
        # Display main content in columns
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Story title derived from topic
            story_title = st.session_state.final_story_topic.title() if len(st.session_state.final_story_topic) < 40 else st.session_state.final_story_topic[:37].title() + "..."
            st.markdown(f"<h2>{story_title}</h2>", unsafe_allow_html=True)
            
            # Story text
            st.markdown(f"<div class='story-text'>{result['story']}</div>", unsafe_allow_html=True)
        
        with col2:
            # Illustration
            if result["image"]:
                st.markdown("### Story Illustration")
                st.image(result["image"], use_column_width=True)
            
            # Audio player
            if result["audio"]:
                st.markdown("### Listen to the Story")
                with open(result["audio"], "rb") as audio_file:
                    st.audio(audio_file, format="audio/mp3")
            
            # Download button
            if result["pdf"]:
                st.markdown("### Keep the Magic")
                with open(result["pdf"], "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download as PDF",
                        data=pdf_file,
                        file_name=f"{st.session_state.final_story_topic}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Footer
        st.markdown("<div class='footer'>Created for LLM project by Dhanush and Charan</div>", unsafe_allow_html=True)

# End of application