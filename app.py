import streamlit as st
import os
from ui.screens.survey import show_survey_screen
from ui.screens.filters import show_filters_screen
from ui.screens.questions import show_questions_screen
from ui.screens.processing import show_processing_screen
from ui.screens.insights import show_insights_screen

# Initialize session state variables if they don't exist
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'survey'

# Page config
st.set_page_config(
    page_title="Orion",
    page_icon="🔍",
    layout="wide",
)

# Load external CSS
def load_css(css_file):
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS file
css_path = os.path.join(os.path.dirname(__file__), "ui/orion.css")
load_css(css_path)

if 'validated' not in st.session_state:
    st.session_state.validated = {
        'Survey': False,
        'Filters': False,
        'Questions': False
    }

# Display the current screen
if st.session_state.current_screen == 'survey':
    show_survey_screen()
elif st.session_state.current_screen == 'filters':
    show_filters_screen()
elif st.session_state.current_screen == 'questions':
    show_questions_screen()
elif st.session_state.current_screen == 'processing':
    show_processing_screen()
elif st.session_state.current_screen == 'insights':
    show_insights_screen()