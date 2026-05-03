import json
import os


def analyze_progress(username):

    progress_file = f"progress/{username}_progress.json"

    if not os.path.exists(progress_file):
        return "No progress data available yet."

    with open(progress_file, "r") as f:
        progress = json.load(f)

    report = "\nLearning Progress Report\n\n"

    report += f"Topics studied: {len(progress.get('topics_studied', []))}\n"
    report += f"Quiz attempts: {len(progress.get('quiz_scores', []))}\n"

    if progress.get("weak_topics"):
        report += "\nWeak topics:\n"
        for topic in progress["weak_topics"]:
            report += f"- {topic}\n"

    else:
        report += "\nNo weak topics detected yet."

    return report