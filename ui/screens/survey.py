import json
import os
import streamlit as st

from agents.keywords.crew import KeywordExtractingCrew
from agents.questions.crew import SurveyAnalyzingCrew
from ui.screens.html import reduced_title_padding
from ui.utils import get_data_path
from utils.pdf_reader import get_text


def process_file(file_path: str):
    """Process the uploaded file and extract survey data"""
    survey_results = get_text(file_path)
    inputs = {
        'survey_results': survey_results
    }
    raw_results = SurveyAnalyzingCrew().crew().kickoff(inputs=inputs)
    raw_keywords = KeywordExtractingCrew().crew().kickoff(inputs=inputs)

    try:
        results = json.loads(raw_results.json)
        keywords = json.loads(raw_keywords.json)

        # Store results and file path in session state
        st.session_state.survey_results = results
        st.session_state.survey_data['uploaded_file'] = file_path

        # Store keywords
        st.session_state.filters = {
            'keywords': keywords,
            'sentiment': [],
        }

        # Directly populate questions now instead of using a flag
        populate_questions_from_results(results)

        # Mark as processed and set the tab
        st.session_state.file_processed = True
        st.session_state.active_tab = 1  # Index for "Enter Questions" tab

        return True
    except Exception as e:
        st.error(f"Error processing survey data: {str(e)}")
        return False


def populate_questions_from_results(results):
    """Convert processed survey results to the format needed for the manual entry form"""
    if 'questions' not in results:
        st.warning("The processed results don't contain the expected 'questions' key.")
        return

    # Clear existing questions
    st.session_state.survey_data['questions'] = []

    # Add each question from the results
    for q in results.get('questions', []):
        # Extract and normalize data_type
        data_type = q.get('data_type', 'Percent')
        # Ensure data_type is one of the valid options
        if data_type.lower() == "percent":
            data_type = "Percent"
        elif data_type.lower() == "count":
            data_type = "Count"
        else:
            data_type = "Percent"

        question_data = {
            'question': q.get('question', ''),
            'data_type': data_type,
            'answers': []
        }

        # Add each answer
        for ans in q.get('answers', []):
            question_data['answers'].append({
                'answer': ans.get('answer', ''),
                'value': float(ans.get('value', 0))
            })

        # If no answers were found, add an empty one
        if not question_data['answers']:
            question_data['answers'].append({'answer': '', 'value': 0})

        st.session_state.survey_data['questions'].append(question_data)

    # If no questions were found, add an empty one
    if not st.session_state.survey_data['questions']:
        st.session_state.survey_data['questions'].append({
            'question': '',
            'data_type': 'Percent',
            'answers': [{'answer': '', 'value': 0}]
        })


def is_survey_data_valid():
    """Check if the survey data is valid for proceeding to the next screen"""
    # Check if we have at least one question
    if not st.session_state.survey_data['questions']:
        return False

    # For manually entered questions, check if at least one question has content
    for question in st.session_state.survey_data['questions']:
        # Check if question text exists and is not just whitespace
        if question.get('question') and question.get('question').strip():
            # Check if at least one answer has content
            for answer in question.get('answers', []):
                if answer.get('answer') and answer.get('answer').strip():
                    return True

    # If we got here without returning True, then no valid questions were found
    return False


def show_survey_screen():
    st.markdown(reduced_title_padding(), unsafe_allow_html=True)

    # Create a centered container with 50% width
    container = st.container()
    with container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title("Survey")

            # Initialize session state for survey data if not exists
            if 'survey_data' not in st.session_state:
                st.session_state.survey_data = {
                    'title': '',
                    'uploaded_file': None,
                    'questions': []
                }
                # Add first empty question
                st.session_state.survey_data['questions'].append({
                    'question': '',
                    'data_type': 'Percent',
                    'answers': [{'answer': '', 'value': 0}]
                })

            # Initialize active tab index (using integer for simplicity)
            if 'active_tab' not in st.session_state:
                st.session_state.active_tab = 0  # Default to Upload Survey tab

            # Create tabs and set the active tab
            tab_titles = ["Upload Survey", "Enter Questions"]
            tabs = st.tabs(tab_titles)

            # Show success message if we just processed a file
            if st.session_state.get('file_processed', False):
                st.success("Survey data successfully processed! You can now edit the extracted questions.")
                # Reset the flag to prevent showing the message on every refresh
                st.session_state.file_processed = False

            # Tab 0: Upload Survey
            with tabs[0]:
                st.subheader("Upload your survey document")

                # File uploader for PDF files
                uploaded_file = st.file_uploader("Choose a file",
                                                 type=["pdf"],
                                                 help="Upload your survey document (PDF only)",
                                                 key='survey_uploader')

                if uploaded_file is not None:
                    # Create downloads directory if it doesn't exist
                    data_path = get_data_path()
                    downloads_path = os.path.join(data_path, "downloads")
                    os.makedirs(downloads_path, exist_ok=True)

                    # Save the uploaded file to the downloads folder
                    file_path = os.path.join(downloads_path, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Process button to give user control over when processing happens
                    if st.button("Process Survey"):
                        with st.spinner("Processing survey data..."):
                            if process_file(file_path):
                                st.rerun()

            # Tab 1: Enter Questions
            with tabs[1]:
                st.subheader("Enter your survey questions")

                # Display questions with their answers
                for q_idx, question in enumerate(st.session_state.survey_data['questions']):
                    with st.expander(f"Question {q_idx + 1}", expanded=True):
                        # Question and data type in the same row
                        q_col1, q_col2 = st.columns([3, 1])

                        with q_col1:
                            question['question'] = st.text_area(
                                "Question",
                                value=question.get('question', ''),
                                key=f"q_{q_idx}"
                            )

                        with q_col2:
                            # Get the current data type and determine the index
                            current_data_type = question.get('data_type', 'Percent')
                            data_type_index = 0 if current_data_type == 'Percent' else 1

                            # Set the selectbox with the correct index
                            question['data_type'] = st.selectbox(
                                "Data type",
                                options=["Percent", "Count"],
                                index=data_type_index,
                                key=f"dtype_{q_idx}"
                            )

                        # Display answer fields
                        st.write("Answers:")
                        for a_idx, answer in enumerate(question.get('answers', [])):
                            ans_col1, ans_col2, ans_col3 = st.columns([3, 1, 0.5], vertical_alignment="bottom")

                            with ans_col1:
                                answer['answer'] = st.text_input(
                                    "Answer",
                                    value=answer.get('answer', ''),
                                    key=f"q{q_idx}_a{a_idx}",
                                    label_visibility="collapsed"
                                )

                            with ans_col2:
                                answer['value'] = st.number_input(
                                    "Value",
                                    value=float(answer.get('value', 0)),
                                    key=f"q{q_idx}_v{a_idx}",
                                    label_visibility="collapsed"
                                )

                            # Delete answer button (don't show for first answer)
                            with ans_col3:
                                if a_idx > 0:
                                    if st.button("❌", key=f"del_ans_{q_idx}_{a_idx}", help="Delete answer"):
                                        question['answers'].pop(a_idx)
                                        st.rerun()

                        # Add answer button
                        if st.button("➕ Add another answer", key=f"add_ans_{q_idx}"):
                            question['answers'].append({'answer': '', 'value': 0})
                            st.rerun()

                    # Delete question button (don't show for first question or if it's the only question)
                    if len(st.session_state.survey_data['questions']) > 1:
                        if st.button("❌ Delete Question", key=f"del_q_{q_idx}", help="Delete question"):
                            st.session_state.survey_data['questions'].pop(q_idx)
                            st.rerun()

                # Add question button
                if st.button("➕ Add another question"):
                    st.session_state.survey_data['questions'].append({
                        'question': '',
                        'data_type': 'Percent',
                        'answers': [{'answer': '', 'value': 0}]
                    })
                    st.rerun()

            st.markdown("---")

            back_col, next_col = st.columns(2)

            # Create "Next" button in the right column, enabled only if survey data is valid
            with next_col:
                # Check if data is valid for proceeding
                is_valid = is_survey_data_valid()

                # Create the button, enabled only if data is valid
                if is_valid:
                    if st.button("Next", key="survey_next", use_container_width=True):
                        # Validate data here if needed
                        if 'validated' not in st.session_state:
                            st.session_state.validated = {}
                        st.session_state.validated['Survey'] = True
                        st.session_state.current_screen = 'filters'
                        st.rerun()
                else:
                    # Display disabled button with tooltip
                    st.button(
                        "Next",
                        key="survey_next_disabled",
                        use_container_width=True,
                        disabled=True,
                        help="Please upload survey results or enter them manually"
                    )