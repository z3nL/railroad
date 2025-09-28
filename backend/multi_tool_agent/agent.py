import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
<<<<<<< HEAD
from generatesteps import generate_steps
from generatesimages import generate_images
"""
def make_quiz_question(topic: str) -> dict:
   # Generates a quiz question for the given topic.
    return {
        "status": "success",
        "report": f"Give the student a challenging quiz question about: {topic}."
    }
=======
>>>>>>> origin/parallel-testing

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

<<<<<<< HEAD





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
=======
    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)
>>>>>>> origin/parallel-testing
