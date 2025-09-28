# Part of agent.py --> Follow https://google.github.io/adk-docs/get-started/quickstart/ to learn the setup

import asyncio
import os
from dotenv import load_dotenv
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent, SequentialAgent
from google.genai import types
from google.adk.runners import InMemoryRunner
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part  # user message container
from google.adk.agents.invocation_context import InvocationContext
from google.adk.tools.tool_context import ToolContext
from typing import AsyncGenerator, Optional
from google.adk.events import Event, EventActions
from requests import session
from google.genai import Client

load_dotenv()
client = Client(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Constants ---
APP_NAME = "image_refinement_app"
USER_ID = "dev_user_01"
SESSION_ID_BASE = "loop_exit_tool_session" # New Base Session ID
GEMINI_MODEL = "gemini-2.0-flash"
STATE_INITIAL_SUBJECT = "initial_subject"

# --- State Keys ---
STATE_CURRENT_IMG = "current_image"
STATE_CRITICISM = "criticism"
# Define the exact phrase the Critic should use to signal completion
COMPLETION_PHRASE = "No major issues found."

# --- Tool Definition ---
def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    # Return empty dict as tools should typically return JSON-serializable output
    return {}

# --- Agent Definitions ---

# STEP 1: Initial Visualizer Agent (Runs ONCE at the beginning)
initial_visualizer_agent = LlmAgent(
    name="InitialVisualizerAgent",
    model=GEMINI_MODEL,
    include_contents='none',
    # MODIFIED Instruction: Ask for a slightly more developed start
    instruction=f"""You are a part of an educational tool that generates images corresponding to steps in a tutorial.
    You must generate the initial image based on the provided subject.
    If the subject is deemed to relate to a mathematical operation or equation, create a simple, clear visual representation of that operation or equation.
    Return the image as a URL. Output only the image reference.
    Subject: {{initial_subject}}

    Output *only* the URL string. Do not add anything else.
""",
    description="Creates the initial image based on the provided subject.",
    output_key=STATE_CURRENT_IMG # Saves the initial image to state['current_image']
)

# STEP 2a: Critic Agent (Inside the Refinement Loop)
critic_agent_in_loop = LlmAgent(
    name="CriticAgent",
    model=GEMINI_MODEL,
    include_contents='none',
    # MODIFIED Instruction: More nuanced completion criteria, look for clear improvement paths.
    instruction=f"""You are a Constructive Critic AI reviewing an image corresponding to a tutorial step. Your goal is balanced feedback.

    **Image to Review:**
    ```
    {{current_image}}
    ```

    **Subject Image Corresponds To:**
    ```
    {{initial_subject}}
    ```

    **Task:**
    Review the image for clarity, engagement, and basic coherence according to the initial subject (if known).

    If there is no image provided, instruct the refiner to create one from scratch using the {{initial_subject}}.

    IF you identify at least 1 *clear and actionable* way the image could be improved to better capture the subject or enhance viewer engagement (e.g., "Needs a stronger focal point", "Clarify the background details").
    If the subject is deemed to relate to a mathematical operation or equation, give feedback that will guide the image to be a simple, clear visual representation of that operation or equation.
    Provide these specific suggestions concisely. Output *only* the critique text.

    ELSE IF the image is coherent, addresses the subject adequately, such that it has no glaring errors or obvious omissions:
    Respond *exactly* with the phrase "{COMPLETION_PHRASE}" and nothing else. It doesn't need to be perfect, just functionally complete for this stage. Avoid suggesting purely subjective stylistic preferences if the core is sound.

    Do not add explanations. Output only the critique OR the exact completion phrase.
""",
    description="Reviews the current image, providing critique if clear improvements are needed, otherwise signals completion.",
    output_key=STATE_CRITICISM
)


# STEP 2b: Refiner/Exiter Agent (Inside the Refinement Loop)
refiner_agent_in_loop = LlmAgent(
    name="RefinerAgent",
    model=GEMINI_MODEL,
    # Relies solely on state via placeholders
    include_contents='none',
    instruction=f"""You are a part of an educational tool that generates images corresponding to steps in a tutorial, refining an image based on feedback OR exiting the process.
    **Current Image:**
    ```
    {{current_image}}
    ```

    **Initial Subject:**
    ```
    {{initial_subject}}
    ```
    **Critique/Suggestions:**
    {{criticism}}

    **Task:**
    Analyze the 'Critique/Suggestions'.
    IF the critique is *exactly* "{COMPLETION_PHRASE}":
    You MUST call the 'exit_loop' function. Do not output anything.
    ELSE (the critique contains actionable feedback):
    Carefully apply the suggestions to improve the 'Current Image'. 
    If the subject is deemed to relate to a mathematical operation or equation use the feedback to create a simple, clear visual representation of that operation or equation.
    Output *only* the refined image as a URL.

    Do not add explanations. Either output the refined image OR call the exit_loop function.
""",
    description="Refines the image based on critique, or calls exit_loop if critique indicates completion.",
    tools=[exit_loop], # Provide the exit_loop tool
    output_key=STATE_CURRENT_IMG # Overwrites state['current_image'] with the refined version
)


# STEP 2: Refinement Loop Agent
refinement_loop = LoopAgent(
    name="RefinementLoop",
    # Agent order is crucial: Critique first, then Refine/Exit
    sub_agents=[
        critic_agent_in_loop,
        refiner_agent_in_loop,
    ],
    max_iterations=4 # Limit loops
)

# STEP 3: Overall Sequential Pipeline
# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = SequentialAgent(
    name="IterativeVisualizationPipeline",
    sub_agents=[
        initial_visualizer_agent, # Run first to create initial image
        refinement_loop       # Then run the critique/refine loop
    ],
    description="Writes an initial image and then iteratively refines it with critique using an exit tool.",
)

async def main():
    app_name = APP_NAME
    user_id = USER_ID
    session_service = InMemorySessionService()

    # ✅ Create session with seeded state
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        state={STATE_INITIAL_SUBJECT: "Subtract 5 from x to get y"}
    )

    runner = Runner(app_name=app_name, agent=root_agent, session_service=session_service)

    user_msg = Content(parts=[Part(text="Subtract 5 from x to get y")])

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=user_msg,
    ):
        print("Event:", event)

    final_session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session.id
    )

    if final_session is None:
        print("No session found!")
    else:
        print("IMG:", final_session.state.get(STATE_CURRENT_IMG))


if __name__ == "__main__":
    asyncio.run(main())
