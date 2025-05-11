import streamlit as st

from ui.screens.html import reduced_title_padding

def show_questions_screen():

    st.markdown(reduced_title_padding(), unsafe_allow_html=True)

    container = st.container()
    with container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title("Questions")

            # Initialize selected questions in session state if they don't exist
            if 'selected_questions' not in st.session_state:
                st.session_state.selected_questions = []

            # Initialize custom questions in session state if they don't exist
            if 'custom_questions' not in st.session_state:
                st.session_state.custom_questions = []

            # Extract questions from survey_results
            survey_questions = []
            if 'survey_results' in st.session_state and 'questions' in st.session_state.survey_results:
                for q in st.session_state.survey_results.get('questions', []):
                    question_text = q.get('question', '')
                    if question_text:  # Only add non-empty questions
                        survey_questions.append(question_text)

            # Display questions from survey_results with checkboxes
            st.subheader("Select Questions")

            if not survey_questions:
                st.info("No questions found in survey results.")
            else:
                for i, question in enumerate(survey_questions):
                    checked = question in st.session_state.selected_questions
                    if st.checkbox(question, value=checked, key=f"question_checkbox_{i}"):
                        if question not in st.session_state.selected_questions:
                            st.session_state.selected_questions.append(question)
                    else:
                        if question in st.session_state.selected_questions:
                            st.session_state.selected_questions.remove(question)

            # Section for custom questions
            st.markdown("---")
            st.subheader("Add Custom Questions")

            # Display existing custom questions
            for i, question in enumerate(st.session_state.custom_questions):
                col1, col2 = st.columns([10, 1])
                with col1:
                    st.text(question)
                with col2:
                    if st.button("❌", key=f"delete_custom_{i}", help="Delete question"):
                        st.session_state.custom_questions.pop(i)
                        st.rerun()

            def add_question():
                if st.session_state.new_custom_question and st.session_state.new_custom_question not in st.session_state.custom_questions:
                    st.session_state.custom_questions.append(st.session_state.new_custom_question)
                    # This will only affect the next run of the app
                    st.session_state.new_custom_question = ""

            # Add new custom question
            col1, col2 = st.columns([10, 1], vertical_alignment="bottom")
            with col1:
                new_question = st.text_input("Enter a custom question",
                                             placeholder="Type your question here",
                                             key="new_custom_question",
                                             on_change=add_question)
            with col2:
                if st.button("➕", key="add_custom_question", help="Add question"):
                    if new_question and new_question not in st.session_state.custom_questions:
                        st.session_state.custom_questions.append(new_question)
                        st.session_state.new_custom_question = ""
                        st.rerun()

            st.markdown("---")

            back_col, next_col = st.columns(2)

            # Create regular "Back" button in the left column
            with back_col:
                if st.button("Back", key="questions_back", use_container_width=True):
                    st.session_state.current_screen = 'filters'
                    st.rerun()

            # Create regular "Next" button in the right column
            with next_col:
                if st.button("Next", key="questions_next", use_container_width=True):
                    st.session_state.validated['Questions'] = True
                    st.session_state.current_screen = 'processing'
                    st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)