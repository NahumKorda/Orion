import base64
import os
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

from ui.pdf import create_pdf


def show_insights_screen():
    # Consolidate all CSS styling into a single markdown element
    st.markdown("""
    <style>
        /* Remove default Streamlit padding and margins */
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            padding-left: 1rem;
            padding-right: 1rem;
            margin-top: 0 !important;
        }
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}

        /* Remove any top borders or lines */
        .main .block-container::before {
            content: none !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            height: 0 !important;
        }

        /* Remove extra padding at the very top */
        [data-testid="stAppViewContainer"] > div:first-child {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }

        /* Header styling */
        h1 {
            margin-top: 0 !important;
            padding-top: 0 !important;
            margin-bottom: 0.25rem !important;
            padding-bottom: 0 !important;
            display: inline-block !important;
        }

        /* Header container styling */
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Button container styling */
        .button-container {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            gap: 10px;
        }

        /* Style for buttons */
        /* Fix spacing for header columns */
        [data-testid="stHorizontal"] > div:first-child {
            padding-right: 0 !important;
        }

        /* Align buttons to the right */
        .header-right-col {
            display: flex;
            justify-content: flex-end;
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Fix streamlit columns alignment */
        .row-widget.stHorizontal {
            align-items: flex-start !important;
        }

        /* Make all columns align at the top */
        [data-testid="column"] {
            align-self: flex-start !important;
            margin-top: 0 !important;
            padding-top: 0 !important;
        }

        /* Adjust tab positioning and spacing */
        .stTabs [data-baseweb="tab-list"] {
            margin-top: -25px !important;
            padding-top: 0 !important;
            margin-bottom: -5px !important;
        }

        .stTabs [data-baseweb="tab-panel"] {
            margin-top: 5px !important;
            padding-top: 0 !important;
        }

        /* Additional spacing for iframe container in tabs */
        .stTabs [data-baseweb="tab-panel"] .iframe-container {
            margin-top: 5px !important;
        }

        /* Basic message styling */
        .user-message {
            background-color: #e0e0e0;
            border-radius: 15px 15px 15px 0;
            padding: 8px 12px;
            margin: 5px 0;
            max-width: 80%;
            float: left;
            clear: both;
        }
        .assistant-message {
            background-color: #1E4D8C;
            color: white;
            border-radius: 15px 15px 0 15px;
            padding: 8px 12px;
            margin: 5px 0;
            max-width: 80%;
            float: right;
            clear: both;
        }

        /* Consistent iframe container styling */
        .iframe-container {
            height: 60vh;
            margin: 0 !important;
            padding: 0 !important;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
            display: block;
            margin-bottom: 10px !important; /* Reduced space below iframe container */
        }

        /* Special styling for iframe in right column (tabs) */
        [data-testid="stVerticalBlock"] > div > [data-testid="stHorizontal"] > div:nth-child(2) .iframe-container {
            margin-top: 5px !important;
        }

        /* Consistent iframe styling */
        .iframe-container iframe {
            width: 100%;
            height: 100%;
            border: none;
            margin: 0 !important;
            padding: 0 !important;
            display: block;
        }

        /* Clear floats */
        .clearfix:after {
            content: "";
            display: table;
            clear: both;
        }

        /* Just make sure navigation buttons have proper margins */
        .stTabs [data-baseweb="tab-panel"] .stButton > button {
            margin-top: 5px !important;
        }

        /* Position indicator styling */
        .stTabs [data-baseweb="tab-panel"] .stMarkdown p {
            margin-top: 5px !important;
        }

        /* Remove space between title and tabs */
        .stTabs {
            margin-top: -25px !important;
        }

        /* Fix spacing for text input label */
        [data-testid="stTextInput"] label {
            margin-top: -22px !important;
            padding: 0 !important;
            overflow: hidden !important;
            position: absolute !important;
        }

        /* Reduce space after iframe */
        .iframe-container {
            margin-bottom: 5px !important;
        }

        /* Adjust text input spacing */
        [data-testid="stTextInput"] {
            margin-top: -5px !important;
            padding-top: 0 !important;
        }

        /* Custom container margin */
        .custom-container {
            margin-bottom: 30px;
        }

        /* Add margin-bottom to the first stElement under header container */
        [data-testid="stVerticalBlock"] > div:first-child {
            margin-bottom: 1.5rem !important;
        }

        /* Target this specific container */
        [data-testid="stVerticalBlock"] > div:first-child > div:first-child {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }

        /* Reduce spacing between all streamlit elements */
        div.stElement > div {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }

        /* Force column containers to align at the top with minimal spacing */
        .row-widget.stHorizontal > div {
            align-items: flex-start !important;
            margin-top: 0 !important;
            padding-top: 0 !important;
        }

        /* File position counter styles to match text input label */
        .file-position-label {
            font-size: 14px !important;
            margin-bottom: 0 !important;
            font-weight: 400 !important;
            line-height: 1.6 !important;
            padding: 0 !important;
            margin-top: -5px !important;
            height: auto !important;
            display: block !important;
        }

        /* Fix vertical alignment across columns */
        [data-testid="stHorizontal"] > div {
            vertical-align: top !important;
        }

        /* Remove margin from text input */
        [data-testid="stTextInput"] {
            margin-top: 0 !important;
        }
        
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state variables if they don't exist
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'current_html_index' not in st.session_state:
        st.session_state.current_html_index = {'Quantitative results': 0, 'Qualitative results': 0}
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Quantitative results"
    if 'session_id' not in st.session_state:
        st.session_state.session_id = int(time.time() * 1000)

    current_path = Path(__file__).resolve()
    package_root = current_path.parent.resolve()
    parent_root = package_root.parent.resolve()
    project_root = parent_root.parent.resolve()
    data_path = os.path.join(project_root, "data")

    # Sample HTML files for demonstration (replace with actual file paths)
    if 'html_files' not in st.session_state:
        st.session_state.html_files = {
            'Quantitative results': [
                os.path.join(data_path, "quantitative/01.html"),
                os.path.join(data_path, "quantitative/02.html"),
                os.path.join(data_path, "quantitative/03.html"),
                os.path.join(data_path, "quantitative/04.html"),
                os.path.join(data_path, "quantitative/05.html"),
                os.path.join(data_path, "quantitative/06.html"),
            ],
            'Qualitative results': [
                os.path.join(data_path, "qualitative/01.html"),
                os.path.join(data_path, "qualitative/02.html"),
                os.path.join(data_path, "qualitative/03.html"),
                os.path.join(data_path, "qualitative/04.html"),
                os.path.join(data_path, "qualitative/05.html"),
                os.path.join(data_path, "qualitative/06.html"),
                os.path.join(data_path, "qualitative/07.html"),
            ]
        }

    def send_message():
        if st.session_state.user_input.strip():
            # Add user message to chat
            st.session_state.chat_messages.append({
                "role": "user",
                "content": st.session_state.user_input,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

            # Simulate assistant response (replace with actual response logic)
            response = f"This is a response to: {st.session_state.user_input}"
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

            # Clear input
            st.session_state.user_input = ""

            # Update session ID to force refresh of HTML component
            st.session_state.session_id = int(time.time() * 1000)

    def navigate_html(direction, tab_name=None):
        # If tab_name is provided, use it; otherwise use active_tab from session state
        tab_to_use = tab_name if tab_name else st.session_state.active_tab

        current_index = st.session_state.current_html_index[tab_to_use]
        max_index = len(st.session_state.html_files[tab_to_use]) - 1

        if direction == "prev" and current_index > 0:
            st.session_state.current_html_index[tab_to_use] -= 1
        elif direction == "next" and current_index < max_index:
            st.session_state.current_html_index[tab_to_use] += 1

    # NEW STRUCTURE: First create header container at the top level (outside any columns)
    header_container = st.container()
    with header_container:
        # Create columns for title and buttons
        title_col, buttons_col = st.columns([3, 1], vertical_alignment="center")

        # Add title to the left column
        with title_col:
            st.title("Results")

        # Add buttons to the right column
        with buttons_col:
            # Use columns to place buttons side by side
            btn_cols = st.columns(2, vertical_alignment="center")

            # Download PDF button
            with btn_cols[0]:
                st.download_button(
                    label="Download PDF",
                    data=create_pdf(),
                    file_name="orion_dashboard.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            # New Survey button
            with btn_cols[1]:
                if st.button("New Survey", key="insights_back", use_container_width=True):
                    st.session_state.current_screen = 'survey'
                    st.rerun()

    # Then create the main container with left and right columns
    main_container = st.container()
    with main_container:
        # Create two columns for the panels with zero spacing
        left_col, right_col = st.columns(2)

        # Left Panel - Chat
        with left_col:
            # Chat messages container
            chat_container = st.container()

            # Create a container for the scrollable area
            with chat_container:
                # Build chat messages HTML
                messages_html = ""
                for message in st.session_state.chat_messages:
                    if message["role"] == "user":
                        messages_html += f"""
                        <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                            <div style="background-color: #e0e0e0; color: black; padding: 8px 12px; 
                                 border-radius: 15px 15px 0 15px; max-width: 80%; text-align: right; word-wrap: break-word;
                                 font-family: Arial, sans-serif;">
                                {message['content']}
                            </div>
                        </div>
                        """
                    else:
                        messages_html += f"""
                        <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                            <div style="background-color: #1E4D8C; color: white; padding: 8px 12px; 
                                 border-radius: 15px 15px 15px 0; max-width: 80%; text-align: left; word-wrap: break-word;
                                 font-family: Arial, sans-serif;">
                                {message['content']}
                            </div>
                        </div>
                        """

                # Create a full HTML component with proper height settings for chat
                chat_html = f"""
                <!DOCTYPE html>
                <html style="height: 100%; margin: 0; padding: 0;">
                <head>
                    <style>
                        html, body {{
                            height: 100%;
                            margin: 0;
                            padding: 0;
                            overflow: hidden;
                            font-family: Arial, sans-serif;
                        }}
                        body {{
                            display: flex;
                            flex-direction: column;
                            font-family: Arial, sans-serif;
                        }}
                        #chat-container {{
                            flex: 1;
                            display: flex;
                            flex-direction: column;
                            height: 100%;
                            overflow: hidden;
                            padding: 10px;
                            font-family: Arial, sans-serif;
                        }}
                        #empty-space {{
                            flex-grow: 1;
                        }}
                        #messages {{
                            overflow-y: auto;
                            font-family: Arial, sans-serif;
                        }}
                        .user-message, .assistant-message {{
                            font-family: Arial, sans-serif;
                        }}
                    </style>
                </head>
                <body>
                    <div id="chat-container">
                        <div id="empty-space"></div>
                        <div id="messages">
                            {messages_html}
                        </div>
                    </div>

                    <script>
                        // Function to scroll to bottom of chat
                        function scrollToBottom() {{
                            const messageContainer = document.getElementById('messages');
                            if (messageContainer) {{
                                messageContainer.scrollTop = messageContainer.scrollHeight;
                            }}
                        }}

                        // Scroll when loaded and after delays
                        window.onload = function() {{
                            scrollToBottom();
                            setTimeout(scrollToBottom, 100);
                            setTimeout(scrollToBottom, 500);
                        }};
                    </script>
                </body>
                </html>
                """

                # Create a data URL for the chat content
                chat_data_url = f"data:text/html;base64,{base64.b64encode(chat_html.encode()).decode()}"

                # Display using the consistent iframe container
                st.markdown(
                    f'<div class="iframe-container"><iframe src="{chat_data_url}"></iframe></div>',
                    unsafe_allow_html=True
                )

            # Chat input area
            st.text_input("Ask questions about the results:", key="user_input", on_change=send_message,
                          placeholder="Type your question here...")

        # Right Panel - HTML Display
        with right_col:
            # Create tabs using Streamlit's native tab component
            tab1, tab2 = st.tabs(["Quantitative results", "Qualitative results"])

            # Define a callback that will be executed after tab selection
            if "previous_tab" not in st.session_state:
                st.session_state.previous_tab = None

            # Update session state based on tab selection
            with tab1:
                # Content for Quantitative results tab
                if st.session_state.previous_tab != 0:
                    st.session_state.active_tab = "Quantitative results"
                    st.session_state.previous_tab = 0

                # Get current HTML file for this tab
                active_tab = "Quantitative results"
                current_index = st.session_state.current_html_index[active_tab]
                html_files = st.session_state.html_files[active_tab]

                # Display HTML content for this tab
                if html_files:
                    try:
                        current_file = html_files[current_index]
                        try:
                            if os.path.exists(current_file):
                                with open(current_file, 'r') as f:
                                    html_content = f.read()
                            else:
                                html_content = f"<html><body><h2>File not found</h2><p>Could not locate: {current_file}</p></body></html>"
                        except Exception as e:
                            html_content = f"<html><body><h2>Error loading file</h2><p>{str(e)}</p></body></html>"

                        # Use a very simple approach - just add padding to the HTML
                        simple_html = f"""
                        <html>
                        <head>
                            <style>
                                body {{
                                    padding-top: 20px;  /* Reduced padding */
                                    padding-bottom: 20px;  /* Reduced padding */
                                    padding-left: 20px;
                                    padding-right: 20px;
                                }}
                            </style>
                        </head>
                        <body>
                            {html_content}
                        </body>
                        </html>
                        """

                        # Encode the HTML content
                        encoded_html = base64.b64encode(simple_html.encode()).decode()

                        # Use the consistent iframe container
                        st.markdown(
                            f'<div class="iframe-container"><iframe src="data:text/html;base64,{encoded_html}"></iframe></div>',
                            unsafe_allow_html=True
                        )
                    except Exception as e:
                        st.error(f"Error displaying HTML: {str(e)}")

                # Show current position with proper label alignment
                if html_files:
                    current_index = st.session_state.current_html_index[active_tab]
                    total_files = len(html_files)
                    st.markdown(f'<div class="file-position-label">File {current_index + 1} of {total_files}:</div>',
                                unsafe_allow_html=True)

                # Navigation buttons for this tab
                nav_col1, nav_col2 = st.columns(2)
                with nav_col1:
                    prev_disabled = st.session_state.current_html_index[active_tab] == 0
                    if st.button("← Previous", key="prev_btn_quant", on_click=navigate_html,
                                 args=("prev", "Quantitative results"),
                                 disabled=prev_disabled, use_container_width=True):
                        pass

                with nav_col2:
                    next_disabled = len(html_files) == 0 or st.session_state.current_html_index[active_tab] >= len(
                        html_files) - 1
                    if st.button("Next →", key="next_btn_quant", on_click=navigate_html,
                                 args=("next", "Quantitative results"),
                                 disabled=next_disabled, use_container_width=True):
                        pass

            with tab2:
                # Content for Qualitative results tab
                if st.session_state.previous_tab != 1:
                    st.session_state.active_tab = "Qualitative results"
                    st.session_state.previous_tab = 1

                # Get current HTML file for this tab
                active_tab = "Qualitative results"
                current_index = st.session_state.current_html_index[active_tab]
                html_files = st.session_state.html_files[active_tab]

                # Display HTML content for this tab
                if html_files:
                    try:
                        current_file = html_files[current_index]
                        try:
                            if os.path.exists(current_file):
                                with open(current_file, 'r', encoding='utf-8') as f:
                                    html_content = f.read()
                            else:
                                html_content = f"<html><body><h2>File not found</h2><p>Could not locate: {current_file}</p></body></html>"
                        except Exception as e:
                            html_content = f"<html><body><h2>Error loading file</h2><p>{str(e)}</p></body></html>"

                        simple_html = f"""
                        <html>
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                            <style>
                                html, body {{
                                    height: 100%;
                                    margin: 0;
                                    padding: 0;
                                    overflow: hidden;
                                }}
                                .scrollable-container {{
                                    height: 100%;
                                    width: 100%;
                                    overflow-y: auto;
                                    overflow-x: auto;
                                    box-sizing: border-box;
                                }}
                                .content-wrapper {{
                                    padding: 20px;
                                    min-height: 100%;
                                    box-sizing: border-box;
                                    /* Center the content horizontally */
                                    display: flex;
                                    flex-direction: column;
                                    align-items: center;
                                }}
                                /* In case the card itself needs specific centering */
                                .content-wrapper > * {{
                                    max-width: 100%;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="scrollable-container">
                                <div class="content-wrapper">
                                    {html_content}
                                </div>
                            </div>
                        </body>
                        </html>
                        """

                        # Encode the HTML content
                        encoded_html = base64.b64encode(simple_html.encode()).decode()

                        # Use the consistent iframe container
                        st.markdown(
                            f'<div class="iframe-container"><iframe src="data:text/html;base64,{encoded_html}"></iframe></div>',
                            unsafe_allow_html=True
                        )
                    except Exception as e:
                        st.error(f"Error displaying HTML: {str(e)}")

                # Show current position with proper label alignment
                if html_files:
                    current_index = st.session_state.current_html_index[active_tab]
                    total_files = len(html_files)
                    st.markdown(f'<div class="file-position-label">File {current_index + 1} of {total_files}:</div>',
                                unsafe_allow_html=True)

                # Navigation buttons for this tab
                nav_col1, nav_col2 = st.columns(2)
                with nav_col1:
                    prev_disabled = st.session_state.current_html_index[active_tab] == 0
                    if st.button("← Previous", key="prev_btn_qual", on_click=navigate_html,
                                 args=("prev", "Qualitative results"),
                                 disabled=prev_disabled, use_container_width=True):
                        pass

                with nav_col2:
                    next_disabled = len(html_files) == 0 or st.session_state.current_html_index[active_tab] >= len(
                        html_files) - 1
                    if st.button("Next →", key="next_btn_qual", on_click=navigate_html,
                                 args=("next", "Qualitative results"),
                                 disabled=next_disabled, use_container_width=True):
                        pass