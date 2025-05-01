import streamlit as st


def show_survey_screen():
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
                uploaded_file = st.file_uploader("Choose a file",
                                                 type=["docx", "pdf", "txt", "csv"],
                                                 help="Upload your survey document",
                                                 key='survey_uploader')

                if uploaded_file is not None:
                    st.success(f"File '{uploaded_file.name}' successfully uploaded!")
                    # Store the file in session state
                    st.session_state.survey_data['uploaded_file'] = uploaded_file.name

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

            back_col, empty_col, next_col = st.columns([3, 10, 2.2])

            # Create regular "Next" button in the right column
            with next_col:
                if st.button("Next", key="survey_next"):
                    # Validate data here if needed
                    if 'validated' not in st.session_state:
                        st.session_state.validated = {}
                    st.session_state.validated['Survey'] = True
                    st.session_state.current_screen = 'filters'
                    st.rerun()