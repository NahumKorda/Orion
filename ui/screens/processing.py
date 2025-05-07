import streamlit as st
import time

from sympy.printing.pretty.pretty_symbology import center

from ui.screens.html import reduced_title_padding


def show_processing_screen():
    # Create a centered container with 50% width
    container = st.container()
    with container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title("Processing")

            # Initialize processing states in session state if they don't exist
            if 'processing_steps' not in st.session_state:
                st.session_state.processing_steps = {
                    'started': False,
                    'social_media': False,
                    'news_agencies': False,
                    'information_processing': False,
                    'deep_analysis': False,
                    'completed': False
                }

            # Display checklist of previous steps
            st.subheader("Steps Completed")

            # For each completed step, add a "Back to X" button
            for step, validated in st.session_state.validated.items():
                # Create two columns for each step - one for the status, one for the button
                step_col, button_col = st.columns([3, 2], vertical_alignment='center')

                with step_col:
                    check_icon = "✅" if validated else "❌"
                    st.markdown(f"{check_icon} {step}")

                # Only show back button if step is validated/completed
                with button_col:
                    if validated:
                        # Convert step name to lowercase and replace spaces with underscores for page name
                        page_name = step.lower().replace(" ", "_")
                        if st.button(f"Back to {step}", key=f"back_to_{page_name}"):
                            # Set current screen to the selected step's page
                            st.session_state.current_screen = page_name
                            st.rerun()

            st.markdown("---")

            # Processing section
            if not st.session_state.processing_steps['started']:
                col1, col2, col3 = st.columns([3, 2, 3])
                with col2:
                    if st.button("Start Processing"):
                        st.session_state.processing_steps['started'] = True
                        st.rerun()
            else:
                # Display all completed steps and their success messages
                if st.session_state.processing_steps['social_media']:
                    st.success("Social media data collected")

                if st.session_state.processing_steps['news_agencies']:
                    st.success("News data collected")

                if st.session_state.processing_steps['information_processing']:
                    st.success("Information processed")

                if st.session_state.processing_steps['deep_analysis']:
                    st.success("Analysis completed and insights are available")

                # Processing steps with spinners and messages
                # Only show spinner for the current uncompleted step
                if not st.session_state.processing_steps['social_media']:
                    with st.spinner("Collecting data from social media..."):
                        time.sleep(5)  # Simulate processing
                        st.session_state.processing_steps['social_media'] = True
                        st.rerun()

                elif not st.session_state.processing_steps['news_agencies']:
                    # Wait a bit before starting next step
                    time.sleep(2)
                    with st.spinner("Collecting data from news agencies..."):
                        time.sleep(5)  # Simulate processing
                        st.session_state.processing_steps['news_agencies'] = True
                        st.rerun()

                elif not st.session_state.processing_steps['information_processing']:
                    # Wait a bit before starting next step
                    time.sleep(2)
                    with st.spinner("Information processing..."):
                        time.sleep(5)  # Simulate processing
                        st.session_state.processing_steps['information_processing'] = True
                        st.rerun()

                elif not st.session_state.processing_steps['deep_analysis']:
                    # Wait a bit before starting next step
                    time.sleep(2)
                    with st.spinner("Deep analysis..."):
                        time.sleep(5)  # Simulate processing
                        st.session_state.processing_steps['deep_analysis'] = True
                        st.rerun()

                elif not st.session_state.processing_steps['completed']:
                    # Wait a bit before showing the View Insights button
                    time.sleep(2)
                    st.session_state.processing_steps['completed'] = True
                    st.rerun()

                # Show View Insights button when completed
                if st.session_state.processing_steps['completed']:
                    col1, col2, col3 = st.columns([3, 2, 3])
                    with col2:
                        if st.button("View Insights"):
                            # Reset processing state for potential reuse
                            st.session_state.processing_steps = {
                                'started': False,
                                'social_media': False,
                                'news_agencies': False,
                                'information_processing': False,
                                'deep_analysis': False,
                                'completed': False
                            }
                            st.session_state.current_screen = 'insights'
                            st.rerun()