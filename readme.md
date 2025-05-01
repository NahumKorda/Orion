# Orion

A Streamlit application for conducting survey analysis and generating insights.

## Project Structure

```
orion/
├── app.py                 # Main entry point for Streamlit
├── requirements.txt       # Project dependencies
└── ui/
    ├── __init__.py
    ├── utils.py           # Utility functions and constants
    └── screens/           # Screens module
        ├── __init__.py
        ├── survey.py      # Survey screen implementation
        ├── filters.py     # Filters screen implementation
        ├── questions.py   # Questions screen implementation
        ├── processing.py  # Processing screen implementation
        └── insights.py    # Insights screen implementation
```