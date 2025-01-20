import openai
import os

# Initialize OpenAI client with API Key from environment variable
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ Fixed issue

def generate_story(story_idea, word_limit=100):
    """
    Generates a short story based on a single user input.

    Parameters:
    - story_idea: A short sentence describing the story concept.
    - word_limit: Maximum number of words in the story (default: 100).

    Returns:
    - AI-generated story as a string.
    """

    # Define the prompt for the AI model with a word constraint
    prompt = f"""
    You are a skilled creative writer. Write a compelling short story based on this idea:
    "{story_idea}"
    
    Ensure the story is approximately {word_limit} words long.
    """

    # Generate the story using OpenAI's API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a skilled creative writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    # Extract the AI-generated story
    story = response.choices[0].message.content

    # Ensure the story meets the word limit constraint
    word_count = len(story.split())  # Count words in the generated story

    # If the story is too short or too long, regenerate it
    if word_count < word_limit - 10 or word_count > word_limit + 10:
        print("Regenerating story to meet word limit...")
        return generate_story(story_idea, word_limit)  # Recursive call to regenerate

    return story

# Test the function
if __name__ == "__main__":
    story_idea = "A scientist discovers a portal to another dimension."
    
    story = generate_story(story_idea, word_limit=100)
    print("\nGenerated Story:\n", story)
