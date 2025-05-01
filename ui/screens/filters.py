import streamlit as st


def show_filters_screen():
    # Create a centered container with 50% width
    container = st.container()
    with container:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title("Filters")

            # Initialize filters in session state if they don't exist
            if 'filters' not in st.session_state:
                st.session_state.filters = {
                    'keywords': [],
                    'sentiment': [],
                }

            # Define callback functions for each filter type
            def add_filter_item(filter_key):
                input_key = f"text_{filter_key}"
                if st.session_state[input_key] and st.session_state[input_key] not in st.session_state.filters[
                    filter_key]:
                    st.session_state.filters[filter_key].append(st.session_state[input_key])
                    st.session_state[input_key] = ""  # Clear the input

            # Check if survey was uploaded to show "Generate Automatically" button
            if st.session_state.survey_data.get('uploaded_file'):
                col1, col2 = st.columns([9, 1])
                with col2:
                    if st.button("Generate Automatically", key="gen_auto"):
                        # Simulate auto-generation with some sample data
                        st.session_state.filters = {
                            'keywords': ['election', 'policy', 'candidate'],
                            'sentiment': ['positive', 'negative', 'neutral'],
                        }
                        st.rerun()

            # Create sections for each filter type
            filter_sections = [
                ('Keywords', 'keywords', 'Enter keywords to filter by'),
                ('Sentiment', 'sentiment', 'Enter sentiment categories'),
            ]

            for title, key, placeholder in filter_sections:
                with st.expander(title, expanded=True):
                    st.subheader(title)

                    # Display existing items
                    for i, item in enumerate(st.session_state.filters[key]):
                        col1, col2 = st.columns([10, 1], vertical_alignment="bottom")
                        with col1:
                            st.text(item)
                        with col2:
                            if st.button("❌", key=f"delete_{key}_{i}", help="Delete item"):
                                st.session_state.filters[key].pop(i)
                                st.rerun()

                    # Add new item using the callback approach
                    col1, col2 = st.columns([10, 1], vertical_alignment="bottom")
                    with col1:
                        new_item = st.text_input(f"Add {title.lower()}",
                                                 placeholder=placeholder,
                                                 key=f"text_{key}",
                                                 on_change=add_filter_item,
                                                 args=(key,))
                    with col2:
                        if st.button("➕", key=f"add_{key}", help="Add item"):
                            add_filter_item(key)
                            st.rerun()

            # Add space before navigation buttons
            st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

            back_col, empty_col, next_col = st.columns([3, 10, 2.2])

            # Create regular "Back" button in the left column
            with back_col:
                if st.button("Back", key="filters_back"):
                    st.session_state.current_screen = 'survey'
                    st.rerun()

            # Create regular "Next" button in the right column
            with next_col:
                if st.button("Next", key="filters_next"):
                    st.session_state.validated['Filters'] = True
                    st.session_state.current_screen = 'questions'
                    st.rerun()