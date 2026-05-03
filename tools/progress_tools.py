import json
import os

from google.adk.tools import ToolContext


def analyze_progress(username: str):

    progress_file = f"progress/{username}_progress.json"

    if not os.path.exists(progress_file):
        return "No progress data available yet."

    with open(progress_file, "r") as f:
        data = json.load(f)

    report = "\nProgress Report\n"

    for topic, stats in data.items():

        attempted = stats.get("attempted", 0)
        correct = stats.get("correct", 0)

        if attempted == 0:
            accuracy = 0
        else:
            accuracy = round((correct / attempted) * 100, 2)

        report += f"\n{topic} → {accuracy}% accuracy"

    return report


def analyze_current_progress(tool_context: ToolContext):
    """Analyze progress for the active student in session state."""

    profile = tool_context.state.get("profile")
    if not profile:
        return "No active student profile is available in session state."

    return analyze_progress(profile["name"])
