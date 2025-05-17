import os
from pathlib import Path

PREDEFINED_QUESTIONS = [
    "How would you rate the current job performance of the President of the United States?",
    "What issues or challenges do you believe are most pressing for the country right now?",
    "What specific factors contribute to your disapproval of the President’s performance, if any?",
    "Overall, how satisfied are you with the current direction in which the country is heading?",
    "What developments or changes, if any, would lead you to reconsider your current opinion of the President?",
    "To what extent does the state of the economy influence your support for the President?",
    "When evaluating the President, which do you prioritize more: their communication style or their policy decisions?",
    "How does level of education relate to approval or disapproval of the President, based on your view or experience?",
    "What emotions best describe how you feel about the President (e.g., hopeful, angry, proud, anxious)?",
    "How do individuals across different political affiliations emotionally describe the current state of the nation?"
]


def get_data_path():
    current_path = Path(__file__).resolve()
    package_root = current_path.parent.resolve()
    project_root = package_root.parent.resolve()
    return os.path.join(project_root, "data")
