# generatesimages.py - FIXED
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from typing import List

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("No OPENAI_API key found in .env or environment")

client = OpenAI(api_key=API_KEY)


def generate_images(
    prompts: List[str], # Required: This is the only parameter the LLM agent will supply
    n_images: int       # Required: The LLM agent MUST supply this value (e.g., 3)
) -> List[str]:
    """
    Generate images using gpt-image-1, save locally, and return file paths.
    
    The ADK forces the agent to explicitly call this with prompts (the steps)
    and n_images (the desired number of images per step).
    """
    
    # --- FIXED PARAMETERS (Hardcoded to avoid ADK Validation Error) ---
    SIZE: str = "1024x1024"
    SAVE_DIR: str = "generated_images"
    # -----------------------------------------------------------------

    os.makedirs(SAVE_DIR, exist_ok=True)
    generated_files = []

    # The ParallelAgent passes ONE step (prompt) to the agent, which then 
    # calls this function with prompts=[single_step] and n_images=X.
    for i, prompt in enumerate(prompts):
        print(f"Generating {n_images} image(s) for step: {prompt}")

        # Call the OpenAI API once, asking for 'n_images' at the same time
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=SIZE,
            n=n_images # Use the value supplied by the agent
        )

        for idx, img in enumerate(response.data):
            # Decode and save (no inner loop needed, as n=n_images handles it)
            if img.b64_json:
                img_bytes = base64.b64decode(img.b64_json)
                # Use a combined index for uniqueness: {prompt_index}_{n_index}
                file_path = os.path.join(SAVE_DIR, f"image_{i+1}_{idx+1}.png")
                with open(file_path, "wb") as f:
                    f.write(img_bytes)
                generated_files.append(file_path)
            # We don't expect URLs if response_format="b64_json" is used, 
            # so the URL fallback is usually not necessary.

    return generated_files


if __name__ == "__main__":
    sentences = [
        "A highly detailed, photorealistic image of a futuristic train arriving at a misty, neon-lit station.",
    ]
    # NOTE: Must pass n_images explicitly now
    images = generate_images(sentences, n_images=3)

    for path in images:
        print(path)