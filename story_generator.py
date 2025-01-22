import openai
import os
import tempfile
from pydub import AudioSegment
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_story_and_image(story_topic, story_length="short"):
    """
    Generates a bedtime story along with a relevant image.

    Returns:
    - Dictionary with story text, image URL, audio file path, and PDF file path.
    """

    # Generate the bedtime story
    story_prompt = f"""
    Create a gentle bedtime story for children aged 2-5 years old about {story_topic}.
    Story length: {story_length.upper()} (2-3 minutes for short, 5-7 minutes for medium)
    """

    story_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": story_prompt}],
        temperature=0.7
    )

    story_text = story_response.choices[0].message.content.strip()

    # Generate an image using DALL·E
    image_prompt = f"Illustration for a children's bedtime story about {story_topic}. The scene should be warm and cozy."
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        size="1024x1024",
        n=1
    )
    image_url = image_response.data[0].url

    # Generate voice narration using OpenAI's TTS API
    audio_file_path = generate_voice_narration(story_text)

    # Generate a downloadable PDF
    pdf_file_path = generate_pdf(story_topic, story_text, image_url)

    return {
        "story": story_text,
        "image": image_url,
        "audio": audio_file_path,
        "pdf": pdf_file_path
    }

def generate_voice_narration(text):
    """Converts text into speech using OpenAI's TTS API."""
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_audio.write(response.content)
    temp_audio.close()

    return temp_audio.name

def generate_pdf(title, story, image_url):
    """Generates a PDF file with the story and illustration."""
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    
    c = canvas.Canvas(temp_pdf.name, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"Cozy Story Time 🛏️📖 - {title}")
    
    c.setFont("Helvetica", 12)
    text = c.beginText(100, 720)
    text.setFont("Helvetica", 12)
    text.setLeading(14)

    # Split text into lines
    for line in story.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.save()
    
    return temp_pdf.name
