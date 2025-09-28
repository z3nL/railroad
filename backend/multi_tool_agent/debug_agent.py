import asyncio
from google.adk.agents import Agent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
import json
from generatesteps import generate_steps

# Simple test to see what the steps_agent outputs
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

# Simple agent that just echoes what it receives
echo_agent = Agent(
    name="echo_agent",
    model="gemini-2.5-flash",
    description="Echoes back what it receives",
    instruction=(
        "You will receive some input. Simply repeat back exactly what you received. "
        "If you receive an array, list each item on a separate line with its index. "
        "Start your response with 'RECEIVED:' followed by the content."
    ),
)

debug_pipeline = SequentialAgent(
    name="DebugPipeline",
    sub_agents=[steps_agent, echo_agent],
    description="Debug pipeline to see data flow"
)

async def debug_main():
    app_name = "DebugApp"
    user_id = "blake"
    session_service = InMemorySessionService()

    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id
    )

    runner = Runner(app_name=app_name, agent=debug_pipeline, session_service=session_service)

    payload = {
        "task": "algebra",
        "values": "basic algebraic operations", 
        "student": "high school student"
    }
    user_msg = Content(parts=[Part(text=str(payload))])

    print("=== DEBUG: Running simple pipeline ===")
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=user_msg
    ):
        print(f"\nEvent from: {getattr(event, 'author', 'Unknown')}")
        print(f"Branch: {getattr(event, 'branch', 'None')}")
        print(f"Finish: {getattr(event, 'finish_reason', 'N/A')}")
        
        # Try to extract content safely
        if hasattr(event, 'content') and event.content:
            if hasattr(event.content, 'parts') and event.content.parts:
                for i, part in enumerate(event.content.parts):
                    if hasattr(part, 'text') and part.text:
                        print(f"Content part {i}: {part.text}")
            else:
                print(f"Content (no parts): {event.content}")
        else:
            print("No content found")

    # Check final state
    state = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session.id
    )
    
    print(f"\n=== FINAL STATE ===")
    print(f"State keys: {list(state.state.keys())}")
    steps_str = state.state.get("steps")
    if steps_str:
        print(f"Steps: {steps_str}")
        try:
            steps_array = json.loads(steps_str)
            print(f"Parsed steps ({len(steps_array)} items):")
            for i, step in enumerate(steps_array):
                print(f"  {i}: {step}")
        except:
            print("Could not parse steps as JSON")
    else:
        print("No steps found in state")

if __name__ == "__main__":
    asyncio.run(debug_main())