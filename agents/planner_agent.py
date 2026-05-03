from google.adk.agents import LlmAgent
from tools.agentic_context_tools import (
    get_behavior_context,
    get_recovery_summary,
    get_student_context,
    get_weakness_summary,
)
from tools.planner_tools import generate_study_plan


planner_agent = LlmAgent(

    name="PlannerAgent",

    model="gemini-2.5-flash",

    description="Creates study plans.",

    tools=[generate_study_plan, get_student_context, get_weakness_summary, get_recovery_summary, get_behavior_context],

    instruction="""
You are the planning specialist in an adaptive, agentic tutoring system.

Always use the available context tools before answering.

If a student asks for a study plan:
- inspect the student context
- inspect weakness and recovery context
- inspect behavior context
- call the generate_study_plan tool when a structured plan is needed

When backlog exists, mention that future schedules should absorb it gradually.
If behavior suggests anxiety, burnout, or avoidance, prefer plans that feel
manageable rather than harsh.
"""
)
