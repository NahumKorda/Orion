# Predefined questions list for the Questions screen
import os
from pathlib import Path

PREDEFINED_QUESTIONS = [
    "What primarily motivates each group's choice?",
    "What else influences each group's choice?",
    "What is the percentage of undecided in each group?",
    "Where are the core supporters in each group?",
    "What are the key concerns for each demographic?",
    "How do economic factors influence voting patterns?",
    "What communication channels are most effective for each group?",
    "How do regional differences affect political alignments?",
    "What policy areas generate the most engagement?",
    "How has sentiment shifted over the past election cycle?"
]


def get_data_path():
    current_path = Path(__file__).resolve()
    package_root = current_path.parent.resolve()
    project_root = package_root.parent.resolve()
    return os.path.join(project_root, "data")
