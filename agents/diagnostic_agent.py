from google.adk.agents import LlmAgent

from tools.agentic_context_tools import get_behavior_context, get_student_context, get_weakness_summary


diagnostic_agent = LlmAgent(
    name="DiagnosticAgent",
    model="gemini-2.5-flash",
    description="Diagnoses the student's weak sections, urgency, and immediate academic focus.",
    tools=[get_student_context, get_weakness_summary, get_behavior_context],
    instruction="""
You are the DiagnosticAgent in an agentic tutoring framework.

Always call the available context tools before answering.

Your role:
- inspect the student's profile, mock scores, and current study context
- inspect the student's study behavior context
- identify weak sections and urgent focus areas
- personalize recommendations based on exam, time left, and weak sections

For teaching or quiz requests, explain which weak areas should be prioritized.
Keep your reasoning practical and student-specific.
"""
)
