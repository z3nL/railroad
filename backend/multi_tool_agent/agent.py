from google.adk.agents import Agent
from generatesteps import generate_steps
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
