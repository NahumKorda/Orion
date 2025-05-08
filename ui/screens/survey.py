import json
import os
import streamlit as st

from agents.questions.crew import SurveyAnalyzingCrew
from ui.screens.html import reduced_title_padding
from ui.utils import get_data_path
from utils.pdf_reader import get_text


def process_file(file_path: str):
    survey_results = get_text(file_path)
    inputs = {
        'survey_results': survey_results
    }
    raw_results = SurveyAnalyzingCrew().crew().kickoff(inputs=inputs)
    results = raw_results.json
    print(f"RESULTS:\n{results}")

    # Store results in session state for further processing
    st.session_state.survey_results = results


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

            # Create tabs for the two input modes
            tab1, tab2 = st.tabs(["Upload Survey", "Enter Questions"])

            with tab1:
                st.subheader("Upload your survey document")

                # Modified file uploader to accept only PDF files
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

                    # Process the file and store results in session state
                    process_file(file_path)

                    st.success(f"File '{uploaded_file.name}' successfully uploaded and processed!")

                    # Store the file path in session state
                    st.session_state.survey_data['uploaded_file'] = file_path

                    # Show a preview of the results if available
                    if 'survey_results' in st.session_state:
                        with st.expander("Preview of Processed Results", expanded=False):
                            st.json(st.session_state.survey_results)

            with tab2:
                st.subheader("Enter your survey questions")

                # Survey title
                st.session_state.survey_data['title'] = st.text_input(
                    "Survey Title",
                    value=st.session_state.survey_data.get('title', '')
                )

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
                            question['data_type'] = st.selectbox(
                                "Data type",
                                options=["Percent", "Count"],
                                index=0 if question.get('data_type') == 'Percent' else 1,
                                key=f"dtype_{q_idx}"
                            )

                        # Display answer fields
                        st.write("Answers:")
                        for a_idx, answer in enumerate(question.get('answers', [])):
                            ans_col1, ans_col2, ans_col3 = st.columns([3, 1, 0.5], vertical_alignment="bottom")

                            with ans_col1:
                                answer['answer'] = st.text_input(
                                    "Answer" if a_idx == 0 else "",
                                    value=answer.get('answer', ''),
                                    key=f"q{q_idx}_a{a_idx}"
                                )

                            with ans_col2:
                                answer['value'] = st.number_input(
                                    "Value" if a_idx == 0 else "",
                                    value=float(answer.get('value', 0)),
                                    key=f"q{q_idx}_v{a_idx}"
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

                    # Delete question button (don't show for first question)
                    if q_idx > 0:
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

                # Debug - show current data structure
                if st.checkbox("Show JSON Data"):
                    st.json(st.session_state.survey_data)

            st.markdown("---")

            back_col, next_col = st.columns(2)

            # Create regular "Next" button in the right column
            with next_col:
                if st.button("Next", key="survey_next", use_container_width=True):
                    # Validate data here if needed
                    if 'validated' not in st.session_state:
                        st.session_state.validated = {}
                    st.session_state.validated['Survey'] = True
                    st.session_state.current_screen = 'filters'
                    st.rerun()