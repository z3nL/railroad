# agent.py
import asyncio
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part  # user message container

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



image_agent = [ LlmAgent (
    name=f"VisualizationTool_Step{i+1}",
    model="dall-e-3",
    description=f"Generates image descriptions for a step {i+1}",
    instruction=(
        "You are a helpful assistant that generates detailed image descriptions based on steps of a solution."
        "When the user gives you a step, call the tool generate_images "
        "with (step, n_images=1, size='1024x1024') and return ONLY the resulting image URLs"
    ),
    tools=[lambda step=step:generate_images([step], n_images = 1) [0]] ,
    output_key=f"image_url_step_{i+1}"
)
for i, step in enumerate(steps_agent.output["steps"])
]





parallel_image_agent = ParallelAgent(
    name = "ParallelVisualizationTool",
    sub_agents= image_agent,
    description= "Generate images in parallel for a given set of steps"
)



sequential_pipeline = SequentialAgent(
    name="PipelineAgent",
    sub_agents=[steps_agent, parallel_image_agent],
    description="Runs agents one after another."
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

    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id
    )

    runner = Runner(app_name=app_name, agent=root_agent, session_service=session_service)

    payload = {
        "task": "algebra",
        "values": "basic algebraic operations",
        "student": "high school student"
    }
    user_msg = Content(parts=[Part(text=str(payload))])

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=user_msg   # <-- fix here
    ):
        # Optional: print events to debug
        print("Event:", event)

    state = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session.id
    )
    print("Steps:", state.state.get("steps"))


if __name__ == "__main__":
    asyncio.run(main())