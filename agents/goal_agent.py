from google.adk.agents import LlmAgent
from tools.planner_tools import generate_study_plan

goal_agent = LlmAgent(

    name="goal_agent",

    model="gemini-2.0-flash",

    description="Creates study plans for students",

    instruction="""
Create study plans based on:

• exam name
• exam date
• subjects
• daily study hours

Allocate time across subjects effectively.
""",

    tools=[generate_study_plan]
)
