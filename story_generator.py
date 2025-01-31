import openai
import os
import requests
from fpdf import FPDF
from gtts import gTTS

# Load OpenAI API Key from Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def generate_story_text(story_topic, story_length):
    """Generates a bedtime story text based on the topic and length."""
    prompt = f"""
    Create a gentle bedtime story for children aged 2-5 years old about {story_topic}.
    Story length: {story_length}

    Story Requirements:
    - Transform the given topic into a calm, bedtime-appropriate narrative
    - Include no more than 2-3 main characters with simple, easy-to-pronounce names
    - Set the story in a peaceful environment (bedroom, garden, or under stars)
    - Weave in familiar bedtime routines and comfort objects
    - Use simple words and short sentences (5-8 words)
    - Include 2-3 soft sound effects (like "whoosh" of wind or "twinkle" of stars)
    - Include mild, calming humor if appropriate
    - Use a rhythmic, peaceful tone throughout

    Format Structure:
    - Clear beginning introducing the peaceful setting and characters
    - Middle focusing on gentle activities and bedtime routines
    - Calm ending with characters getting sleepy and going to bed

    Remember: Every element of the story should guide children toward feeling calm and ready for sleep.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a bedtime storyteller."},
                  {"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    return response["choices"][0]["message"]["content"]

def generate_story_image(story_topic):
    """Generates an illustration based on the story topic."""
    image_url = "https://via.placeholder.com/500"  # Placeholder for API call
    response = openai.Image.create(
        prompt=f"A cozy and magical bedtime illustration about {story_topic}.",
        n=1,
        size="512x512"
    )
    
    image_url = response["data"][0]["url"]
    image_path = "story_image.png"
    
    with open(image_path, "wb") as img_file:
        img_file.write(requests.get(image_url).content)

    return image_path

def generate_story_audio(story_text):
    """Converts the generated story into voice narration."""
    tts = gTTS(text=story_text, lang="en", slow=False)
    audio_path = "story_audio.mp3"
    tts.save(audio_path)
    return audio_path

def generate_story_pdf(story_text, image_path):
    """Creates a PDF with the story and illustration."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    pdf.cell(200, 10, "Cozy Story Time", ln=True, align="C")
    pdf.image(image_path, x=40, y=20, w=130)
    
    pdf.ln(80)  # Space after image
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, story_text)

    pdf_path = "story.pdf"
    pdf.output(pdf_path)
    
    return pdf_path