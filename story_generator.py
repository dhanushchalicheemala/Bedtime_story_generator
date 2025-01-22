import openai
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_story_and_image(story_topic, story_length="short"):
    """
    Generates a bedtime story along with a relevant image.

    Parameters:
    - story_topic (str): The central theme of the story.
    - story_length (str): "short" (2-3 minutes) or "medium" (5-7 minutes).

    Returns:
    - A dictionary with the story text and the image URL.
    """

    # Adjust word limit based on story length
    word_limit = 250 if story_length == "short" else 400

    # Generate the bedtime story
    story_prompt = f"""
    Create a gentle bedtime story for children aged 2-5 years old about {story_topic}.
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

    # Generate an image prompt based on the story setting
    image_prompt = f"Illustration for a children's bedtime story about {story_topic}. The scene should be warm and cozy, with soft lighting, gentle colors, and a peaceful atmosphere. The main character(s) should be in a relaxing environment, like a bedroom, garden, or under a starry sky."

    # Request image generation from OpenAI's DALL·E
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        size="1024x1024",
        n=1
    )

    image_url = image_response.data[0].url  # Extract the generated image URL

    # Return both story and image
    return {
        "story": story_text,
        "image": image_url
    }
