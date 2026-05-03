from google.adk.agents import LlmAgent

from tools.agentic_context_tools import get_behavior_context, get_student_context, get_weakness_summary
from tools.progress_tools import analyze_current_progress


progress_agent = LlmAgent(
    name="ProgressAgent",
    model="gemini-2.5-flash",
    description="Analyzes student progress, weaknesses, and improvement priorities.",
    tools=[get_student_context, get_weakness_summary, get_behavior_context, analyze_current_progress],
    instruction="""
You are the ProgressAgent in an adaptive learning multi-agent system.

Always use the available context tools before giving conclusions.

Your job:
- inspect the student's current profile and weakness profile
- inspect the student's behavior profile
- analyze current progress and likely problem areas
- identify what the student is improving in and what needs attention
- produce concise, practical observations rather than generic motivation

If progress data is sparse, say that clearly and fall back to mock scores and planner state.
"""
)
