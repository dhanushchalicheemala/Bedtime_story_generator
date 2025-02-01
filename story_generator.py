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

    story_prompt = f"""
    **IMPORTANT INSTRUCTIONS FOR AI:**
    - If the topic contains **violence**, **vulgarity**, **scary content**, **evil characters**, **battles**, or anything inappropriate for children aged 3-5, **DO NOT** create the story. 
    - In such cases, respond with: **"Sorry, I cannot create a story on this topic."**
    - If the topic is unclear or potentially inappropriate, err on the side of caution and do not generate the story.

    Now, create a gentle bedtime story for children aged 3-5 years old about {story_topic}.
    Story length: {story_length.upper()} ({'2-3 minutes' if story_length == 'short' else '5-7 minutes'})

    **Story Requirements:**
    - Transform the given topic into a calm, bedtime-appropriate narrative
    - Include no more than 2-3 main characters with simple, easy-to-pronounce names
    - Set the story in a peaceful environment (bedroom, garden, or under the stars)
    - Weave in familiar bedtime routines and comfort objects
    - Use simple words and short sentences (5-8 words)
    - Include {'2-3' if story_length == 'short' else '3-4'} scenes
    - Add gentle repetitive phrases that children can predict and say along
    - Include 2-3 soft sound effects (like "whoosh" of wind or "twinkle" of stars)
    - Add 1-2 interactive moments where children can mimic actions (stretching, yawning, counting)
    - End with characters feeling sleepy and peaceful

    **Strict Guidelines:**
    - **No violence, battles, scary content, evil characters, or complex conflicts.**
    - **No inappropriate themes or language.**
    - If the topic doesn’t fit these guidelines, reply: **"Sorry, I cannot create a story on this topic."**

    **Writing Style:**
    - Use soothing descriptive words (soft, cozy, warm, snuggly)
    - Keep sentences simple and direct
    - Include gentle parent/caregiver figures
    - Avoid any scary elements or conflicts
    - Include mild, calming humor if appropriate
    - Use a rhythmic, peaceful tone throughout

    **Format Structure:**
    - Clear beginning introducing the peaceful setting and characters
    - Middle focusing on gentle activities and bedtime routines
    - Calm ending with characters getting sleepy and going to bed
    - Simple questions or prompts in [brackets] for parent-child interaction
    """

    # Request story generation from OpenAI
    story_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": story_prompt}],
        temperature=0.7
    )

    story_text = story_response.choices[0].message.content.strip()

    # If AI refuses to create the story, skip further generation
    if "Sorry, I cannot create a story on this topic." in story_text:
        return {"story": story_text, "image": None, "audio": None, "pdf": None}

    image_url = generate_image(story_topic)
    audio_file_path = generate_voice_narration(story_text)
    pdf_file_path = generate_pdf(story_topic, story_text, image_url)

    return {
        "story": story_text,
        "image": image_url,
        "audio": audio_file_path,
        "pdf": pdf_file_path
    }

def generate_image(story_topic):
    """Generates an image using DALL·E."""
    try:
        image_prompt = f"Illustration for a children's bedtime story about {story_topic}. The scene should be warm and cozy."
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def generate_voice_narration(text):
    """Converts text into speech using OpenAI's TTS API."""
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_audio.write(response.content)
        temp_audio.close()
        return temp_audio.name
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

def generate_pdf(title, story, image_url):
    """Generates a well-formatted PDF with the story and illustration."""
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_pdf.name, pagesize=letter)
    page_width, page_height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, page_height - 80, f"Cozy Story Time - {title}")

    # Add image if available
    if image_url:
        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                img = Image.open(response.raw)
                img_reader = ImageReader(img)
                c.drawImage(img_reader, 150, page_height - 350, width=250, height=250)
        except Exception as e:
            print("Error fetching image:", e)

    # Add story text
    c.setFont("Helvetica", 12)
    y = page_height - 400
    for line in story.split('\n'):
        c.drawString(50, y, line)
        y -= 18

    c.save()
    return temp_pdf.name