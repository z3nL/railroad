import asyncio
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part  # user message container
import json
# Your tools (plain Python functions are auto-wrapped as FunctionTools by ADK)
from .generatesteps import generate_steps
from .generatesimages import generate_images

steps_agent = Agent(
    name="teaching_guide_agent",
    model="gemini-2.5-flash",
    description="Generates step-by-step plans for students.",
    instruction=(
        "You are a helpful teaching assistant. "
        "When the user asks for a step-by-step plan, call the tool `generate_steps` "
        "with (task, values, student) and return ONLY the resulting array of strings."
    ),
    tools=[generate_steps],
    output_key="steps"
)

# Create a custom agent that processes individual steps
class StepProcessorAgent(Agent):
    def __init__(self, step_index: int):
        super().__init__(
            name=f"step_processor_{step_index}",
            model="gemini-2.5-flash",
            description=f"Processes step {step_index} and generates an image.",
            instruction=(
                f"You will receive an array of steps. Extract step {step_index} (0-indexed) from the array. "
                f"Then call `generate_images` with that single step as the only item in prompts and n_images=1. "
                f"Return ONLY the exact list string returned by the tool. "
                f"DO NOT add any prefix, suffix, conversational text, or explanation."
            ),
            tools=[generate_images]
        )
        self.step_index = step_index

# Alternative approach: Create a manual distributor
def create_step_image_generator(step_number: int) -> Agent:
    return Agent(
        name=f"step_image_generator_{step_number}",
        model="gemini-2.5-flash",
        description=f"Generates image for step {step_number}",
        instruction=(
            f"You will receive context from a previous agent that contains steps. "
            f"Find the step content that logically corresponds to step {step_number}. "
            f"This might be explicitly labeled 'Step {step_number}.' or it might be unlabeled content that represents step {step_number}. "
            f"Extract that step's content and create an enhanced prompt that FORCES the image to show 'Step {step_number}' as the header. "
            f"Call `generate_images` with a specially crafted prompt that includes: "
            f"'Create an educational image with Step {step_number} as the prominent header, showing: [step content]' "
            f"The key requirement is that the image MUST display 'Step {step_number}' regardless of what step number (if any) appears in the original content. "
            f"Return ONLY the exact JSON array returned by the tool. "
            f"DO NOT add explanations or extra text, just the JSON array of file paths."
        ),
        tools=[generate_images],
    )

# Create agents for the first 6 steps (adjust number as needed)
step_image_generators = [create_step_image_generator(i) for i in range(1, 7)]

parallel_image_agent = ParallelAgent(
    name="ParallelImageGenerator",
    sub_agents=step_image_generators,
    description="Generate images in parallel for individual steps from the array"
)

sequential_pipeline = SequentialAgent(
    name="PipelineAgent",
    sub_agents=[steps_agent, parallel_image_agent],
    description="Runs steps agent, then generates images in parallel for each step."
)

root_agent = sequential_pipeline

async def main(topic, description, level):
    app_name = "PipelineApp"
    user_id = "blake"
    session_service = InMemorySessionService()

    # 1. Setup Session
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id
    )

    runner = Runner(app_name=app_name, agent=root_agent, session_service=session_service)

    # 2. Prepare Input
    payload = {
        "task": topic,
        "values": description,
        "student": level
    }
    user_msg = Content(parts=[Part(text=str(payload))])

    # --- Result Collection Variables ---
    generated_image_paths = []
    
    # 3. Run the Pipeline and Collect Events
    print("Starting pipeline execution...")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=user_msg
    ):
        # Debug: Print all events to see what's happening
        print(f"Event: {event.author} | Branch: {event.branch} | Finish: {getattr(event, 'finish_reason', 'N/A')}")
        
        # Safely extract content
        result_content = None
        if hasattr(event, 'content') and event.content:
            if hasattr(event.content, 'parts') and event.content.parts:
                # Look for text in the parts
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        result_content = part.text
                        print(f"Content: {result_content[:100]}...")
                        break
            elif hasattr(event.content, 'text') and event.content.text:
                # Direct text access
                result_content = event.content.text
                print(f"Content (direct): {result_content[:100]}...")

        # Check for successful final output from step image generators
        # Look for function response events instead of direct agent responses
        if (
            event.branch and 
            event.author and event.author.startswith('step_image_generator_') and 
            getattr(event, 'finish_reason', None) == 'STOP'
        ):
            # Check if this is a function call response (the actual image generation result)
            if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts'):
                for part in event.content.parts:
                    # Look for function response parts that contain the generated image paths
                    if hasattr(part, 'function_response') and part.function_response:
                        try:
                            # Extract the result from the function response
                            if hasattr(part.function_response, 'response'):
                                result_data = part.function_response.response
                                if isinstance(result_data, list):
                                    generated_image_paths.extend(result_data)
                                    print(f"✅ Collected image paths from {event.author}: {result_data}")
                                elif isinstance(result_data, str):
                                    # Sometimes the result might be a JSON string
                                    try:
                                        paths = json.loads(result_data)
                                        generated_image_paths.extend(paths)
                                        print(f"✅ Collected image paths from {event.author}: {paths}")
                                    except:
                                        print(f"⚠️  Couldn't parse result from {event.author}: {result_data}")
                        except Exception as e:
                            print(f"❌ Error extracting function response from {event.author}: {e}")
            
            # If no function response found, this might be the function call itself
            if result_content:
                try:
                    paths = json.loads(result_content)
                    generated_image_paths.extend(paths)
                    print(f"✅ Collected image paths from {event.author}: {paths}")
                except json.JSONDecodeError as e:
                    print(f"❌ Error parsing JSON from {event.author}: {e}")
                    print(f"Raw content: {result_content}")
                except Exception as e:
                    print(f"❌ Unexpected error from {event.author}: {e}")
            else:
                print(f"⚠️  Function call detected from {event.author}, waiting for function response...")

    # 4. Retrieve Final State
    state = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session.id
    )
    
    saved_steps_str = state.state.get("steps")

    # 5. Print Final Results
    print("\n" + "="*50)
    print("--- Final Results ---")
    print("="*50)
    
    if saved_steps_str:
        steps_array = json.loads(saved_steps_str)
        print(f"Total Steps Generated: {len(steps_array)}")
        for i, step in enumerate(steps_array, 1):
            print(f"  Step {i}: {step}")
    else:
        print("No steps found in state")
    
    print(f"\n--- Generated Images ---")
    print(f"Total Images Collected: {len(generated_image_paths)}")
    for i, path in enumerate(generated_image_paths, 1):
        print(f"  Image {i}: {path}")

    # Check if we have the right number of images
    if saved_steps_str:
        expected_images = len(json.loads(saved_steps_str))
        actual_images = len(generated_image_paths)
        if actual_images == expected_images:
            print(f"✅ SUCCESS: Generated {actual_images} images for {expected_images} steps")
        else:
            print(f"⚠️  MISMATCH: Expected {expected_images} images, got {actual_images}")
    
    return steps_array if saved_steps_str else []


if __name__ == "__main__":
    asyncio.run(main("algebra", "basic algebraic operations", "high school student"))