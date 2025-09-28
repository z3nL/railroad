from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from typing import List
import time

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("No OPENAI_API key found in .env or environment")

client = OpenAI(api_key=API_KEY)


def generate_images(
    prompts: List[str],
    n_images: int
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

    # Create a unique identifier for this batch to avoid overwrites
    timestamp = int(time.time() * 1000)  # milliseconds
    
    # The ParallelAgent passes ONE step (prompt) to each agent, which then 
    # calls this function with prompts=[single_step] and n_images=X.
    for i, original_prompt in enumerate(prompts):
        print(f"Generating {n_images} image(s) for step: {original_prompt[:100]}...")
        
        # Extract step number using regex - more robust approach
        import re
        
        # Try multiple regex patterns to catch different formats
        patterns = [
            r'Step (\d+)\.',           # "Step 1."
            r'Step (\d+):',            # "Step 1:"
            r'Step (\d+)\s',           # "Step 1 "
            r'(\d+)\.',                # Just "1." at the start
        ]
        
        extracted_step_num = None
        for pattern in patterns:
            step_match = re.search(pattern, original_prompt)
            if step_match:
                extracted_step_num = int(step_match.group(1))
                break
        
        # Fallback if no step number found
        if extracted_step_num is None:
            extracted_step_num = i + 1
        
        print(f"Detected step number: {extracted_step_num}")
        
        # Enhance the prompt to REQUIRE step number text in the image
        enhanced_prompt = (
            f"IMPORTANT: You MUST include the exact text 'Step {extracted_step_num}' prominently at the top of the image in large, bold, readable text. "
            f"Create a clear educational illustration that shows 'Step {extracted_step_num}' as a header. "
            f"Below that header, create a visual representation of: {original_prompt}. "
            f"The image should be educational, clean, and suitable for a high school algebra student. "
            f"Make sure 'Step {extracted_step_num}' is the most prominent text element in the image, clearly visible and easy to read. "
            f"Use a clean, educational design with good contrast so the step number stands out."
        )

        print(f"Enhanced prompt: {enhanced_prompt[:150]}...")

        # Call the OpenAI API once, asking for 'n_images' at the same time
        response = client.images.generate(
            model="gpt-image-1",
            prompt=enhanced_prompt,
            size=SIZE,
            n=n_images # Use the value supplied by the agent
        )

        for idx, img in enumerate(response.data):
            # Decode and save with regex-based naming convention
            if img.b64_json:
                img_bytes = base64.b64decode(img.b64_json)
                
                # Create clean filename using regex-extracted step number
                # Format: step_##_timestamp_imagenum.png (zero-padded for sorting)
                file_path = os.path.join(SAVE_DIR, f"step_{extracted_step_num:02d}_{timestamp}_{idx+1}.png")
                
                with open(file_path, "wb") as f:
                    f.write(img_bytes)
                generated_files.append(file_path)
                print(f"✅ Saved image: {file_path}")

    return generated_files


if __name__ == "__main__":
    sentences = [
        "A highly detailed, photorealistic image of a futuristic train arriving at a misty, neon-lit station.",
    ]
    # NOTE: Must pass n_images explicitly now
    images = generate_images(sentences, n_images=3)

    for path in images:
        print(path)