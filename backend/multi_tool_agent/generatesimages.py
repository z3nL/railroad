from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get the API key from the environment
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("No OpenAI API key found. Please set OPENAI_API_KEY in your .env file.")

client = OpenAI(api_key=API_KEY)

def generate_images(prompts, n_images=1, size="1024x1024"):
    """
    Generate images for a list of prompts.
    Returns a list of URLs to the generated images.
    """
    generated_urls = []
    for i, prompt in enumerate(prompts):
        print(f"Generating image {i+1}/{len(prompts)} for prompt: {prompt}")
        response = client.images.generate(
            model="dall-e-3",  # or "dall-e-3" if your account has access
            prompt=prompt,
            size=size,
            n=n_images
        )
        # Collect the URLs of generated images
        for img in response.data:
            generated_urls.append(img.url)
    return generated_urls

if __name__ == "__main__":
    sentences = [
        
        "make an image of a algebra math problem"
    ]
    
    images = generate_images(sentences, n_images=1)
    
    for url in images:
        print(url)
