import openai
import os
import tempfile
import requests
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

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

    # Generate a downloadable PDF with the image
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
    """Generates a well-formatted PDF file with text-wrapped story and illustration."""
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    # Define PDF canvas
    c = canvas.Canvas(temp_pdf.name, pagesize=letter)
    page_width, page_height = letter  # Get page size

    # Set title at the top
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, page_height - 80, f"Cozy Story Time 🛏️📖 - {title}")

    # Download and add the image below the title
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            img = Image.open(response.raw)
            img_reader = ImageReader(img)

            # Adjust image placement (below the title, centered)
            img_width = 250  # Fixed width
            img_height = 250  # Fixed height
            img_x = (page_width - img_width) / 2  # Center image
            img_y = page_height - 350  # Adjust Y-position below title

            c.drawImage(img_reader, img_x, img_y, width=img_width, height=img_height)

    except Exception as e:
        print("Error fetching image:", e)

    # Add story text below the image with proper line wrapping
    text_start_y = img_y - 50  # Leave space below the image
    c.setFont("Helvetica", 12)

    # Define max text width to wrap lines properly
    text_margin_x = 50
    max_text_width = page_width - 100  # Leave margins

    # Split the text into properly wrapped lines
    from textwrap import wrap
    wrapped_lines = []
    for paragraph in story.split("\n"):  # Split paragraphs
        wrapped_lines.extend(wrap(paragraph, width=90))  # Adjust width for wrapping
        wrapped_lines.append("")  # Add blank line after each paragraph

    # Add the wrapped text to the PDF
    text_y_position = text_start_y
    for line in wrapped_lines:
        if text_y_position < 50:  # Start a new page if needed
            c.showPage()
            text_y_position = page_height - 100  # Reset text position for new page
            c.setFont("Helvetica", 12)

        c.drawString(text_margin_x, text_y_position, line)
        text_y_position -= 18  # Move cursor down for next line

    # Save the PDF
    c.save()

    return temp_pdf.name