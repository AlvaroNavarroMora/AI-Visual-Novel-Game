import os
from openai import AzureOpenAI
import requests
import uuid
import time

client = None
image_client = None
SYSTEM_MESSAGE = """
You are an interactive children's storyteller. Your role is to create engaging, imaginative, and age-appropriate stories for kids. You should actively involve the child in the storytelling process by asking questions, offering choices, and allowing them to influence the plot.

Guidelines:

Keep the language simple, fun, and engaging.
Use vivid descriptions, friendly characters, and positive messages.
Encourage creativity by asking the child to name characters, choose between plot options, or guess what happens next.
Maintain a warm and encouraging tone, making the child feel like part of the adventure.
Ensure stories are suitable for children aged 4–10, avoiding dark or scary themes.
If the child asks for a new story, start fresh with a new adventure.
Be flexible and adapt the story based on the child's responses and preferences.
Example Interaction:

You: "Once upon a time in a magical forest, there was a tiny dragon who loved to explore. What should we name the dragon?"
Child: "Sparkle!"
You: "Great choice! One day, Sparkle found a mysterious glowing door in the middle of the woods. Should Sparkle open it or call a friend for help?"
Let the magic begin!
"""

INSTRUCTIONS_SCENE_PROMPT = """
You are an expert in scene description. Analyze the text provided and extract the main idea of the scene, focus in the most important things and generate a description suitable for an image generation AI.
The image will be use as a *background* scenario for an storytelling AI. It should be only a backgound, the character should not appear in the image.
The answer must be a sentence.
"""


def create_client():
    global client
    """Creates and configures the Azure OpenAI client."""
    try:
        client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),  
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )
        print("Azure OpenAI client created successfully.")
    except Exception as e:
        print(f"Error creating Azure OpenAI client: {e}")

def generate_response(conversation):
    """Generates a response from Azure OpenAI."""
    try:
        messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
        messages.extend(conversation)
        response = client.chat.completions.create(
        model=os.getenv("OPENAI_DEPLOYMENT_NAME"),
        messages=messages
        )
        openai_response = response.choices[0].message.content
        print(f"OpenAI response: {openai_response}")
        return openai_response
    except Exception as e:
        print(f"Error generating OpenAI response: {e}")
        return "Sorry, I encountered an error processing your request."
    
def create_image_prompt(text):
    """
    Generates an image prompt based on the AI's response.
    """
    try:
        messages = [{"role": "system", "content": INSTRUCTIONS_SCENE_PROMPT}]
        messages.append({"role": "user", "content": text})
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_DEPLOYMENT_NAME"),
            messages=messages
        )
        image_prompt = response.choices[0].message.content
        print(f"Image prompt: {image_prompt}")
        return image_prompt
    except Exception as e:
        print(f"Error generating image prompt: {e}")
        return "A general scene with a children book"

def create_image_client():
    global image_client
    """Creates and configures the Azure OpenAI client."""
    try:
        image_client = AzureOpenAI(
            api_key=os.getenv("OPENAI_IMAGE_API_KEY"),  
            api_version=os.getenv("OPENAI_IMAGE_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_IMAGE_ENDPOINT"),
        )
        print("Azure OpenAI image client created successfully.")
    except Exception as e:
        print(f"Error creating Azure OpenAI image client: {e}")

def generate_image(image_name, image_prompt):
    """
    Generates an image using DALL-E based on the given prompt.
    Saves the generated image to a file.
    """
    try:
        response = image_client.images.generate(
            model=os.getenv("OPENAI_IMAGE_DEPLOYMENT_NAME"),
            prompt=image_prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url

        # Download the image
        image_data = requests.get(image_url).content

        # Save the image to a file
        image_path = os.path.join("static", "img", image_name)
        with open(image_path, "wb") as image_file:
            image_file.write(image_data)

        print(f"Image saved to {image_path}")
        # Wait a little to ensure the file is saved
        time.sleep(2)
        return image_name

    except Exception as e:
        print(f"Error generating image: {e}")
        return "book-cover.png"

