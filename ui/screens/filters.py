import streamlit as st

from ui.screens.html import reduced_title_padding


def show_filters_screen():
    st.markdown(reduced_title_padding(), unsafe_allow_html=True)

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

            # Extract keywords correctly based on their structure
            keywords = []
            if 'keywords' in st.session_state.filters:
                # Check if keywords is a dictionary with numeric keys
                if isinstance(st.session_state.filters['keywords'], dict):
                    # It's a dictionary, so extract values
                    for key, value in st.session_state.filters['keywords'].items():
                        if isinstance(value, str):
                            keywords.append(value)
                elif isinstance(st.session_state.filters['keywords'], list):
                    # It's already a list, use it directly
                    keywords = st.session_state.filters['keywords']
                elif isinstance(st.session_state.filters['keywords'], str):
                    # It's a single string, convert to list
                    keywords = [st.session_state.filters['keywords']]

                # Update the keywords in session state to ensure correct format
                st.session_state.filters['keywords'] = keywords

            # Define callback functions for each filter type
            def add_filter_item(filter_key):
                input_key = f"text_{filter_key}"
                if st.session_state[input_key] and st.session_state[input_key] not in st.session_state.filters[
                    filter_key]:
                    st.session_state.filters[filter_key].append(st.session_state[input_key])
                    st.session_state[input_key] = ""  # Clear the input

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

                    # Add space after the last item if there are any items
                    if st.session_state.filters[key]:
                        st.markdown("<br>", unsafe_allow_html=True)

                    # Add new item using the callback approach
                    col1, col2 = st.columns([10, 1], vertical_alignment="bottom")
                    with col1:
                        st.text_input(f"Add {title.lower()}",
                                      placeholder=placeholder,
                                      key=f"text_{key}",
                                      on_change=add_filter_item,
                                      args=(key,))
                    with col2:
                        if st.button("➕", key=f"add_{key}", help="Add item"):
                            add_filter_item(key)
                            st.rerun()

            st.markdown("---")

            back_col, next_col = st.columns(2)

            # Create regular "Back" button in the left column
            with back_col:
                if st.button("Back", key="filters_back", use_container_width=True):
                    st.session_state.current_screen = 'survey'
                    st.rerun()

            # Create regular "Next" button in the right column
            with next_col:
                if st.button("Next", key="filters_next", use_container_width=True):
                    st.session_state.validated['Filters'] = True
                    st.session_state.current_screen = 'questions'
                    st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)