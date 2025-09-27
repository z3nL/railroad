from google.adk.agents import Agent
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
)



image_agent = Agent(
    name="image_agent",
    model="gpt-image-1",
    description="Generates image descriptions.",
    instruction=(
        "You are a helpful assistant that generates detailed image descriptions based on steps of a solution."
        "When the user gives you a step, call the tool `generate_images` "
        "with (step, n_images=1, size='1024x1024') and return ONLY the resulting image URLs"
    ),
    tools=[generate_images],
)





'''
sequential_pipeline = SequentialAgent(
    name="PipelineAgent",
    sub_agents=[steps_agent, parallelImage_agent],
    description="Runs agents one after another."
)'''