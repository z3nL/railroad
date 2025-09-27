from google.adk.agents import Agent

def make_quiz_question(topic: str) -> dict:
    """Generates a quiz question for the given topic."""
    return {
        "status": "success",
        "report": f"Give the student a challenging quiz question about: {topic}."
    }

def summarize_for_grade_level(topic: str, grade: str = "high school") -> dict:
    """Provides an instruction for simplifying content to a certain grade level."""
    return {
        "status": "success",
        "report": f"Explain {topic} in a way that a {grade} student would understand."
    }

root_agent = Agent(
    name="teaching_guide_agent",
    model="gemini-2.5-flash",
    description="An educational agent that can explain any school subject, create practice questions, and adapt explanations to grade level.",
    instruction=(
        "You are a helpful teaching assistant. "
        "You can explain any school subject clearly, summarize topics, "
        "and generate quiz questions to help the student learn."
    ),
    tools=[make_quiz_question, summarize_for_grade_level],
)