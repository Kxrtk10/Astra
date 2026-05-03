from google.adk.agents import LlmAgent
from tools.profile_tools import create_profile

profile_agent = LlmAgent(

    name="profile_agent",

    model="gemini-2.0-flash",

    description="Handles student profile creation",

    instruction="""
You manage student learning profiles.

If a student needs to create or update a profile,
use the available profile tool.
""",

    tools=[create_profile]
)
