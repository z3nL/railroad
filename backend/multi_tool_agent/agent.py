# agent.py
import asyncio
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part  # user message container
import json
# Your tools (plain Python functions are auto-wrapped as FunctionTools by ADK)
from generatesteps import generate_steps
from generatesimages import generate_images

"""
def make_quiz_question(topic: str) -> dict:
   # Generates a quiz question for the given topic.
    return {
        "status": "success",
        "report": f"Give the student a challenging quiz question about: {topic}."
    }

def summarize_for_grade_level(topic: str, grade: str = "high school") -> dict:
    #Provides an instruction for simplifying content to a certain grade level.
    return {
        "status": "success",
        "report": f"Explain {topic} in a way that a {grade} student would understand."
    }"""






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

# agents.py (Only the single_image_generator part needs this update)


from google.adk.agents import Agent
# Assuming 'generate_images' is imported from your tools module

single_image_generator = Agent(
    name="single_image_generator",
    model="gemini-2.5-flash", 
    description="Generates ONE image path based on a single step.",
    instruction=(
        "You receive a single step from a sequence. You MUST call the tool "
        "`generate_images` with the step as the only item in `prompts` and `n_images=1`. "
        
        # This is the critical part to fix the empty content issue:
        # Changed the example to use strict double quotes for JSON compliance.
        "Your final output MUST be the exact list string returned by the tool, "
        "for example: [\"generated_images\\image_1_1.png\"]. " 
        "DO NOT add any prefix, suffix, conversational text, or explanation."
    ),
    tools=[generate_images],
)





parallel_image_agent = ParallelAgent(
    name = "ParallelImageGenerator",
    sub_agents= [single_image_generator],
    description= "Generate images in parallel for a given set of steps"
)



sequential_pipeline = SequentialAgent(
    name="PipelineAgent",
    sub_agents=[steps_agent, parallel_image_agent],
    description="Runs steps agent, then generates images in parallel."
)

dict = {
    "task": "algebra",
    "values": "basic algebraic operations",
    "student": "high school student"
}

root_agent = sequential_pipeline
async def main():
    app_name = "PipelineApp"
    user_id = "blake"
    session_service = InMemorySessionService()

    # 1. Setup Session
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id
    )

    # Assuming 'root_agent' is defined globally or imported
    runner = Runner(app_name=app_name, agent=root_agent, session_service=session_service)

    # 2. Prepare Input
    payload = {
        "task": "algebra",
        "values": "basic algebraic operations",
        "student": "high school student"
    }
    # The ADK expects a message object
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
        # Optional: uncomment to print all events for detailed debugging
        # print("Event:", event)

        # Check for the successful final output of a single image generator branch
        # This event contains the generated image path list (e.g., '["image_1_1.png"]')
        if (
            event.branch and 
            event.author == 'single_image_generator' and 
            event.finish_reason == 'STOP'
        ):
            # The path is in the first part of the content
            result_content = event.content.parts[0].text
            
            if result_content:
                try:
                    # Parse the string result into a Python list
                    paths = json.loads(result_content)
                    generated_image_paths.extend(paths)
                    
                except json.JSONDecodeError as e:
                    # Catch malformed JSON output from the LLM
                    print(f"Error parsing image path JSON for branch {event.branch}: {e}. Raw content: {result_content}")
                except Exception as e:
                    # Catch general errors, like the JSON object being NoneType when accessed
                    print(f"Unexpected error processing image path for branch {event.branch}: {e}")
            else:
                print(f"Warning: single_image_generator event for branch {event.branch} returned empty content.")

    # 4. Retrieve Final State
    # The loop completes only when all parallel tasks (Steps 1-4) are finished.
    state = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session.id
    )
    
    # Retrieve the steps stored by the teaching_guide_agent
    saved_steps_str = state.state.get("steps")

    # 5. Print Final Results
    print("\n" + "="*25)
    print("--- Final Results ---")
    print("="*25)
    # The key is simply 'steps', not len(steps)
    print(f"Total Steps Retrieved: {len(json.loads(saved_steps_str)) if saved_steps_str else 0}")
    print(f"Steps (Raw State Value): {saved_steps_str}")
    print("\n--- Generated Images ---")
    print(f"Total Images Collected: {len(generated_image_paths)}")
    print("Generated Images (Collected from Events):", generated_image_paths)


if __name__ == "__main__":
    # Ensure you have 'root_agent' and the service classes imported before running
    # Example: root_agent = SequentialAgent(...)
    asyncio.run(main())
